 # Car Price Prediction App
This app predicts the price of cars based on various features using machine learning models trained on the get_around_pricing_project.csv dataset.

# Models
The following regression models were trained to predict car prices:

Linear Regressor: This model uses a linear approach to predict car prices based on input features.
Random Forest Regressor: This ensemble learning method constructs multiple decision trees during training and outputs the mean prediction of the individual trees for regression tasks.
# Best Model
The Random Forest Regressor outperformed other models, demonstrating better performance in predicting car prices. The following metrics were used to evaluate the model:

R2 Score: This metric measures the proportion of the variance in the dependent variable that is predictable from the independent variables. Higher values indicate better model performance.
Mean Squared Error (MSE): This metric measures the average squared difference between the predicted values and the actual values. Lower values indicate better model performance.

# How to Use
Input Features: Users can input various features of a car, such as model key, mileage, engine power, fuel type, paint color, car type, and additional attributes like parking availability, GPS, air conditioning, etc.
Prediction: After entering the car features, the app predicts the price of the car based on the trained Random Forest Regressor model.

# Usage
To use the app locally, follow these steps:

1.Install the required Python libraries listed in requirements.txt.
2.Run the Streamlit app using the command streamlit run dashboard_predictor.py.
3.Open the app in your web browser and input the car features to get the predicted price.
# Data Source
The data used to train the models (get_around_pricing_project.csv) can be found in the same directory.









