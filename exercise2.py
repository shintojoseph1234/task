from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace 'your_secret_key' with your actual pre-shared key
SECRET_KEY = 'your_secret_key'

def authenticate_request():
    """Middleware to authenticate requests."""
    if request.endpoint == 'authorize':
        return  # Skip authentication for the /authorize endpoint

    # Get the Authorization header from the request
    auth_header = request.headers.get('Authorization')

    # Check if the Authorization header is present and matches the pre-shared key
    if not auth_header or auth_header != f'Bearer {SECRET_KEY}':
        return jsonify({'error': 'Unauthorized'}), 401  # Unauthorized

@app.route('/ping')
def ping():
    return 'Pong!'

@app.route('/authorize')
def authorize():
    return 'Authorized!'

if __name__ == '__main__':
    app.before_request(authenticate_request)
    app.run(debug=True)

