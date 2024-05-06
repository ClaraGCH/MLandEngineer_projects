import streamlit as st
import pandas as pd
import plotly.express as px 
import numpy as np
import math

# Config
st.set_page_config(
    page_title="Getaround Delay Analysis 🚗",
    page_icon="🚗 ",
    layout="wide")

st.title('Getaround Delay Analysis - Dashboard')
st.markdown("""
    When using Getaround, drivers book cars for a specific time period: hours to days.
    Users need to bring back the car on time.Somemtimes drivers are late for the checkout.
    Late returns at checkout may generate problems for the next driver, especially, if the car is reserved on the same day. 
""")

# Function to load data
@st.cache_data 
def load_data():
    fname = 'get_around_delay_analysis.xlsx'
    data = pd.read_excel(fname)
    return data
 

df_delay = load_data()
if st.checkbox('Show raw data'):
    st.subheader('Raw delay data')
    st.write(df_delay) 

st.subheader("Presentation of the data about delays")
columns = ['rental_id', 'car_id', 'checkin_type', 'state', 'delay_at_checkout_in_minutes', 
           'previous_ended_rental_id', 'time_delta_with_previous_rental_in_minutes']

st.header('Main Numbers')
col1, col2, col3 = st.columns(3)
nb_rentals = len(df_delay)
with  col1:
    st.metric(label = 'Number of cars', value = df_delay["car_id"].nunique())
with col2:
    st.metric(label = "Number of cars with consecutive rental",
               value=f"{round(len(df_delay[~df_delay['previous_ended_rental_id'].isna()]) / nb_rentals * 100)}%")
with col3:
    st.metric(label = "Maximal time between 2 rentals", 
              value=f"{round(df_delay['time_delta_with_previous_rental_in_minutes'].max())} minutes")


def get_previous_rental_delay(row, dataframe):
    delay = np.nan
    previous_rental_id = row['previous_ended_rental_id']
    if not np.isnan(previous_rental_id):
        previous_rental = dataframe[dataframe['rental_id'] == previous_rental_id]
        if not previous_rental.empty:
            delay = previous_rental['delay_at_checkout_in_minutes'].values[0]
    return delay

def get_impact_of_previous_rental_delay(row):
    impact = 'No previous rental info'
    if not math.isnan(row['checkin_delay_in_minutes']):
        if row['checkin_delay_in_minutes'] > 0:
            if row['state'] == 'Canceled':
                impact = 'Cancelation'
            else:
                impact = 'Late checkin'
        else:
            impact = 'No impact'
    return impact

def delay_function(x):
    y = 'Unknown'  
    if x < 0 :
        y = 'No delay'
    elif x< 5:
        y = 'Delay between <5 mins'
    elif 5<x < 10 : 
        y = 'Delay between 5-10 mins'
    elif 10<x < 60 :
        y = 'Delay between 10-60 mins'
    elif x >= 60 :
        y = 'Delay ≥ 60'
    elif x >= 1440:
        y ='Delay of 1 day'
    return y    

df_delay['previous_rental_checkout_delay_in_minutes'] = df_delay.apply(get_previous_rental_delay, args = [df_delay], axis = 1) # add 'previous_rental_checkout_delay_in_minutes' column:
df_delay['checkin_delay_in_minutes'] = df_delay['previous_rental_checkout_delay_in_minutes'] - df_delay['time_delta_with_previous_rental_in_minutes'] # add 'checkin_delay_in_minutes' column:
df_delay['checkin_delay_in_minutes'] = df_delay['checkin_delay_in_minutes'].apply(lambda x: 0 if x < 0 else x)
df_delay['impact_of_previous_rental_delay'] = df_delay.apply(get_impact_of_previous_rental_delay, axis = 1)# add 'impact_of_previous_rental_delay' column:
df_delay = df_delay[df_delay['delay_at_checkout_in_minutes'] != 'Unknown']
df_delay ['delay_timecheckout'] = df_delay["delay_at_checkout_in_minutes"].apply(lambda x: delay_function(x))
df_delay ['delay_timewith previous'] = df_delay["time_delta_with_previous_rental_in_minutes"].apply(lambda x: delay_function(x))

selected_feature = st.selectbox("Select a feature to visualize", columns)
fig = px.histogram(data_frame=df_delay, x=selected_feature)
fig.update_layout(title=f"Distribution plot of {selected_feature}")
st.plotly_chart(fig, use_container_width=True)

# Plot histograms
st.markdown("---")
st.subheader("Some data insights")

fig1 = px.histogram(df_delay, x='delay_timecheckout', histnorm= "percent")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.histogram(df_delay, x='delay_timewith previous', color='checkin_type', facet_col='state', histnorm='percent')
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(df_delay, x='state', color='delay_timewith previous', facet_col='checkin_type', histnorm='percent')
st.plotly_chart(fig3, use_container_width=True)


@st.cache_data 
def load_data2():
    fname = 'get_around_pricing_project.csv'
    data_price = pd.read_csv(fname)
    return data_price
 
df_price = load_data2()
if st.checkbox('Show raw data', key= 'raw_data_checkbox'):
    st.subheader('Raw prizes data')
    st.write(df_price) 

st.subheader("Presentation of the data about prices")
cols_cat = ['model_key', 'fuel', 'paint_color', 'car_type', 'private_parking_available', 'has_gps',
            'has_air_conditioning', 'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires']
cols_num = ['mileage', 'engine_power', 'rental_price_per_day']

col1, col2, col3 = st.columns(3)
for col, num_feature in zip([col1, col2, col3], cols_num):
    with col:
        st.write(f"#### Descriptive statistics for {num_feature}") #"<b>Rental state</b>"
        st.write(df_price[num_feature].describe())

        st.write(f"#### Histogram of {num_feature}")
        fig = px.histogram(df_price, x=num_feature)
        st.plotly_chart(fig, use_container_width=True)

selected_column = st.selectbox("Select a categorical column to visualize", cols_cat) # Let the user choose the column
st.write(f"#### Descriptive statistics for {selected_column}")
st.write(df_price[selected_column].describe())

st.write(f"#### Histogram of {selected_column}")
fig = px.histogram(df_price, x=selected_column)
st.plotly_chart(fig, use_container_width=True)

