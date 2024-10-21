import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)
rf_model = pickle.load(open('trained_model.pkl', 'rb'))

# Create a LabelEncoder object for non-numeric features
label_encoder = LabelEncoder()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = request.form.getlist('feature')

    # Fit the LabelEncoder with non-numeric features and transform them
    preprocessed_features = label_encoder.fit_transform(features)

    # Convert features to a numeric array
    numeric_features = np.array(preprocessed_features, dtype=float)

    final_features = [numeric_features]
    prediction = rf_model.predict(final_features)

    return render_template('index.html', prediction_text='{}'.format(prediction))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=True)

