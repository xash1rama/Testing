from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    # @app.before_first_request

    @app.before_first_request
    def before_req():
        db.create_all()
        new_client1 = Client(name="Влад", surname="Владов", credit_card="SBER", car_number="2777KX-3")
        new_client2 = Client(name="Денис", surname="Денисов", credit_card="BELARUSBANK", car_number="1353EA-3")
        new_client3 = Client(name="Игорь", surname="Игорев", credit_card="BSB", car_number="5475KO-4")
        new_client4 = Client(name="Света", surname="Светланова", credit_card="VTB", car_number="2123PP-5")
        new_client5 = Client(name="Таня", surname="Танькина", credit_card="T-BANK", car_number="4245ET-5")
        new_park1 = Parking(address="Homel", opened=True, count_places=100, count_available_places=100)
        new_park2 = Parking(address="Minsk", opened=True, count_places=58, count_available_places=58)
        fix_park1 = ClientParking(client_id=1, parking_id=1)
        fix_park2 = ClientParking(client_id=2, parking_id=2)
        fix_park3 = ClientParking(client_id=3, parking_id=1)
        db.session.add_all([new_client1, new_client2, new_client3, new_client4, new_client5, new_park1, new_park2, fix_park1, fix_park2, fix_park3])
        db.session.commit()


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients")
    def get_all_clients():
        try:
            all_clients = db.session.query(Client).all()
            response = []
            if not all_clients:
                return "Пусто"
            for client in all_clients:
                response.append(client.to_json())
            return render_template("all_clients_template.html", response=response)
            # return jsonify(clients=response)
        except Exception as e:
            return jsonify(error=f"Ошибка: {str(e)}"), 500


    @app.route("/clients/<client_id>")
    def get_clients_with_id(client_id):
        try:
            client_one = db.session.query(Client).where(Client.id == client_id).one_or_none()
            res = [client_one.to_json()]
            print(res)
            return render_template("for_one_template.html", response=res)
            # return jsonify(clients=client.to_json())
        except Exception as e:
            return jsonify(error=f"Ошибка: {str(e)}"), 500


    @app.route("/clients", methods=["POST"])
    def add_client():
        data = request.json
        try:
            if not data.get("name") or not data.get("surname"):
                return "Ошибка, некорректные данные: имя и фамилия обязательны.", 400

            new_client = Client(
                name=data["name"],
                surname=data["surname"],
                credit_card=data.get("credit_card"),
                car_number=data.get("car_number")
            )

            db.session.add(new_client)
            db.session.commit()
            return jsonify(new_client=new_client.to_json()), 201

        except Exception as e:
            return jsonify(error=f"Ошибка: {str(e)}"), 500

    @app.route("/parkings", methods=["POST"])
    def add_new_parking_place():
        data = request.json
        if not data.get("address"):
            return "Не указан адрес", 400
        if not data.get("count_place"):
            return "Не указано количество парковочных мест", 400

        new_parking = Parking(
            address=data["address"],
            opened=True,
            count_places=data["count_place"],
            count_available_places=data["count_place"]
        )

        db.session.add(new_parking)
        db.session.commit()
        return jsonify(new_parking=new_parking.to_json()), 201

    @app.route("/client_parkings", methods=["POST"])
    def client_parking():
        data = request.json
        parking_id = data.get("parking_id")
        client_id = data.get("client_id")

        exam_parking = db.session.query(Parking).filter_by(id=parking_id).one_or_none()
        exam_client = db.session.query(Client).filter_by(id=client_id).one_or_none()

        if not exam_client:
            return f"Клиент с ID {client_id} не найден.", 404
        if not exam_parking:
            return f"Парковка с ID {parking_id} не найдена.", 404
        if not exam_parking.opened:
            return f"Парковка по адресу {exam_parking.address} закрыта.", 404
        if exam_parking.count_available_places <= 0:
            return f"На парковке по адресу {exam_parking.address} нет свободных мест", 404

        exam_parking.count_available_places -= 1
        client_parking_record = ClientParking(client_id=client_id, parking_id=parking_id, time_in=datetime.now())
        db.session.add(client_parking_record)
        db.session.commit()

        return f"Клиент {exam_client.name} {exam_client.surname} занял место на парковке - {exam_parking.address}", 201

    @app.route("/client_parkings", methods=["DELETE"])
    def client_unparking():
        data = request.json
        parking_id = data.get("parking_id")
        client_id = data.get("client_id")

        client = db.session.query(Client).filter_by(id=client_id).one_or_none()
        parking = db.session.query(Parking).filter_by(id=parking_id).one_or_none()
        client_parking_record = db.session.query(ClientParking).filter_by(client_id=client_id,
                                                                          parking_id=parking_id).first()

        if not client_parking_record:
            return "Не корректные данные: отсутствует запись о парковке клиента.", 404
        if not client:
            return "Клиент не найден.", 404

        if client.credit_card:
            parking.count_available_places += 1
            client_parking_record.time_out = datetime.now()
            all_time_in_parking = client_parking_record.time_out - client_parking_record.time_in
            result = (f"Клиент {client.name} {client.surname} выехал с парковки по адресу {parking.address} "
                      f"в {client_parking_record.time_out} (время на парковке: {all_time_in_parking})")

            db.session.delete(client_parking_record)
            db.session.commit()
            return result, 201
        else:
            return "У клиента не привязана карта", 400

    return app