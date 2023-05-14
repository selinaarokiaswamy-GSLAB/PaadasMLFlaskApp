# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, Response
import random
import time
import wave

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with paadas() function.
def paadas():
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
    files.append("../numbers/" + str(number) + ".wav")
    times = random.randint(1,10)
    files.append("../times/" + str(times) + ".wav")
    return render_template("index.html", source=generate(files))
   
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
