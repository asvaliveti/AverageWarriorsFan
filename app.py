from flask import Flask, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

# Define a POST endpoint for receiving messages from the frontend chatbot
@app.route('/message', methods=['POST'])
def handle_message():
    message = request.json['message']
    # Process the message and generate a response
    output = chatbot.inputMessage(message)
    response = {'response': output}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)