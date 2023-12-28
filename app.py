from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet_v2 import preprocess_input
import numpy as np

app = Flask(__name__)

# Define the directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

# Load your trained model
def load_your_model():
    model_path = 'StandardOCR-ResNet50V2-2.h5'  # Replace with your model path
    model = load_model(model_path)
    return model

# Function to preprocess the uploaded image
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Preprocess for ResNet50V2
    return img_array

# Function to perform prediction
def perform_prediction(filepath):
    loaded_model = load_your_model()  # Load the model
    processed_img = preprocess_image(filepath)  # Preprocess the image
    predictions = loaded_model.predict(processed_img)  # Get predictions
    predicted_class_index = np.argmax(predictions, axis=1)[0]  # Get the predicted class index
    return predicted_class_index  # Return the predicted class index

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        predicted_class_index = perform_prediction(filepath)  # Get the predicted class index
        # Convert class index to class name based on your class list
        class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        predicted_class_name = class_names[predicted_class_index]

        return jsonify({'prediction': predicted_class_name})  # Return the predicted class name

    return jsonify({'error': 'File not allowed or unsupported format'})

if __name__ == '__main__':
    app.run(debug=True)
