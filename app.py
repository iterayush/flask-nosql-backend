from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

users_db = {}

# Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(list(users_db.values())), 200

# Add a new user
@app.route('/api/users', methods=['POST'])
def add_user():
    user_data = request.json
    user_id = str(uuid.uuid4()) 
    user_data['id'] = user_id
    users_db[user_id] = user_data  
    return jsonify({"message": "User added successfully!", "user": user_data}), 201

# Update a user
@app.route('/api/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id in users_db:
        user_data = request.json
        users_db[user_id].update(user_data)  
        return jsonify({"message": "User updated successfully!"}), 200
    return jsonify({"message": "User not found!"}), 404

# Delete a user
@app.route('/api/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users_db:
        del users_db[user_id] 
        return jsonify({"message": "User deleted successfully!"}), 200
    return jsonify({"message": "User not found!"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
