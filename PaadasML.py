# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, send_file, Response, render_template, redirect, url_for, request
import random
import time
import wave
import io
import os

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
# ‘/’ URL is bound with index() function.
@app.route('/')
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

    files = []
    number = random.randint(1,10)
    files.append("./numbers/" + str(number) + ".wav")
    times = random.randint(1,10)
    files.append("./times/" + str(times) + ".wav")
    #data = dict(
    #    file=(generate(files), "padaa.wav"),
    #)
    padaa = generate(files)
    f = open('./padaa.wav', 'wb')
    f.write(padaa)
    f.close()
    if os.path.isfile('./padaa.wav'):
        print("./padaa.wav exists")
    #app.post(url_for('static', filename='padaa.wav'), content_type='multipart/form-data', data=data)
    return render_template("index.html", source=padaa)
    #return Response(padaa, mimetype='audio/wav')

@app.route("/recording", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = open('./file.wav', 'wb')
        f.write(request.data)
        f.close()
        if os.path.isfile('./file.wav'):
            print("./file.wav exists")

        return render_template('index.html', request="POST")   
    else:
        return render_template("index.html")
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
