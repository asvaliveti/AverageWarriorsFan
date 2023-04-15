from flask import Flask, request, jsonify, make_response
from chatbot import Chatbot
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
chatbot = Chatbot()
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}, "methods": ["POST"]})

# Define a POST endpoint for receiving messages from the frontend chatbot
@app.route('/message', methods=['POST'])
@cross_origin()
def handle_message():
    message = request.json['message']
    # Process the message and generate a response
    output = chatbot.inputMessage(message)
    response = make_response(jsonify({'response': output}))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)