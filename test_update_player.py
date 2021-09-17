import responses, json
from update_player import *


@responses.activate
def test_send_put_request():
    with open("200.json") as f:
        responses.add(
            responses.PUT,
            "http://bla",
            json=json.load(f),
            status=200
        )
    response = send_put_request()
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["profile"]["applications"][0]["applicationId"] == "music_app"
