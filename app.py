from flask import Flask, request, jsonify, make_response
from chatbot import Chatbot
import json

app = Flask(__name__)
chatbot = Chatbot()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Define a POST endpoint for receiving messages from the frontend chatbot
@app.route('/message', methods=['POST'])
def handle_message():
    print("called function")
    message = request.json['message']
    print("message: " + message)
    # Process the message and generate a response
    output = chatbot.inputMessage(message)
    print("output: " + output)
    response = make_response(jsonify({'response': output}))
    print("response: " + response)
    return response


@app.route('/test', methods=['POST'])
def test_message():
    return chatbot.testSuccess()

if __name__ == '__main__':
    app.run(debug=True)