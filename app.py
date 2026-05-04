from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Connection
MONGO_URI = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['in999_database']
users_collection = db['users']

@app.route('/')
def home():
    # Ye line 'Not Found' fix karegi
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    invite_code = data.get('invite_code')

    if not phone or not password:
        return jsonify({"message": "Details bhariye!"}), 400
    
    if users_collection.find_one({"phone": phone}):
        return jsonify({"message": "User pehle se hai!"}), 400
    
    users_collection.insert_one({
        "phone": phone, 
        "password": password, 
        "invite_code": invite_code,
        "balance": 0
    })
    return jsonify({"message": "Registration Successful!"}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
