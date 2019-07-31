import json
import datetime
from functools import wraps
from flask import jsonify, request, Response
from settings import app
from models import Person, User
import jwt


residential = Person.get_all_person()
DEFAULT_PAGE_LIMIT = 3
app.config['SECRET_KEY'] = 'huyxdong'


# Make a token
@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username, password = str(request_data['username']), str(
        request_data['password'])

    match = User.username_password_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date},
                           app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({"error": "need a valid token"}), 401
    return wrapper


@app.route('/residential')
def get_residential():
    return jsonify({"residential": residential})


# Get a specific person in a list of residential
@app.route('/residential/<int:passport>')
def get_person(passport):
    return_value = Person.get_person(passport)
    return jsonify(return_value)


def validPerson(personObject):
    return ('name' in personObject and 'age' in personObject)


# Add a person to a list of residential
@app.route('/residential', methods=['POST'])
@token_required
def add_person():
    request_data = request.get_json()
    if validPerson(request_data):
        Person.add_person(
            request_data['name'], request_data['age'], request_data['passport'])
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/residential/' + \
            str(request_data['name'])
        return response
    else:
        errorMsg = {
            "error": "invalid content",
            "helpString": "please insert similar {'name': 'evil', 'age': 28, 'passport': 18677484}"
        }
        response = Response(json.dumps(errorMsg), status=400,
                            mimetype='application/json')
        return response


# Replace a person in a list of residential
@app.route('/residential/<int:passport>', methods=['PUT'])
@token_required
def replace_person(passport):
    request_data = request.get_json()
    if not validPerson(request_data):
        errorMsg = {
            "error": "invalid content",
            "helpString": "please insert similar {'name': 'evil', 'age': 28, 'passport': 18677484}"
        }
        response = Response(json.dumps(errorMsg), status=400,
                            mimetype='application/json')
    Person.replace_person(passport, request_data['name'], request_data['age'])
    response = Response('', status=204)
    return response


# Update a person in a list of residential
@app.route('/residential/<int:passport>', methods=['PATCH'])
@token_required
def update_person(passport):
    request_data = request.get_json()
    if 'name' in request_data:
        Person.update_person_name(passport, request_data['name'])
    if 'age' in request_data:
        Person.update_person_age(passport, request_data['age'])
    response = Response('', status=204)
    response.headers['Location'] = '/residential/' + str(passport)
    return response


# Delete a person in a list of residential
@app.route('/residential/<int:passport>', methods=['DELETE'])
@token_required
def delete_person(passport):
    if Person.delete_person(passport):
        response = Response('', 204)
        return response
    errorMsg = {
        "error": "This person doesn't exist!"
    }
    response = Response(json.dumps(errorMsg), status=400,
                        mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5005)
