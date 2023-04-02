from flask import Flask, request, jsonify
from chatbot import Chatbot
import time

app = Flask(__name__)

@app.route("/getResponse")
def index():
    chatbot = Chatbot()
    response = chatbot.inputMessage("Who are you")
    return response

@app.route("/bot", methods=["POST"])
def response():
    query = dict(request.form)['message']
    chatbot = Chatbot()
    res = chatbot.inputMessage(query)
    currTime = time.ctime()
    return jsonify({"response" : res, "createdAt": currTime})