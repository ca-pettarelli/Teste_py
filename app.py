# Caroline F. Pettarelli
# Python test

# run the following commands to up the api using Flask:

# pip install virtualenv
# virtualenv .venv
# source .venv/bin/activate
# pip install flask
# touch requirements.txt
# pyhton app.py



from flask import Flask, jsonify, request

app = Flask(__name__)


# exemples of rows
cards = [
    {
        'id': 1,
        'name': 'Rafael Marques', # name of the cardholder
        'card_number': 14256576576, # number of the card
        'val': '12-22' # data of card validity
    },
    {
        'id': 2,
        'name': 'Robert Hrosher',
        'card_number': 767697697697,
        'val': '02-21'
    },
    {
        'id': 3,
        'name': 'John Delare',
        'card_number': 87121878796,
        'val': '07-29'
    },
    {
        'id': 4,
        'name': 'John Doe',
        'card_number': 87987986767,
        'val': '07-29'
    }
]

# to get all cards
@app.route('/cards', methods=['GET'])
def home():
    return jsonify(cards), 200

# to get cards with the especific validity data 
@app.route('/cards/<string:val>', methods=['GET'])
def cards_per_val(val):
    cards_per_val = [dev for dev in cards if dev['val'] == val]
    return jsonify(cards_per_val), 200

# to get a especific card; need a ID insertion
@app.route('/cards/<int:id>', methods=['GET'])
def cards_per_id(id):
    for dev in cards:
        if dev['id'] == id:
            return jsonify(dev), 200

    return jsonify({'error': 'not found'}), 404


#to update the row; need a ID insertion
@app.route('/cards/<int:id>', methods=['PUT'])
def change_lang(id):
    for dev in cards:
        if dev['id'] == id:
            dev['lang'] = request.get_json().get('lang')

            return jsonify(dev), 200

    return jsonify({'error': 'dev not found'}), 404

# to post a row with informations of card
@app.route('/cards', methods=['POST'])
def save_dev():
    data = request.get_json()
    cards.append(data)
    
    return jsonify(data), 201

# to delete a row; need a ID insertion
@app.route('/cards/<int:id>', methods=['DELETE'])
def remove_dev(id):
    index = id - 1
    del cards[index]

    return jsonify({'message': 'Dev is no longer alive'}), 200


if __name__ == '__main__':
    app.run(debug=True)


# http://127.0.0.1:5000/cards/12-22  ---> pesquisar data de validade
# http://127.0.0.1:5000/cards ----------> ver dados dos clientes/cartoes
# http://127.0.0.1:5000/cards/1 --------> pesquisar pelo id