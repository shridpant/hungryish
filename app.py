import os 
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
import matplotlib.pyplot as plt 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

@app.route('/prediction/<filename>') 
def prediction(filename):
    my_image = os.getcwd() + '\\static\\' + str(filename)
    html_image = image_file = url_for('static', filename=str(filename))
    image_file = tf.io.gfile.GFile(my_image, 'rb')
    data = image_file.read()
    # Model Initialization
    classes = [line.rstrip() for line in tf.io.gfile.GFile(os.getcwd() + "\\ML-Model\\hot_dog_labels.txt")]
    with tf.io.gfile.GFile(os.getcwd() + "\\ML-Model\\hot_dog_graph.pb", 'rb') as inception_graph:
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

if __name__ == "__main__":
    app.run(debug=True)