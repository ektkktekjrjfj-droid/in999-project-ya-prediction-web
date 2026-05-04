from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# App setup mein secret key add karein (Sessions ke liye zaroori hai)
app.secret_key = 'kushal_secret_key' 

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login_process', methods=['POST'])
def login_process():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    
    # Database mein check karein
    user = users_collection.find_one({"phone": phone, "password": password})
    
    if user:
        session['user_id'] = str(user['_id']) # Session save karein
        return jsonify({"message": "Success"}), 200
    else:
        return jsonify({"message": "Invalid Phone or Password"}), 401
