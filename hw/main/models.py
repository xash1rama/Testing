from .app import db
from datetime import datetime


class Client(db.Model):
    __tablename__ = "clients"

    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name:str = db.Column(db.String(length=50), nullable=False)
    surname:str = db.Column(db.String(length=50), nullable=False)
    credit_card:int = db.Column(db.String(length=10))
    car_number:str = db.Column(db.String(length=10))
    client_parkings = db.relationship("ClientParking", back_populates="clients")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = "parking"

    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address:str = db.Column(db.String(length=100),nullable=False)
    opened:bool = db.Column(db.Boolean)
    count_places:int = db.Column(db.Integer, nullable=False)
    count_available_places:int = db.Column(db.Integer, nullable=False)
    client_parkings = db.relationship("ClientParking", back_populates="parkings")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = "client_parking"

    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id:int = db.Column(db.Integer, db.ForeignKey("clients.id"))
    parking_id:int = db.Column(db.Integer, db.ForeignKey("parking.id"))
    time_in:int = db.Column(db.DATETIME, default=datetime.now())
    time_out:int = db.Column(db.DATETIME)
    parkings = db.relationship("Parking", back_populates="client_parkings")
    clients = db.relationship("Client", back_populates="client_parkings")
    # __table_args__ = (db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
