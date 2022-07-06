from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import datetime

import data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text())
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    address = db.Column(db.String(100))
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

db.drop_all()
db.create_all()


for user in data.USERS:
    db.session.add(User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    ))
    db.session.commit()

for order in data.ORDERS:
#    date_obj_start_list = order['start_date'].split("/")
#    date_obj_start = datetime.date(year=date_obj_start_list[2], month=date_obj_start_list[0],day=date_obj_start_list[1])
    month_start, day_start, year_start = [int(_) for _ in order['start_date'].split("/")]
    month_end, day_end, year_end = [int(_) for _ in order['end_date'].split("/")]
    db.session.add(Order(
        id=order['id'],
        name=order['name'] ,
        description=order['description'] ,
        start_date=datetime.date(year=year_start, month=month_start,day=day_start),
        end_date=datetime.date(year=year_end, month=month_end,day=day_end),
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    ))
    db.session.commit()