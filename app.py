from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from noren_api import NorenAPI
import os

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Store API instances
api_instances = {}

def get_api():
    session_id = request.headers.get('X-Session-ID', 'default')
    if session_id not in api_instances:
        api_instances[session_id] = NorenAPI()
    return api_instances[session_id]

@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('frontend', 'dashboard.html')

@app.route('/api/login-url', methods=['GET'])
def get_login_url():
    api = get_api()
    result = api.get_login_url()
    return jsonify(result)

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    auth_code = data.get('auth_code')
    api = get_api()
    result = api.get_access_token(auth_code)
    return jsonify(result)

@app.route('/api/quotes', methods=['POST'])
def get_quotes():
    data = request.json
    api = get_api()
    result = api.get_quotes(data.get('exchange'), data.get('tradingsymbol'))
    return jsonify(result)

@app.route('/api/search', methods=['POST'])
def search_scrip():
    data = request.json
    api = get_api()
    result = api.search_scrip(data.get('search_text'))
    return jsonify(result)

@app.route('/api/place-order', methods=['POST'])
def place_order():
    data = request.json
    api = get_api()
    result = api.place_order(data)
    return jsonify(result)

@app.route('/api/modify-order', methods=['POST'])
def modify_order():
    data = request.json
    api = get_api()
    result = api.modify_order(data)
    return jsonify(result)

@app.route('/api/cancel-order', methods=['POST'])
def cancel_order():
    data = request.json
    api = get_api()
    result = api.cancel_order(data.get('order_no'))
    return jsonify(result)

@app.route('/api/order-book', methods=['GET'])
def get_order_book():
    api = get_api()
    result = api.get_order_book()
    return jsonify(result)

@app.route('/api/trade-book', methods=['GET'])
def get_trade_book():
    api = get_api()
    result = api.get_trade_book()
    return jsonify(result)

@app.route('/api/holdings', methods=['GET'])
def get_holdings():
    api = get_api()
    result = api.get_holdings()
    return jsonify(result)

@app.route('/api/positions', methods=['GET'])
def get_positions():
    api = get_api()
    result = api.get_positions()
    return jsonify(result)

@app.route('/api/limits', methods=['GET'])
def get_limits():
    api = get_api()
    result = api.get_limits()
    return jsonify(result)

@app.route('/api/logout', methods=['POST'])
def logout():
    api = get_api()
    result = api.logout()
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
