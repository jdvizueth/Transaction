from datetime import datetime
import json

import db
from flask import Flask
from flask import request

DB = db.DatabaseDriver()

app = Flask(__name__)

# generalized response formats
def success_response(body, code=200):
    return json.dumps(body), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/")


# your routes here

@app.route("/users/")
def get_users():
    """
    Enpoint for getting all users
    """
    return json.dumps({"users": DB.get_all_users()}), 200

@app.route("/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance", 0)
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "name or username is not provided"}), 400
    return json.dumps(user), 201

@app.route("/users/<int:user_id>/")
def get_user(user_id):
    if (DB.get_user_by_id(user_id) != None):
        return DB.get_user_by_id(user_id)
    else:
        return failure_response("user not found", 404)
@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Setting up the endpoint for deleting a user from a database
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200

@app.route("/users/", methods=["POST"])
def send_money():
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")

@app.route("/transactions/", methods = ["POST"])
def create_exchange():
    """
    Endpoint for creating a exchange for a exchange with id user_id
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    message = body.get("message")
    accepted = body.get("accepted")



    user = DB.get_user_by_id(sender_id)
    receiver = DB.get_user_by_id(receiver_id)
    if user is None:
        return failure_response("User not found!")

    if receiver is None:
        return failure_response("User not found!")

    exchange_id = DB.insert_exchange(sender_id, receiver_id, amount, message, accepted)
    exchange = DB.get_exchange_by_id(exchange_id)

    if exchange is None:
        return failure_response("Could not create exchange", 400)
    return success_response(exchange, 201)

@app.route("/transactions/<int:exchange_id>/", methods = ["POST"])
def accept_or_deny(exchange_id):
    """
    declares if an exchange has been accepted
    """
    body = json.loads(request.data)
    response = body.get("accepted")

    exchange = DB.get_exchange_by_id(exchange_id)
    if (exchange['accepted'] == None):
        if (response):
            if (DB.get_user_by_id(exchange['sender_id'])['balance'] > exchange['amount']):
                DB.update_exchange_by_id(exchange_id, True)
                exchange['accepted'] = True
                return exchange, 200
            else:
                return failure_response("You are broke", 403)
        else: 
            DB.update_exchange_by_id(exchange_id, False)
            exchange['accepted'] = False
            return exchange, 200
    else: 
        return failure_response("Transaction has already been accepted/denied")
    DB.conn.commit()
            
        
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
