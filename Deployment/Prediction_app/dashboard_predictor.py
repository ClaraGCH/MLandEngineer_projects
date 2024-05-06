import streamlit as st
import pandas as pd
import numpy as np
import math
from joblib import load
import joblib
from PIL import Image

preprocessor = joblib.load('preprocessor.pkl')
classifier = joblib.load('random_forest_regressor_model.pkl')

# Load dataframe
@st.cache_data 
def load_data():
    fname = 'get_around_pricing_project.csv'
    data_price = pd.read_csv(fname)
    return data_price
 
df_price = load_data()
if st.checkbox('Show raw data', key= 'raw_data_checkbox'):
    st.subheader('Raw prizes data')
    st.write(df_price) 

# Streamlit interface
st.title('Car Price Prediction')

# User input features
model_key = st.selectbox ('Model Key',df_price['model_key'].unique())
mileage = st.slider('Mileage (in km)', min_value=0, max_value=300000, step=1000)
engine_power = st.slider('Engine Power (in HP)', min_value=50, max_value=500, step=10)
fuel = st.selectbox('Fuel Type', ['diesel', 'petrol', 'electric', 'hybrid'])
paint_color = st.selectbox('Paint Color', ['black', 'white', 'silver', 'red', 'blue', 'grey'])
car_type = st.selectbox('Car Type', ['convertible', 'sedan', 'suv', 'hatchback', 'coupe', 'van'])
private_parking_available = st.checkbox('Private Parking Available')
has_gps = st.checkbox('GPS Available')
has_air_conditioning = st.checkbox('Air Conditioning Available')
automatic_car = st.checkbox('Automatic Car')
has_getaround_connect = st.checkbox('Getaround Connect Available')
has_speed_regulator = st.checkbox('Speed Regulator Available')
winter_tires = st.checkbox('Winter Tires Available')

# Preprocess input data
input_data = pd.DataFrame({
    'model_key':[model_key],
    'mileage': [mileage],
    'engine_power': [engine_power],
    'fuel': [fuel],
    'paint_color': [paint_color],
    'car_type': [car_type],
    'private_parking_available': [private_parking_available],
    'has_gps': [has_gps],
    'has_air_conditioning': [has_air_conditioning],
    'automatic_car': [automatic_car],
    'has_getaround_connect': [has_getaround_connect],
    'has_speed_regulator': [has_speed_regulator],
    'winter_tires': [winter_tires]})

# Convert categorical features to numerical encoding and preprocess
input_data_preprocessed = preprocessor.transform(input_data)

# Make prediction
predicted_price = classifier.predict(input_data_preprocessed)

# Display prediction
st.subheader('Predicted Car Price per Day')
st.write(f'${predicted_price[0]:,.2f}')

image = Image.open ("feature_importance.png")
st.image(image, caption='Feature Importances')
