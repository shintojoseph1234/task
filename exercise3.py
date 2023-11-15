from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace 'sqlite:///example.db' with your actual database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
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

    key_value = KeyValue(key=data['key'], value=data['value'])
    db.session.add(key_value)
    db.session.commit()

    return jsonify({'message': 'Data saved successfully'})

@app.route('/get', methods=['GET'])
def get():
    key = request.args.get('key')

    if not key:
        return jsonify({'error': 'Key parameter is required for the /get endpoint'}), 400

    key_value = KeyValue.query.filter_by(key=key).first()

    if not key_value:
        return jsonify({'error': 'Key not found'}), 404

    return jsonify({'key': key_value.key, 'value': key_value.value})

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

