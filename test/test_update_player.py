import responses, json, pytest
 
from ..update_player import *

test_url = "http://test"


def test_valid_csv():
    assert valid_csv('input/test.csv')
    with pytest.raises(argparse.ArgumentTypeError):
        valid_csv('hi')
        valid_csv('hi.csv')
        valid_csv('empty.csv')


@responses.activate
def test_update_players():
    with open("input/200.json") as f:
        responses.add(responses.PUT, 'http://test/profiles/clientId:a1:bb:cc:dd:ee:ff', json=json.load(f), status=200)
    assert update_players('input/test.csv', test_url, 20)


@responses.activate
def test_update_players():
    responses.add(responses.PUT, 'http://test/profiles/clientId:b2:bb:cc:dd:ee:ff', status=500)
    assert not update_players('input/test_http_error.csv', test_url, 20)


@responses.activate
def test_update_player():
    assert update_player('a1:bb:cc:dd:ee:ff', test_url)


def test_update_player():
    assert not update_player('hi', test_url)


def test_is_valid_mac_address_valid_input():
    assert is_valid_mac_address("a1:bb:cc:dd:ee:ff")
    assert is_valid_mac_address("FF:FF:FF:FF:FF:FF")
    assert is_valid_mac_address("00:00:00:00:00:00")
    assert is_valid_mac_address("00-00-00-00-00-00")


def test_is_valid_mac_address_invalid_input():
    assert not is_valid_mac_address("g1:bb:cc:dd:ee:ff")
    assert not is_valid_mac_address("aa1:bb:cc:dd:ee:ff")
    assert not is_valid_mac_address("a1:bb:cc:dd:ee.ff")
    assert not is_valid_mac_address(" a1:bb:cc:dd:ee:ff")
    assert not is_valid_mac_address("a1:bb:cc:dd:ee:ff ")
    assert not is_valid_mac_address("hi")
    assert not is_valid_mac_address("(#@&$%^%$)")
    assert not is_valid_mac_address("a1:bb:cc:dd:ee")
    assert not is_valid_mac_address("a1:bb:cc:dd:ee:ff:ff")
    assert not is_valid_mac_address("a1:bb:cc:dd:ee:f")


@responses.activate
def test_send_put_request():
    with open("input/200.json") as f:
        responses.add(responses.PUT, test_url, json=json.load(f), status=200)
    assert send_put_request(test_url)


@responses.activate
def test_send_put_request_401():
    with open("input/401.json") as f:
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
