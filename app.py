import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        res = []
        for user in User.query.all():
            res.append(user.to_dict())
        return jsonify(res)
        # return json.dumps([user.to_dict() for user in User.query.all()]) -//- то же самое, что предыдущие 4 строки

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'Delete'])
def one_user(user_id):
    if request.method == 'GET':
        try:
            return jsonify(User.query.get(user_id).to_dict())
        except:
            return "User is not found"





if __name__ == '__main__':
    app.run()
