import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        res = []
        for user in User.query.all():
            res.append(user.to_dict())
        return jsonify(res)
        # return jsonify([user.to_dict() for user in User.query.all()]) -//- то же самое, что предыдущие 4 строки
    if request.method == 'POST':
        try:
            user = json.loads(request.data)
            new_user_object = User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            )
            db.session.add(new_user_object)
            db.session.commit()
            db.session.close()
            return "The user is added to DataBase", 200
        except:
            return "The user is not added to DataBase"


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == 'GET':
        try:
            return jsonify(User.query.get(user_id).to_dict())
        except:
            return "User is not found", 404

    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "User is not found", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f"User`s {user_id} data is updated", 200
    elif request.method == 'DELETE':
        try:
            user = db.session.query(User).get(user_id)
            db.session.delete(user)
            db.session.commit()
            db.session.close()
            return f"User {user_id} is deleted", 200
        except:
            return f"User`s {user_id} data is not deleted, user is not found", 404


@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        return jsonify([order.to_dict() for order in Order.query.all()])
    if request.method == 'POST':
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = [int(_) for _ in order['start_date'].split("/")]
            month_end, day_end, year_end = [int(_) for _ in order['end_date'].split("/")]
            new_order_object = Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                end_date=datetime.date(year=year_end, month=month_end, day=day_end),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id']
            )
            db.session.add(new_order_object)
            db.session.commit()
            db.session.close()
            return "The order is added to DataBase", 200
        except:
            return "The order is not added to DataBase"


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        try:
            return jsonify(Order.query.get(order_id).to_dict())
        except:
            return "Order is not found"
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Order is not found", 404
        #month_start, day_start, year_start = [int(_) for _ in order['start_date'].split("/")]
        #month_end, day_end, year_end = [int(_) for _ in order['end_date'].split("/")]
        order.id = order_data['id']
        order.name = order_data['name']
        #order.start_date = datetime.date(year=year_start, month=month_start, day=day_start)
        #order.end_date = datetime.date(year=year_end, month=month_end, day=day_end)
        order.description = order_data['description']
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Order {order_id} data is updated", 200
    elif request.method == 'DELETE':
        try:
            order = db.session.query(Order).get(order_id)
            db.session.delete(order)
            db.session.commit()
            db.session.close()
            return f"Order {order_id} is deleted", 200
        except:
            return f"Order {order_id} is not deleted, order is not found", 404


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        return jsonify([offer.to_dict() for offer in Offer.query.all()])

    if request.method == 'POST':
        try:
            offer = json.loads(request.data)
            new_offer_object = Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id']
            )
            db.session.add(new_offer_object)
            db.session.commit()
            db.session.close()
            return "The offer is added to DataBase", 200
        except:
            return "The offer is not added to DataBase"


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    if request.method == 'GET':
        try:
            return jsonify(Offer.query.get(offer_id).to_dict())
        except:
            return "Offer is not found"

    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if offer is None:
            return "Offer is not found", 404
        offer.id = offer_data['id']
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return f"Offer`s {offer_id} data is updated", 200
    elif request.method == 'DELETE':
        try:
            offer = db.session.query(Offer).get(offer_id)
            db.session.delete(offer)
            db.session.commit()
            db.session.close()
            return f"Offer {offer_id} is deleted", 200
        except:
            return f"Offer`s {offer_id} data is not deleted, offer is not found", 404



if __name__ == '__main__':
    app.run()
