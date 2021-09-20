import requests, json, csv, re, argparse, os
from concurrent.futures import ThreadPoolExecutor, as_completed

mac_addres_regex = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$' # from https://stackoverflow.com/questions/4260467/what-is-a-regular-expression-for-a-mac-address

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='API base URL')
    parser.add_argument('input_csv', help='input csv file', type=valid_csv)
    parser.add_argument('-w', '--max_workers', help='number of workers (threads)', default=1, type=int)
    args = parser.parse_args()
    if update_players(args.input_csv, args.url, args.max_workers):
        print('\nAll players updated successfully!')
    else: print('\nOne or more players could not be updated. Check the error messages above.')


def valid_csv(input_csv):
    if not os.path.exists(input_csv) or \
        os.stat(input_csv).st_size == 0 or \
        not input_csv.endswith(".csv"):
        raise argparse.ArgumentTypeError(f'Invalid input file {input_csv}')
    return input_csv


def update_players(input_file, base_url, num_workers):
    threads = []
    success = True
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        with open(input_file, 'r') as f:
            reader = csv.reader(f, skipinitialspace=True)
            next(reader, None)
            for row in reader:
                mac_address = row[0]
                threads.append(executor.submit(update_player, mac_address, base_url))

            for task in as_completed(threads):
                success = success and task.result()
    return success


def update_player(macaddress, base_url):
    if not is_valid_mac_address(macaddress): return False
    url = f'{base_url}/profiles/clientId:{macaddress}'
    print(f'\nupdating player {macaddress}')
    return send_put_request(url)


def is_valid_mac_address(macaddress):
    word = re.search(mac_addres_regex, macaddress)
    if not word or word.span() != (0, 17):
        print(f'\ninvalid MAC address {macaddress}, player will not be updated')
        return False
    return True


def send_put_request(url):
    client_id, token = get_auth()
    headers = {'x-client-id': client_id, 'x-authentication-token': token}
    response = None
    try:
        response = requests.put(url, headers=headers, data=get_data())
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as err:
        print(f'http error: {err}')
        if response is not None and 'application/json' in response.headers.get('Content-Type'):
            print(response.json())
    except requests.exceptions.RequestException as err:
        print(f'error while sending request to {url}: {err}')
    return False


def get_auth():
    return 'some_client_id', 'some_auth_token'


def get_data():
    with open('example_data.json') as f:
        return json.load(f)


if __name__ == '__main__':
    main()