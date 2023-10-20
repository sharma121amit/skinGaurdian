from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import numpy as np

app = Flask(__name__)

# Assuming our model is saved as "cancer_model.h5"
# from tensorflow.keras.models import load_model
# model = load_model('cancer_model.h5')

# For the sake of this demonstration, creating a dummy model function
def dummy_model_predict(image_path):
    """Dummy function to simulate model prediction. 
    Returns 1 for malignant and 0 for benign."""
    # In real-world, we would preprocess the image and use model.predict
    return np.random.choice([0, 1])

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join("/tmp", filename)
        file.save(filepath)
        
        # Predict using the model
        prediction = dummy_model_predict(filepath)
        if prediction == 1:
            return jsonify({"result": "malignant"})
        else:
            return jsonify({"result": "benign"})

    return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)