# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
super_kart_predictor_api = Flask("Super Kart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("super_kart_model_v1_0.joblib")

# Define a route for the home page (GET request)
@super_kart_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Super Kart Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@super_kart_predictor_api.post('/v1/superkart')
def predict_super_kart_price():
    """
    This function handles POST requests to the '/v1/rental' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': superkart_data['Product_Weight'],
        'Product_Sugar_Content': superkart_data['Product_Sugar_Content'],
        'Product_Allocated_Area': superkart_data['Product_Allocated_Area'],
        'Product_Type_Category':	superkart_data['Product_Type_Category'],
        'Product_MRP': superkart_data['Product_MRP'],
        'Store_Size': superkart_data['Store_Size'],
        'Store_Location_City_Type': superkart_data['Store_Location_City_Type'],
        'Store_Type': superkart_data['Store_Type'],
        'Product_Id_char': superkart_data['Product_Id_char'],
        'Store_Age_Years': superkart_data['Store_Age_Years']
        }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction 
    Predicted_Product_Store_Sales_Total = model.predict(input_data)[0]

   # Convert predicted_price to Python float
    predicted_price = round(float(Predicted_Product_Store_Sales_Total), 2)
    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_price})


# Define an endpoint for batch prediction (POST request)
@super_kart_predictor_api.post('/v1/superkartbatch')
def predict_super_kart_batch():
    """
    This function handles POST requests to the '/v1/rentalbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_price = model.predict(input_data).tolist()

        # Create a dictionary of predictions with property IDs as keys
    superkart_ids = input_data['id'].tolist()  # Assuming 'id' is the property ID column
    output_dict = dict(zip(superkart_ids, predicted_price))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    super_kart_predictor_api.run(debug=True)
