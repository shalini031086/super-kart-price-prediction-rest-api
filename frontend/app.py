import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Super Kart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features


Store_Age_Years = st.number_input("Store Age in Years", min_value=1, step=1, value=2)
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Size = st.selectbox("Store Size", ["High", "Medium","Low"])
Store_Type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type 1","Supermarket Type 2","Food Mart"])
Product_Type_Category = st.selectbox("Product Type Category", ["meat", "snack foods", "hard drinks", "dairy", "canned", "soft drinks", "health and hygiene", "baking goods", "bread", "breakfast", "frozen foods", "fruits and vegetables", "household", "seafood", "starchy foods", "others"])
Product_Id_char = st.selectbox("Product ID", ["FD", "DR", "NC",])
Product_MRP = st.number_input("Product MRP", min_value=0.0, max_value=10000.0, step=1.0, value=1.0)
Product_Weight = st.number_input("Product Weight", min_value=0, step=1, value=1)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product allocated ares", min_value=0, step=1, value=1)

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Store_Age_Years': Store_Age_Years,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Size': Store_Size,
    'Store_Type': Store_Type,
    'Product_Type_Category': Product_Type_Category,
    'Product_Id_char': Product_Id_char,
    'Product_MRP': Product_MRP,
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/superkart", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Price (in dollars)']
        st.success(f"Super Kart Sales Price (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/superkartbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
