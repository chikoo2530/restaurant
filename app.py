from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "fusionsecret"

# In-memory storage (for demonstration)
users = {}
reservations = {}

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users[username] = {'email': email, 'password': password}
        session['username'] = username
        return redirect('/reserve')
    return render_template('login.html')

# Reservation page
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        people = request.form['people']
        reservations[session['username']] = {'date': date, 'time': time, 'people': people}
        return redirect('/dashboard')
    return render_template('reserve.html')

# User dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    username = session['username']
    user = users[username]
    reservation = reservations.get(username)
    return render_template('dashboard.html', username=username, user=user, reservation=reservation)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
