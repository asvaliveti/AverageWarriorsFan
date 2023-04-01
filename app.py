from flask import Flask
from chatbot import Chatbot

app = Flask(__name__)

@app.route("/getResponse")
def index():
    chatbot = Chatbot()
    response = chatbot.inputMessage("Who are you")
    return response