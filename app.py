from flask import Flask, request, jsonify
from release import ReleaseInstance

app = Flask(__name__)

# Define a POST endpoint for receiving messages from the frontend chatbot
@app.route('/message', methods=['POST'])
def handle_message():
    message = request.json['message']
    # Process the message and generate a response
    output = ReleaseInstance.getInstance().inputMessage(message)
    response = {'response': output}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)