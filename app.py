from flask import Flask, jsonify, request
from crawler import get_lowest_price

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/lowest-price')
def lowest_price():
    id = request.args.get('id')
    price = get_lowest_price(id)
    return jsonify(price)

if __name__ == '__main__':
    app.run(debug=True)
