from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = 'kushal_in999_key'

# MongoDB Connection
MONGO_URI = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['in999_database']
users_collection = db['users']

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login_process', methods=['POST'])
def login_process():
    data = request.json
    user = users_collection.find_one({"phone": data['phone'], "password": data['password']})
    if user:
        session['user_id'] = str(user['_id'])
        return jsonify({"message": "Success"}), 200
    return jsonify({"message": "Invalid Credentials"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if users_collection.find_one({"phone": data['phone']}):
        return jsonify({"message": "User exists"}), 400
    users_collection.insert_one(data)
    return jsonify({"message": "Registration Successful!"}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
