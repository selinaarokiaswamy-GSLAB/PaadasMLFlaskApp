# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, Response, render_template, request, session
import random
import time
import wave
import io
import os
import uuid
import speech_recognition as sr

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.secret_key = "Sameer"

transcription = []

def load_transcription():
    with open("marathi_number_transcription.txt") as file:
        for line in file:
            transcription.append(line.split())
 
def pose_a_problem(files):
    session["number"] = random.randint(1,10)
    session["times"] = random.randint(1,10)
    number = session["number"]
    files.append("./numbers/" + str(number) + ".wav")
    times = session["times"]
    files.append("./times/" + str(times) + ".wav")
    session["files"] = files

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
# ‘/’ URL is bound with index() function.
@app.route('/',  methods=['POST', 'GET'])
def index():
    print (request.method)
    if request.method == "POST":
        correct_answer = session["number"] * session["times"]
        if request.mimetype == "audio/wav":
            file_name = "./samples/" + uuid.uuid4().hex + ".wav"
            f = open(file_name, 'wb')
            f.write(request.data)
            f.close()
            if os.path.isfile(file_name):
                print(file_name + " created")
            print("Recognizing the marathi number Now .... ")
            f = sr.AudioFile(file_name)
            r = sr.Recognizer()
            with f as source:
                audio = r.record(source)

            user_answer = ""
            try:
                user_answer = r.recognize_google(audio, language="mr-IN")
                print("You have said: " + user_answer)
            except Exception as e:
                print("Error :  " + str(e))

            # check answer
            number_transcriptions = []

            if len(transcription) >= correct_answer:
                number_transcriptions = transcription[correct_answer - 1]

            is_correct = False

            for s in number_transcriptions:
                if s == user_answer:
                    is_correct = True

            files = []

            if is_correct:
                files.append("./prompt/correct.wav")
            else:
                # remove incorrect audio sample
                os.remove(file_name)
                files.append("./prompt/incorrect.wav")

            # revise the problem
            number = session["number"]
            files.append("./numbers/" + str(number) + ".wav")
            times = session["times"]
            files.append("./times/" + str(times) + ".wav")
            files.append("./numbers/" + str(correct_answer) + ".wav")

            # also pose the next problem
            pose_a_problem(files)
            print("session['files'] = ", session["files"])
    else:
        pose_a_problem([])
    
    return render_template("index.html", number=session["number"], times=session["times"])

@app.route('/paadas',  methods=['POST', 'GET'])
def paadas():
    #Approach 2
    def generate(files):
        with wave.open(files[0], 'rb') as f:
            params = f.getparams()
            frames = f.readframes(f.getnframes())
        
        print("in generate")

        for file in files[1:]:
            print("file = ", file)
            with wave.open(file, 'rb') as f:
                frames += f.readframes(f.getnframes())
        
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as f:
            f.setparams(params)
            f.writeframes(frames)
        
        buffer.seek(0)
        return buffer.read()

    return Response(generate(session["files"]), mimetype='audio/wav')
 
# main driver function
if __name__ == '__main__':
    load_transcription()
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
