import numpy as np
import pickle
import json

import nltk
from nltk.stem import PorterStemmer
import torch
import torch.nn as nn

import RAKE
Rake = RAKE.Rake(RAKE.SmartStopList())

import warnings
warnings.filterwarnings('ignore')

from flask import Flask, render_template, url_for, request, jsonify

##############################################

#install these packages when you run the app for the first time

#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('omw')

##############################################

#Disease Predictor (see Disease Notebook)

#this is the where the Disease predictor and the list of all possible symptoms (for bag of symptoms) comes from   
with open('static/assets/files/fitted_model.pickle', 'rb') as modelFile:
    model_final = pickle.load(modelFile)
    
with open('static/assets/files/all_symptoms.pickle', 'rb') as symptomsFile:
    list_of_symptoms = pickle.load(symptomsFile)
    
##############################################

#Symptoms Predictor (see Symptom Notebook)

#this is where the fitted Symptom Predictor comes from
data_file='static/assets/files/data.pth'

symptom_model = torch.load(data_file)
model_state = symptom_model['model_state']
word_list = symptom_model['word_list']
tags = symptom_model['tags']
    
##############################################

#Neural Network for Symptom Predictor (see Symptom Notebook)

class Net(nn.Module):
    def __init__(self, number_words, hidden_size, number_tags):
        super(Net, self).__init__()
        self.start = nn.Linear(number_words, hidden_size) #input layer
        self.h1 = nn.Linear(hidden_size, hidden_size) #hidden layer
        self.end = nn.Linear(hidden_size, number_tags) #output layer
        
        self.relu = nn.ReLU() 
        
    def forward(self, x):
        x = self.relu(self.start(x))
        x = self.relu(self.h1(x))
        x = self.end(x)
        return x

#active model for website
model = Net(number_words=len(word_list), number_tags=len(tags), hidden_size=8).to(torch.device('cpu'))
model.load_state_dict(model_state)
model.eval()


##############################################

##### helping functions for processing the user input #####

#(see Symptom Notebook)
def word_to_vect(tokenized_sentence, all_words):
    lemmatized_sentence = [PorterStemmer().stem(w.lower()) for w in tokenized_sentence]

    vect=[]
    
    for word in all_words:
        if word in lemmatized_sentence:
            vect.append(1)
        else: 
            vect.append(0)

    return np.asarray(vect, dtype=np.float32)

#(see keywords Notebook)
def keywords(sentence):
    keywords = Rake.run(sentence)
    liste = []
    for keyword, i in keywords:
        liste.append(keyword)
    string = ' '.join(liste)
    return string

#this is to apply the symptom model on the user input sentence and predict the symptom (plus probability of right prediction)
def symptom(sentence):

    #tokenize
    sentence = nltk.word_tokenize(sentence)

    #word_to_vec (+stemming in word to vec function)
    X = word_to_vect(sentence, word_list)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    #predict
    output = model(X)
    _, predicted = torch.max(output, dim=1)

    #get right tag
    tag = tags[predicted.item()]
    
    #get probability
    probability = torch.softmax(output, dim=1)
    probability = probability[0][predicted.item()].item()

    return tag, probability

#this is to apply the disease model on the user list of symptoms (similar approach to symptom prediction)
def disease(liste):
    #create bag of symptoms
    bag_of_symptoms = []

    for symptom in list_of_symptoms: 
        if symptom in liste:
            bag_of_symptoms.append(1)
        else: 
            bag_of_symptoms.append(0)

    bag_of_symptoms = np.asarray(bag_of_symptoms) 
    bag_of_symptoms = bag_of_symptoms.reshape(1,-1)
    
    #predict disease
    disease = model_final.predict(bag_of_symptoms)[0]
    return disease

#this is the function that gets applied when the user sends a message
def bot(sentence):
    
    #if the user is done with describing their symptoms, the disease gets predicted
    if sentence.replace(".", "").replace("!","").lower().strip() == "done":
        

        final_disease = disease(user_symptoms)

        
        response = f'Considering your described symptoms, you probably have the following disease: {final_disease}'

        user_symptoms.clear()

    #if the user is still describing a new symptom, the symptom gets predicted    
    else:
        
        #first keyword extraction
        keyword = keywords(sentence)
        #then symptom prediction
        new_symptom, probability = symptom(keyword)
        
        #if the model is over 50% sure of the symptom, then add it to the list, else not
        if probability > 0.50:

            user_symptoms.add(new_symptom)
            
            
            response = f'I am {probability*100:.2f}% sure you described the symptom: {new_symptom.replace("_", " ")}. So far you have described the following symptoms: {[item.replace("_", " ") for item in  user_symptoms]}'
        else:
            response = f"I'm afraid I was not able to identify your symptom. {probability*100:.2f}%"

    return response

##############################################

##############################################

#Start app

app = Flask(__name__)

#set new user list of symptoms
    
user_symptoms = set()
user_symptoms.clear()

###############################
#old code
data = []
file = open("static/assets/files/ds_symptoms.txt", "r")
all_symptoms = file.readlines()

for s in all_symptoms:
    data.append(s.replace("'", "").replace("_", " ").replace(",\n", ""))
data = json.dumps(data)
###############################

#index page

@app.route('/')
def index():
    return render_template('index.html', data=data)

#symptom function gets triggered when user hits enter / clicks send button

@app.route('/symptom', methods=['GET', 'POST'])
def predict_symptom():

    #get sentence from html
    sentence = request.json['sentence']
    
    #get response from function
    response = bot(sentence)
    
    #post response to html
    return jsonify(response)


