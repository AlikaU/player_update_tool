import flask, json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/profiles/clientId:a<client_id>', methods=['PUT'])
def update_player(client_id):
    with open("input/200.json") as f:
        return json.dumps(json.load(f))


def prepare_resp(status_code):
    with open(f"input/{status_code}.json") as f:
        return json.dumps(json.load(f)), status_code, {'Content-Type': 'application/json'}


# just to try all the possible responses, if mac address
# starts by b, c, d or e, we will return the different errors
@app.route('/profiles/clientId:b<client_id>', methods=['PUT'])
def update_player_401(client_id):
    return prepare_resp(401)


@app.route('/profiles/clientId:c<client_id>', methods=['PUT'])
def update_player_404(client_id):
    return prepare_resp(404)


@app.route('/profiles/clientId:d<client_id>', methods=['PUT'])
def update_player_409(client_id):
    return prepare_resp(409)


@app.route('/profiles/clientId:e<client_id>', methods=['PUT'])
def update_player_500(client_id):
    return prepare_resp(500)


app.run(threaded=True)
