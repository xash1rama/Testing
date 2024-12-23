import json
from .factories import ClientFactory, ParkingFactory



def test_create_client(client, db):
    new_client = ClientFactory()
    db.session.commit()
    client_data = {
        "name": new_client.name,
        "surname": new_client.surname,
        "credit_card": new_client.credit_card,
        "car_number": new_client.car_number}
    print(client_data)
    resp = client.post("/clients", data=json.dumps(client_data), content_type='application/json')
    assert resp.status_code == 201


def test_create_parking(client, db):
    parking = ParkingFactory()
    db.session.commit()
    parking_data = {
        "address": parking.address,
        "opened": parking.opened,
        "count_place": parking.count_places,
        "count_available_places": parking.count_available_places}
    print(parking_data)
    resp = client.post("/parkings", data=json.dumps(parking_data), content_type='application/json')
    assert resp.status_code == 201
