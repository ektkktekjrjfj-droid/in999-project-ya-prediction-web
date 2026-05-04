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
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    
    if users_collection.find_one({"phone": phone}):
        return jsonify({"message": "User already exists!"}), 400
    
    users_collection.insert_one({
        "phone": phone, 
        "password": password, 
        "balance": 0
    })
    return jsonify({"message": "Success! Account Created."}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
