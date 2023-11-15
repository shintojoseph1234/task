from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

app = Flask(__name__)

# Replace 'sqlite:///example.db' with your actual database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['CACHE_TYPE'] = 'simple'  # You can choose a different caching type based on your needs
cache = Cache(app)
db = SQLAlchemy(app)

class KeyValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)

# Create the database tables
db.create_all()

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()

    if 'key' not in data or 'value' not in data:
        return jsonify({'error': 'Invalid request, both key and value are required'}), 400

    key = data['key']
    value = data['value']

    # Check if the key already exists in the database
    existing_key = KeyValue.query.filter_by(key=key).first()

    if existing_key:
        return jsonify({'error': 'Key already exists in the database'}), 400

    # Save the new key-value pair to the database
    new_key_value = KeyValue(key=key, value=value)
    db.session.add(new_key_value)
    db.session.commit()

    # Cache the newly saved data
    cache.set(key, value)

    return jsonify({'message': 'Data saved and cached successfully'}), 200

@app.route('/get', methods=['GET'])
def get():
    key = request.args.get('key')

    if not key:
        return jsonify({'error': 'Key parameter is required for the /get endpoint'}), 400

    # Try to get the data from cache
    cached_data = cache.get(key)

    if not cached_data:
        # If not in cache, fetch from the database
        key_value = KeyValue.query.filter_by(key=key).first()

        if not key_value:
            return jsonify({'error': 'Key not found'}), 404

        # Cache the data for future requests
        cache.set(key, key_value.value)

        return jsonify({'message': 'Data retrieved from the database', 'key': key, 'value': key_value.value})
    
    return jsonify({'message': 'Data retrieved from cache', 'key': key, 'value': cached_data}), 200

@app.route('/delete', methods=['DELETE'])
def delete():
    key = request.args.get('key')

    if not key:
        return jsonify({'error': 'Key parameter is required for the /delete endpoint'}), 400

    key_value = KeyValue.query.filter_by(key=key).first()

    if not key_value:
        return jsonify({'error': 'Key not found'}), 404

    db.session.delete(key_value)
    db.session.commit()

    return jsonify({'message': 'Data deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)

