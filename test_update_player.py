import responses, json
from update_player import *

test_url = "http://test"

@responses.activate
def test_send_put_request():
    with open("example_data.json") as f:
        responses.add(responses.PUT, test_url, json=json.load(f), status=200)
    assert send_put_request(test_url)


@responses.activate
def test_send_put_request_401():
    with open("401.json") as f:
        responses.add(responses.PUT, test_url, json=json.load(f), status=401)
    assert not send_put_request(test_url)

@responses.activate
def test_send_put_request_handle_HTTPError():
    responses.add(
        responses.PUT, test_url, body=requests.exceptions.HTTPError("http error")
    )
    assert not send_put_request(test_url)

@responses.activate
def test_send_put_request_handle_ConnectionError():
    responses.add(
        responses.PUT, test_url, body=requests.exceptions.ConnectionError("connection error")
    )
    assert not send_put_request(test_url)

@responses.activate
def test_send_put_request_handle_RequestException():
    responses.add(
        responses.PUT, test_url, body=requests.exceptions.RequestException("error while sending request")
    )
    assert not send_put_request(test_url)