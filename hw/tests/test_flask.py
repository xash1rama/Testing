import json

import pytest


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_get_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_create_client(client) -> None:
    client_data = {"name": "Оля",
                    "surname": "Олькина",
                    "credit_card": 12345,
                    "car_number": "9346HH-3"}
    resp = client.post("/clients", data=json.dumps(client_data), content_type='application/json')
    assert resp.status_code == 201



def test_create_parking(client) -> None:
    parking_data = {
                    "address": "Mohilev",
                    "count_place": 50,
                    "count_available_places": 50}
    resp = client.post("/parkings", data=json.dumps(parking_data), content_type='application/json')
    assert resp.status_code == 201


@pytest.mark.parking
def test_enter_from_parking(client) -> None:
    client_parkings_data = {
                    "parking_id": 1,
                    "client_id": 1}
    resp = client.post("/client_parkings", data=json.dumps(client_parkings_data), content_type='application/json')
    assert resp.status_code == 201

@pytest.mark.parking
def test_exit_from_parking(client) -> None:
    client_parkings_data = {
                    "parking_id": 1,
                    "client_id": 1}
    resp = client.delete("/client_parkings", data=json.dumps(client_parkings_data), content_type='application/json')
    assert resp.status_code == 201


def test_render_jinja2(client, captured_templates) -> None:
    route = "/clients"
    resp = client.get(route)
    assert resp.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "all_clients_template.html"
    assert context["response"]
    response = context["response"]
    assert response[0]["name"] == "Влад"