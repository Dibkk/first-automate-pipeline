from flask import Flask, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
mydb = client['idb']
collection = mydb['emp']

@app.errorhandler(InvalidId)
def invalid_object_id(error):
    return jsonify({"error": "Invalid ID format"}), 400

@app.route('/emps', methods=['GET'])
def get_all_users():
    try:
        data = []
        for i in collection.find():
            data.append({"_id":str(i['_id']), 'name':i['name'], "age":i['age'], "email":i['email'], "Department":i['Department']})
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emps/<emp_id>', methods=['GET'])
def get_emp(emp_id):
    try:
        emp = collection.find_one({"_id": ObjectId(emp_id)})
        if emp:
            return jsonify(emp)
        else:
            return jsonify({"error": "User not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid user ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emps', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        required_fields = ["name", "age", "email", "department"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        existing_emp = collection.find_one({"_id": data['_id']})
        if existing_emp:
            return jsonify({"error": "You are already exists"}), 409
        
        result = collection.insert_one(data)
        
        # new_emp = collection.find_one({"_id": result.inserted_id})
        return jsonify({
            "message": "Employee created successfully",
            "new employee" : data
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)