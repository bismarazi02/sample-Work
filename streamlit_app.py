# -*- coding: utf-8 -*-
"""streamlit_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ns3R1ew74uAZK2tDWhAL4PzPoP1FOJic
"""


# Commented out IPython magic to ensure Python compatibility.
# %%writefile healthy-heart-app.py
import streamlit as st
import base64
import numpy as np
import pickle as pkl
from sklearn.preprocessing import MinMaxScaler
scal = MinMaxScaler()

model = pkl.load(open("final_model.p", "rb"))

st.set_page_config(page_title="Healthy Heart App", page_icon="⚕️", layout="centered", initial_sidebar_state="expanded")

def preprocess(age, sex, cp, trestbps, restecg, chol, fbs, thalach, exang, oldpeak, slope, ca, thal):
    if sex == "male":
        sex = 1
    else:
        sex = 0

    if cp == "Typical angina":
        cp = 0
    elif cp == "Atypical angina":
        cp = 1
    elif cp == "Non-anginal pain":
        cp = 2
    elif cp == "Asymptomatic":
        cp = 2

    if exang == "Yes":
        exang = 1
    elif exang == "No":
        exang = 0

    if fbs == "Yes":
        fbs = 1
    elif fbs == "No":
        fbs = 0

    if slope == "Upsloping: better heart rate with exercise(uncommon)":
        slope = 0
    elif slope == "Flatsloping: minimal change(typical healthy heart)":
        slope = 1
    elif slope == "Downsloping: signs of unhealthy heart":
        slope = 2

    if thal == "fixed defect: used to be defect but ok now":
        thal = 6
    elif thal == "reversable defect: no proper blood movement when exercising":
        thal = 7
    elif thal == "normal":
        thal = 2.31

    if restecg == "Nothing to note":
        restecg = 0
    elif restecg == "ST-T Wave abnormality":
        restecg = 1
    elif restecg == "Possible or definite left ventricular hypertrophy":
        restecg = 2

    user_input = [age, sex, cp, trestbps, restecg, chol, fbs, thalach, exang, oldpeak, slope, ca, thal]
    user_input = np.array(user_input)
    user_input = user_input.reshape(1, -1)
    user_input = scal.fit_transform(user_input)
    prediction = model.predict(user_input)

    return prediction

html_temp = """
    <div style ="background-color:pink;padding:13px">
    <h1 style ="color:black;text-align:center;">Healthy Heart App</h1>
    </div>
    """

st.markdown(html_temp, unsafe_allow_html=True)
st.subheader('by Amlan Mohanty ')

age = st.selectbox("Age", range(1, 121, 1))
sex = st.radio("Select Gender: ", ('male', 'female'))
cp = st.selectbox('Chest Pain Type',("Typical angina","Atypical angina","Non-anginal pain","Asymptomatic"))
trestbps = st.selectbox('Resting Blood Sugar', range(1, 500, 1))
restecg = st.selectbox('Resting Electrocardiographic Results',("Nothing to note","ST-T Wave abnormality","Possible or definite left ventricular hypertrophy"))
chol = st.selectbox('Serum Cholestoral in mg/dl', range(1, 1000, 1))
fbs = st.radio("Fasting Blood Sugar higher than 120 mg/dl", ['Yes','No'])
thalach = st.selectbox('Maximum Heart Rate Achieved', range(1, 300, 1))
exang = st.selectbox('Exercise Induced Angina',["Yes","No"])
oldpeak = st.number_input('Oldpeak')
slope = st.selectbox('Heart Rate Slope',("Upsloping: better heart rate with exercise(uncommon)","Flatsloping: minimal change(typical healthy heart)","Downsloping: signs of unhealthy heart"))
ca = st.selectbox('Number of Major Vessels Colored by Fluoroscopy', range(0, 5, 1))
thal = st.selectbox('Thalium Stress Result', range(1, 8, 1))

pred = preprocess(age, sex, cp, trestbps, restecg, chol, fbs, thalach, exang, oldpeak, slope, ca, thal)

if st.button("Predict"):
    if pred[0] == 0:
        st.error('Warning! You have a high risk of getting a heart attack!')
    else:
        st.success('You have a lower risk of getting a heart disease!')

st.sidebar.subheader("About App")
st.sidebar.info("This web app helps you find out whether you are at risk of developing a heart disease.")
st.sidebar.info("Enter the required fields and click on the 'Predict' button to check whether you have a healthy heart")
st.sidebar.info("Don't forget to rate this app")
