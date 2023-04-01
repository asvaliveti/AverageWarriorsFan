import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from chatbot import Chatbot

# Initialize Firebase
cred = credentials.Certificate('averagewarriorsfan-firebase-adminsdk-p2vje-a99b39ba2f.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://averagewarriorsfan-default-rtdb.firebaseio.com/'
})

# Get a reference to the database
ref = db.reference('chatbotConversations')

# Add data to the database
new_conversation_ref = ref.push()

# Listen for new messages
def on_message_added(message):
    chatbot = Chatbot()
    response = chatbot.inputMessage(message)
    new_conversation_ref.set({
        'message': response,
        'timestamp': {'.sv': 'timestamp'}  
    })

# get data from firebase front end
returned = ref.order_by_child("timestamp").limit_to_last(1).get()
print(returned)