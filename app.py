from flask import Flask, render_template, request, redirect, url_for, session
import requests
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)  # Changed _name to _name_
app.secret_key = "b75375b19333a8b301121ad2e51ca363d89267762ad5c66a560b9debd61b6cda"  # Change this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Portfolio model
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crypto_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_crypto_price(crypto_name):
    params = {"ids": crypto_name, "vs_currencies": "usd"}
    response = requests.get(COINGECKO_API_URL, params=params)
    data = response.json()
    return data.get(crypto_name, {}).get("usd", "N/A")

# Define allocation percentages for each cryptocurrency
allocation = {
    "Bitcoin (BTC)": 40,   # 40%
    "Ethereum (ETH)": 20,  # 20%
    "BNB": 10,             # 10%
    "Solana (SOL)": 10,    # 10%
    "Polygon (MATIC)": 5,  # 5%
    "AI Projects": 5,      # 5%
    "DeFi Projects": 5,    # 5%
    "High-Risk Investments": 5  # 5%
}

# Add a mock function to simulate future worth prediction (for demonstration)
def get_future_worth_crypto():
    # In a real-world application, you would use some kind of prediction model
    # For now, we'll just pick a random crypto based on some mock logic
    future_worth = {
        "Bitcoin (BTC)": "Highly probable",
        "Ethereum (ETH)": "Moderate probability",
        "BNB": "Low probability",
        "Solana (SOL)": "Moderate probability",
        "Polygon (MATIC)": "Moderate probability",
        "AI Projects": "High probability",
        "DeFi Projects": "High probability",
        "High-Risk Investments": "Unpredictable"
    }
    return future_worth


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for('login'))

    user_id = session["user_id"]
    portfolio = Portfolio.query.filter_by(user_id=user_id).all()

    future_worth_crypto = get_future_worth_crypto()  # Fetch future worth predictions


    # Calculate the real-time price and value of the portfolio items
    portfolio_data = []
    for entry in portfolio:
        price = get_crypto_price(entry.crypto_name.lower())  # Get real-time price
        value = entry.quantity * price if price != "N/A" else "N/A"
        portfolio_data.append({
            "crypto_name": entry.crypto_name,
            "quantity": entry.quantity,
            "price": price,
            "value": value
        })

    investment = {}
    if request.method == "POST":
        if "amount" in request.form:  # Check if the 'amount' field is present
            try:
                amount = float(request.form["amount"])  # Get user input
                crypto_name = request.form["crypto_name"]
                percent = allocation.get(crypto_name, 0)  # Get the allocation percentage for the selected crypto
                investment[crypto_name] = round((percent / 100) * amount, 2)  # Calculate the allocated amount
            except Exception as e:
                print(f"Error: {e}")
                investment = {}

        # Handle adding new crypto to the portfolio
        if "add_crypto" in request.form:
            try:
                crypto_name_add = request.form['crypto_name_add']  # Crypto name for addition
                quantity_add = float(request.form['quantity_add'])  # Quantity to add
                new_entry = Portfolio(user_id=user_id, crypto_name=crypto_name_add, quantity=quantity_add)
                db.session.add(new_entry)
                db.session.commit()
            except Exception as e:
                print(f"Error: {e}")
                return "There was an error adding the crypto to your portfolio."

    

    # Pass 'allocation' dictionary to the template so the dropdown can be populated
    return render_template('dashboard.html', portfolio=portfolio_data, investment=investment, allocation=allocation, future_worth_crypto=future_worth_crypto
)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            return "User already exists!"
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for('dashboard'))
        return "Invalid credentials!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect(url_for('home'))

@app.route('/add_crypto', methods=['POST'])
def add_crypto():
    if "user_id" not in session:
        return redirect(url_for('login'))

    crypto_name = request.form['crypto_name']
    quantity = float(request.form['quantity'])
    user_id = session["user_id"]

    new_entry = Portfolio(user_id=user_id, crypto_name=crypto_name, quantity=quantity)
    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for('dashboard'))



if __name__ == "__main__":  # Changed _name to _name_
    app.run(debug=True)