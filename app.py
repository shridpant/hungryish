# MIT License

# Copyright (c) 2020 Shrid Pant

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os 
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import tensorflow as tf
import matplotlib.pyplot as plt 
import random

from src import meme

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def main_page():
    try:
        if request.method == 'POST':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', filename))
            return redirect(url_for('prediction', filename=filename))
        return render_template('index.html')
    except Exception as msg:
        return error(msg)

@app.route('/prediction/<filename>') 
def prediction(filename):
    try:
        my_image = os.getcwd() + '\\static\\' + str(filename)
        html_image = image_file = url_for('static', filename=str(filename))
        image_file = tf.io.gfile.GFile(my_image, 'rb')
        data = image_file.read()
        # Model Initialization
        classes = [line.rstrip() for line in tf.io.gfile.GFile(os.getcwd() + "\\src\\classes.txt")]
        with tf.io.gfile.GFile(os.getcwd() + "\\src\\model.pb", 'rb') as inception_graph:
            definition = tf.compat.v1.GraphDef()
            definition.ParseFromString(inception_graph.read())
            _ = tf.import_graph_def(definition, name='')
        with tf.compat.v1.Session() as session:
            tensor = session.graph.get_tensor_by_name('final_result:0')
            #^ Feeding data as input and find the first prediction
            result = session.run(tensor, {'DecodeJpeg/contents:0': data})
            top_results = result[0].argsort()[-len(result[0]):][::-1] 
            max_score = 0
            for type in top_results:
                hot_dog_or_not = classes[type]
                score = result[0][type]
                if score > max_score:
                    max_score = score
                    predictions = hot_dog_or_not
        return render_template('predict.html', predictions=str(predictions), my_image=html_image)
    except Exception as msg:
        return error(msg)

def error(message, code=400):
    meme.meme(message)
    return render_template("error.html", random = random.randint(1, 32500))

# Error handler
def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)