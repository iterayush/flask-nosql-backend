from flask import Flask, jsonify, request
import json, os, uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React

DATA_PATH = './data'

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)  # Create data directory if it doesn't exist

# Helper functions to read and write collections (JSON files)
def read_collection(collection_name):
    file_path = os.path.join(DATA_PATH, f'{collection_name}.json')
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def write_collection(collection_name, data):
    file_path = os.path.join(DATA_PATH, f'{collection_name}.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# API Routes for CRUD operations

# Create a new document (POST)
@app.route('/api/<collection>', methods=['POST'])
def create_document(collection):
    document = request.json
    document['_id'] = str(uuid.uuid4())  # Generate a unique ID for the document
    collection_data = read_collection(collection)
    collection_data.append(document)
    write_collection(collection, collection_data)
    return jsonify(document), 201

# Get all documents in a collection (GET)
@app.route('/api/<collection>', methods=['GET'])
def get_documents(collection):
    collection_data = read_collection(collection)
    return jsonify(collection_data), 200

# Get a document by ID (GET)
@app.route('/api/<collection>/<doc_id>', methods=['GET'])
def get_document_by_id(collection, doc_id):
    collection_data = read_collection(collection)
    document = next((doc for doc in collection_data if doc['_id'] == doc_id), None)
    if document:
        return jsonify(document), 200
    return jsonify({"message": "Document not found"}), 404

# Update a document by ID (PUT)
@app.route('/api/<collection>/<doc_id>', methods=['PUT'])
def update_document(collection, doc_id):
    collection_data = read_collection(collection)
    updated_data = request.json
    document = next((doc for doc in collection_data if doc['_id'] == doc_id), None)
    if document:
        document.update(updated_data)  # Update document with new data
        write_collection(collection, collection_data)
        return jsonify(document), 200
    return jsonify({"message": "Document not found"}), 404

# Delete a document by ID (DELETE)
@app.route('/api/<collection>/<doc_id>', methods=['DELETE'])
def delete_document(collection, doc_id):
    collection_data = read_collection(collection)
    updated_collection = [doc for doc in collection_data if doc['_id'] != doc_id]
    if len(updated_collection) != len(collection_data):
        write_collection(collection, updated_collection)
        return jsonify({"message": "Document deleted"}), 200
    return jsonify({"message": "Document not found"}), 404

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    # Assume you're generating or assigning a unique ID to the user
    new_user = {
        'id': generate_unique_id(),  # Example of ID generation
        'name': data['name'],
        'email': data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
