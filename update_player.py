import requests, json, csv, re

endpoint = 'http://someendpoint.com'
mac_addres_regex = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$' # from https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address

def main():
    try:
        update_players('input.csv')
    except Exception:
        print(f'error while reading input file {input_file}, make sure it is a valid csv file')


def update_players(input_file):
    with open(input_file, 'r') as f:
        reader = csv.reader(f, skipinitialspace=True)
        for row in reader:
            mac_address = row[0]
            if is_valid_mac_address(mac_address):
                update_player(mac_address)


def is_valid_mac_address(macaddress):
    word = re.search(mac_addres_regex, macaddress)
    if not word: return False
    if word.span() != (0, 17): return False
    return True


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