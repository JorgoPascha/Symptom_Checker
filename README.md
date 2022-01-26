# Symptom_Checker

## Dokumentation
### Disclaimer
Dieser Chatbot ist ein rein wissenschaftliches Projekt. Er sollte nicht als Diagnosemittel für echte Krankheitssymptome verwendet werden.

### Getting Started: 

Folgende Bibliotheken werden benötigt um den Symptom Checker zu starten:
```
pip install numpy

pip install pandas

pip install nltk

pip install spacy

pip install python-rake

pip install torch

pip install sklearn

pip install flask
```
Erstellen eines Virtual Environment:

```
py -3 -m venv venv
venv\Scripts\activate
```
Um nltk tokenization zu verwenden, muss folgende packages gedownloaded werden:
```
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw')
```
In Python kann nun über Flask das Frontend aufgerufen werden. Sie können den Chatbot nun verwenden.
```
python -m flask run
```

### Einleitung

#### Team:
Nico Heller (5538521), Lennart Schulz (3300490), Jonah Jäger (9431529), Marcel Winter (5542090), Georgios Paschaloglou (5405319), Laura Struss (4212678)

Ein Chatbot, welcher mit dem Mensch interagiert und einer Symptomatik einem Krankheitsbild zuordnet.

### Motivation
Wahllose Google-Suchen durch fundiertes Wissen ablösen, Alternative zum direkten Arztbesuch, digitale (Zweit-)Meinung.

### Ziel

Chatbot entwickeln, welcher Symptomen mit hoher prozentualen Sicherheit die richtige Diagnose/Krankheit zuordnen kann.



### Backend

Dokumentation zum Backend ist in den einzelnen Jupyter Notebooks und der app.py zu finden.

### Frontend

Das Frontend arbeitete anfangs mit Vue.js als PWA, wodurch folgende Erfolge erzielt werden:

Das vorgegebene MockUp: 

<div>
<img src="https://github.com/JorgoPascha/Symptom_Checker/blob/main/assets/MockUp_HomeScreen.png?raw=true" alt="Mock-Up Homescreen" width="200"/>
<img src="https://github.com/JorgoPascha/Symptom_Checker/blob/main/assets/MockUp_Chatbot.png?raw=true" alt="Mock-Up Chatbot" width="200"/>
<img src="https://github.com/JorgoPascha/Symptom_Checker/blob/main/assets/MockUp_Description.png?raw=true" alt="Mock-Up Description" width="200"/>
</div>

<br>
Das in Vue.js erstellte Ergebnis:  
<br>
<br>

<div>
<img src="https://github.com/JorgoPascha/Symptom_Checker/blob/main/assets/VueHomeScreen.PNG?raw=true" alt="Ergebnis Homescreen" width="200"/>
<img src="https://github.com/JorgoPascha/Symptom_Checker/blob/main/assets/VueChatbot.PNG?raw=true" alt="Ergebnis Chatbot" width="200"/>
<img src="https://github.com/JorgoPascha/Symptom_Checker/blob/main/assets/VueDescription.PNG?raw=true" alt="Ergebnis Description" width="200"/>
</div>

Bevor das Frontend fertiggestellt werden konnte, wurde versucht, dies mit dem Backend zu verbinden. Dies hat sich als sehr problematisch herausgestellt, da kein einfacher Weg vorhanden war, Pythonskripte in Vue auszuführen. Deshalb entschied sich das Team dazu, Flask zu verwenden, da dies sowieso benötigt wurde, um das Frontend mit dem Backend zu verbinden.

Nach dem Wechsel zu Flask wurde das Frontend von grundauf neu aufgebaut und das Team kam zu folgendem Ergebnis:


<div>
<img src="https://github.com/JorgoPascha/Symptom_Checker/blob/main/assets/ChatbotFlaskFinal2.png?raw=true" alt="Ergebnis Flask"/>
</div>
