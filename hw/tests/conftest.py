import pytest
from flask import template_rendered
from python_advanced.module_29_testing.hw.main.app import create_app, db as _db
from python_advanced.module_29_testing.hw.main.models import Client, ClientParking, Parking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        new_client1 = Client(name="Влад", surname="Владов", credit_card="SBER", car_number="2777KX-3")
        new_park1 = Parking(address="Homel", opened=True, count_places=100, count_available_places=100)
        fix_park1 = ClientParking(client_id=1, parking_id=1)
        _db.session.add(fix_park1)
        _db.session.add(new_park1)
        _db.session.add(new_client1)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()

@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
