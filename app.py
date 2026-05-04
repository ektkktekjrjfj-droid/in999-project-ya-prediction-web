from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'in999_secret_key'

# Yeh route check karega ki user logged in hai ya nahi
@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    # Simple Logic: Aap yahan apna koi bhi password rakh sakte hain
    if len(phone) >= 10 and password == "123456": 
        session['user'] = phone
        return redirect(url_for('dashboard'))
    else:
        return "Invalid Credentials! Please try again."

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
