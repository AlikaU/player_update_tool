import requests, json

endpoint = 'http://someendpoint.com'

def main():
    update_player()


def update_player(macaddress):
    url = f'{endpoint}/profiles/clientId:{macaddress}'
    send_put_request(url)


def send_put_request(url):
    client_id, token = get_auth()
    headers = {'x-client-id': client_id, 'x-authentication-token': token}
    try:
        response = requests.put(url, headers=headers, data=get_data())
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as err:
        print(f'http error: {err}')
    except requests.exceptions.ConnectionError as err:
        print(f'connection error: {err}')
    except requests.exceptions.RequestException as err:
        print(f'error while sending request: {err}')
    return False


def get_auth():
    return 'some_client_id', 'some_auth_token'


def get_data():
    with open("example_data.json") as f:
        return json.load(f)



if __name__ == "__main__":
    main()