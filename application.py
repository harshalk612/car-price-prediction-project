# modules: streamlit, numpy , pickle-mixin

import streamlit as st
import pickle
import numpy as np
import pandas as pd
import pyautogui

# Import the model and dataset
pipe_lr = pickle.load(open("LRModel.pkl", "rb"))
df_cars = pickle.load(open("cleaned_data.pkl", "rb"))

# # Title for the App
st.title("Car Price Prediction")

# Making a Dict for Company and Model Together
comp_model_dict = {}

for company_name in sorted(list(df_cars["company"].unique())):
    comp_model_dict[company_name] = []
    for car_name in sorted(list(df_cars["name"].unique())):
        if company_name in car_name:
            comp_model_dict[company_name].append(car_name)

# adding "select" as the first and default choice
company_name = st.selectbox("Select the Company Name: ", options=[
                            "Choose Company"] + list(comp_model_dict.keys()), key="company")

# display selectbox 2 if Company_name is not "select"
if company_name != "Choose Company":
    car_model = st.selectbox(
        'Select Car Model', options=["Choose Model"] + comp_model_dict[company_name])

# Selecting the Year of Purchase
year = st.selectbox("Select the Year of Purchase:",
                    ["Choose Year"] + sorted(list(df_cars["year"].unique())), key="year")

# Typing the KMS Driven
kms_driven = st.text_input(
    "Type the Kilometers driven till now: ", "Enter in Digits", key="kms_driven")

# # Selecting the Fuel Type
fuel_type = st.selectbox("Select the Fuel Type",
                         ["Choose Fuel Type"] + sorted(list(df_cars["fuel_type"].unique())), key="fuel_type")

# Button to Predict
if st.button("Predict Price"):
    # Query
    pred = pipe_lr.predict(pd.DataFrame([
        [car_model, company_name, year, kms_driven, fuel_type]], columns=["name", "company", "year", "kms_driven", "fuel_type"]))

    pred_final = np.round(float(pred[0]), 2)
    pred_sentence = "Predicted Price: ₹ " + str(pred_final)
    st.title(pred_sentence)


def reset():
    st.session_state.company = "Choose Company"
    st.session_state.year = "Choose Year"
    st.session_state.fuel_type = "Choose Fuel Type"
    st.session_state["kms_driven"] = "Enter KMs Again"


st.button('Reset All', on_click=reset)
# Another Workaround
# if st.button("Reset"):
#     pyautogui.hotkey("ctrl", "F5")
