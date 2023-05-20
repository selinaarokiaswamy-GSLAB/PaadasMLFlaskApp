# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, Response, render_template, request, session
import random
import time
import wave
import io
import os

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.secret_key = "Sameer"
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
# ‘/’ URL is bound with index() function.
@app.route('/',  methods=['POST', 'GET'])
def index():
    print (request.method)
    if request.method == "POST":
        f = open('./file.wav', 'wb')
        f.write(request.data)
        f.close()
        if os.path.isfile('./file.wav'):
            print("./file.wav exists")
        answer = session["number"] * session["times"]
        # TODO: hook up to google recognition
        # TODO: identify files to play depending on recorded and correct answer
        # TODO: also pose the next problem
        session["files"] = [ "./numbers/" + str(answer) + ".wav" ]
        return render_template("index.html", answer = answer)
    else:
        session["number"] = random.randint(1,10)
        session["times"] = random.randint(1,10)
        files = []
        number = session["number"]
        files.append("./numbers/" + str(number) + ".wav")
        times = session["times"]
        files.append("./times/" + str(times) + ".wav")
        session["files"] = files
        return render_template("index.html", number=session["number"], times=session["times"])

@app.route('/paadas')
def paadas():
    #Approach 2
    def generate(files):
        with wave.open(files[0], 'rb') as f:
            params = f.getparams()
            frames = f.readframes(f.getnframes())
        
        for file in files[1:]:
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
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
