from flask import Flask, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://database:27017/")
mydb = client['idb']
collection = mydb['emp']

@app.route('/')
def home():
    return "<h1>Welcome to the Employee API</h1>"

def serialize_doc(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc['_id'] = str(doc['_id'])
    if 'Department' in doc and 'department' not in doc:
        doc['department'] = doc.pop('Department')
    return doc

@app.errorhandler(InvalidId)
def invalid_object_id(error):
    return jsonify({"error": "Invalid ID format"}), 400

@app.route('/emps', methods=['GET'])
def get_all_emps():
    try:
        data = []
        for i in collection.find():
            data.append(serialize_doc(i))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emps/<name>', methods=['GET'])
def get_emp(name):
    try:
        emp = collection.find_one({"name": name})
        if emp:
            return jsonify(serialize_doc(emp))
        else:
            return jsonify({"error": "User not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid user ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emps', methods=['POST'])
def create_emps():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
        
        required_fields = ["name", "age", "email", "Department"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        result = collection.insert_one(data)
        new_emp = collection.find_one({"_id": result.inserted_id})
        
        return {
            "_id": str(new_emp['_id']), "name": new_emp['name'], "age": new_emp['age'], "email": new_emp['email'], "Department": new_emp['Department']
        }, 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)