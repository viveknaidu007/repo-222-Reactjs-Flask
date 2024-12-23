from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with your own secret key
jwt = JWTManager(app)
CORS(app)  # To allow cross-origin requests from React frontend

# MongoDB connection
client = MongoClient('')  #mongo db uri
db = client['vivek_data']
users_collection = db['vivek']

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': 'Missing username or password'}), 400

    # Check if user already exists
    if users_collection.find_one({'username': username}):
        return jsonify({'msg': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    users_collection.insert_one({'username': username, 'password': hashed_password})

    return jsonify({'msg': 'User registered successfully'}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'msg': 'Invalid username or password'}), 401

    # Create JWT token
    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

# Protected route example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="This is a protected route!")

if __name__ == '__main__':
    app.run(debug=True)
