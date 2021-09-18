import requests, json, csv, re, argparse
from time import time

mac_addres_regex = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$' # from https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url",
        help="API base URL",
    )
    parser.add_argument(
        "input_csv",
        help="input csv file",
    )
    args = parser.parse_args()
    update_players(args.input_csv, args.url)


def update_players(input_file, base_url):
    with open(input_file, 'r') as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        for row in reader:
            mac_address = row[0]
            if is_valid_mac_address(mac_address):
                update_player(mac_address, base_url)
            else:
                print(f'\ninvalid MAC address {mac_address}, player will not be updated')


def is_valid_mac_address(macaddress):
    word = re.search(mac_addres_regex, macaddress)
    if not word: return False
    if word.span() != (0, 17): return False
    return True


def update_player(macaddress, base_url):
    url = f'{base_url}/profiles/clientId:{macaddress}'
    print(f'\nupdating player {macaddress}')
    send_put_request(url)


def send_put_request(url):
    client_id, token = get_auth()
    headers = {'x-client-id': client_id, 'x-authentication-token': token}
    response = None
    try:
        curr_time = round(time() * 1000)
        print(f'sending request, time: {curr_time}')
        response = requests.put(url, headers=headers, data=get_data())
        curr_time = round(time() * 1000)
        print(f'done sending request, time: {curr_time}')
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as err:
        print(f'http error: {err}')
        if response is not None and 'application/json' in response.headers.get('Content-Type'):
            print(response.json())
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