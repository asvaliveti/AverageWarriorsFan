import json
import string
import random 
import nltk
import numpy as np
import json
from nltk.stem import WordNetLemmatizer 
import tensorflow as tf
from tweets import Tweets
from stats import Stats
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import Dense, Dropout
nltk.download("punkt")
nltk.download("wordnet")


class Chatbot:
  words = []
  lemmatizer = WordNetLemmatizer()
  model = Sequential()
  classes = []
  data = {}


  def __init__(self):
    global words
    global lemmatizer
    global model
  
    with open('intents.json') as json_file:
        self.data = json.load(json_file)

    # initializing lemmatizer to get stem of words
    # Each list to create
    doc_X = []
    doc_Y = []
    # Loop through all the intents
    # tokenize each pattern and append tokens to words, the patterns and
    # the associated tag to their associated list
    for intent in self.data["intents"]:
        for pattern in intent["patterns"]:
            tokens = nltk.word_tokenize(pattern)
            self.words.extend(tokens)
            doc_X.append(pattern)
            doc_Y.append(intent["tag"])
        
        # add the tag to the classes if it's not there already 
        if intent["tag"] not in self.classes:
            self.classes.append(intent["tag"])
    # lemmatize all the words in the vocab and convert them to lowercase
    # if the words don't appear in punctuation
    self.words = [self.lemmatizer.lemmatize(word.lower()) for word in self.words if word not in string.punctuation]
    # sorting the vocab and classes in alphabetical order and taking the # set to ensure no duplicates occur
    self.words = sorted(set(self.words))
    self.classes = sorted(set(self.classes))

    # list for training data
    training = []
    out_empty = [0] * len(self.classes)
    # creating the bag of words model
    for idx, doc in enumerate(doc_X):
        bow = []
        text = self.lemmatizer.lemmatize(doc.lower())
        for word in self.words:
            bow.append(1) if word in text else bow.append(0)
        # mark the index of class that the current pattern is associated
        # to
        output_row = list(out_empty)
        output_row[self.classes.index(doc_Y[idx])] = 1
        # add the one hot encoded BoW and associated classes to training 
        training.append([bow, output_row])
    # shuffle the data and convert it to an array
    random.shuffle(training)
    training = np.array(training, dtype=object)
    # split the features and target labels
    train_X = np.array(list(training[:, 0]))
    train_y = np.array(list(training[:, 1]))

    # defining some parameters
    input_shape = (len(train_X[0]),)
    output_shape = len(train_y[0])
    epochs = 200
    # the deep learning model
    self.model.add(Dense(128, input_shape=input_shape, activation="relu"))
    self.model.add(Dropout(0.5))
    self.model.add(Dense(64, activation="relu"))
    self.model.add(Dropout(0.3))
    self.model.add(Dense(output_shape, activation = "softmax"))
    adam = tf.keras.optimizers.legacy.Adam(learning_rate=0.01, decay=1e-6)
    self.model.compile(loss='categorical_crossentropy',
                  optimizer=adam,
                  metrics=["accuracy"])
    print(self.model.summary())
    self.model.fit(x=train_X, y=train_y, epochs=200, verbose=1)

  def clean_text(self, text): 
    global lemmatizer
    tokens = nltk.word_tokenize(text)
    tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
    return tokens

  def bag_of_words(self, text, vocab): 
    tokens = self.clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens: 
      for idx, word in enumerate(vocab):
        if word == w: 
          bow[idx] = 1
    return np.array(bow)

  def pred_class(self, text, vocab, labels): 
    bow = self.bag_of_words(text, vocab)
    result = self.model.predict(np.array([bow]))[0]
    thresh = 0.2
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
      return_list.append(labels[r[0]])
    return return_list

  def get_response(self, intents_list, intents_json): 
    tag = intents_list[0]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents: 
      if i["tag"] == tag:
        if i["tag"] == "twitter":
          result = Tweets.getWarriorsTweet()
        elif i["tag"] == "todays_game":
          result = Stats.getMostRecentGameSummary()
        else: 
          result = random.choice(i["responses"])
        break
    return result

  # running the chatbot
  def inputMessage(self, message):
      global words
      global classes
      global data
      intents = self.pred_class(message, self.words, self.classes)
      result = self.get_response(intents, self.data)
      return result