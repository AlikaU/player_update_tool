# player_update_tool
This tool automates the update of music players by using an API. The input is a .csv file containing, at the very minimum, MAC addresses of players to update, always in the first column. The first line of the csv is expected to contain column names.

Example of a .csv file:
```mac_addresses, id1, id2, id3
a1:bb:cc:dd:ee:ff, 1, 2, 3
a2:bb:cc:dd:ee:ff, 1, 2, 3
a3:bb:cc:dd:ee:ff, 1, 2, 3
a4:bb:cc:dd:ee:ff, 1, 2, 3
```

##Prerequisites:
python 3.9

##Installation
```pip install -r requirements.txt```

##Usage
```python update_player.py <API base URL> <input csv>```

You can optionally specify the number of workers (default is 1):
```python update_player.py <API base URL> <input csv> -w <num_workers>```

##To run unit tests:
In command line, run:
```pytest```

##To run on a minimal test server with a test input file:
Run the server:
```python test/server.py```
In another command line window, run the tool:
```python update_player.py http://localhost:5000 input/input.csv -w 1```
*Note that some requests will fail because the flask server doesn't handle a lot of concurrent requests.*
*Note that to test error handling behaviour, the server will return errors for requests for MAC addresses starting with letters 'b', 'c', 'd' or 'e'.*

# Technical decisions
The tool is written in Python, since it is a cross-platform language and allows for quick prototyping. For unit testing, pytest and the responses library were used to mock the API requests. To test the full program, a minimal Flask server was used. Since we expect to update thousands of players and API calls can get slow, multi-threading is used to speed it up.

##Future work
* Implement authentication with a token that expires
* For the API requests, set timeouts, and retry after connection errors