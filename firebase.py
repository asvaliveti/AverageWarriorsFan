import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from chatbot import Chatbot

# Initialize Firebase
cred = credentials.Certificate('averagewarriorsfan-firebase-adminsdk-p2vje-a99b39ba2f.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://averagewarriorsfan-default-rtdb.firebaseio.com/'
})

input_ref = db.reference('inputMessages')
chatbot = Chatbot()
response = chatbot.inputMessage(input_ref.order_by_child("inputMessages").get()["message"])

output_ref = db.reference('outputMessages')
new_conversation_ref = output_ref.push()
new_conversation_ref.set({
    'message': response,
    'timestamp': {'.sv': 'timestamp'}  
})