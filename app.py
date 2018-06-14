from flask import Flask, jsonify, request, render_template, json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from crawler import get_item
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))
    price = db.Column(db.String(100))

    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price

    def __repr__(self):
        return json.dumps(dict(
                name = self.name,
                price = self.price,
                id = self.item_id
            )
        )

@app.route('/')
def home():
    items = Item.query.paginate().items
    return render_template('home.html', items=items)

@app.route('/lowest-price')
def lowest_price():
    item_id = request.args.get('id')
    item = get_item(item_id)
    return jsonify(dict(price = item.get('price', '')))

@app.route('/add-item', methods=['POST'])
def add_item():
    item_id = request.form.get('item', '')
    item = get_item(item_id)
    price = item.get('price', '')
    name = item.get('name', '')
    dbcreate = Item(item_id, name, price) 
    db.session.add(dbcreate)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
