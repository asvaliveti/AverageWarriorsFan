from flask import Flask, request, jsonify, make_response
from chatbot import Chatbot
import json

app = Flask(__name__)
chatbot = Chatbot()

# Define a POST endpoint for receiving messages from the frontend chatbot
@app.route('/message', methods=['POST'])
def handle_message():
    message = request.json['message']
    # Process the message and generate a response
    output = chatbot.inputMessage(message)
    response = make_response(jsonify({'response': output}))
    response.headers["Access-Control-Allow-Origin"] = '*'
    return response

if __name__ == '__main__':
    app.run(debug=True)