from chatbot import Chatbot
class ReleaseInstance:
    chatbot = Chatbot()

    def getInstance():
        global chatbot
        return chatbot
    
if __name__ == "__main__":
    releaseInstance = ReleaseInstance