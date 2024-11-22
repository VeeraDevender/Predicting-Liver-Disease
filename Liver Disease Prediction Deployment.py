# -*- coding: utf-8 -*-
"""liver disease prediction.ipynb

Automatically generated by Colab.

"""

# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Streamlit app title
st.title("Liver Disease Prediction App")

# File upload
uploaded_file = st.file_uploader("Upload your dataset (CSV file)", type=["csv"])

if uploaded_file is not None:
    # Load the dataset
    data = pd.read_csv(uploaded_file)

    # Display dataset
    st.subheader("Uploaded Dataset")
    st.write(data.head())

    # Preprocess the data
    st.subheader("Data Preprocessing")

    data_split = data.iloc[:, 0].str.split(';', expand=True)
    data_split.columns = [
        'category', 'age', 'sex', 'albumin', 'alkaline_phosphatase',
        'alanine_aminotransferase', 'aspartate_aminotransferase', 'bilirubin',
        'cholinesterase', 'cholesterol', 'creatinina', 'gamma_glutamyl_transferase', 'protein'
    ]

    num_cols = ['age', 'albumin', 'alkaline_phosphatase', 'alanine_aminotransferase',
                'aspartate_aminotransferase', 'bilirubin', 'cholinesterase', 'cholesterol',
                'creatinina', 'gamma_glutamyl_transferase', 'protein']
    data_split[num_cols] = data_split[num_cols].apply(pd.to_numeric, errors='coerce')

    data_split['sex'] = data_split['sex'].map({'m': 1, 'f': 0})
    le = LabelEncoder()
    data_split['category'] = le.fit_transform(data_split['category'])
    data_cleaned = data_split.dropna()

    st.write("Data after preprocessing:")
    st.write(data_cleaned.head())

    # Split the data into features and target
    X = data_cleaned.drop('category', axis=1)
    y = data_cleaned['category']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train the Logistic Regression model
    st.subheader("Training Logistic Regression Model")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Model performance metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    st.subheader("Logistic Regression Model Performance")
    st.write(f"**Accuracy:** {accuracy:.2f}")
    st.text_area("Classification Report", report, height=200)

    # Allow user to input data for prediction
    st.header("Make a Prediction")

    # Input fields for all features
    age = st.number_input("Age", min_value=0, max_value=150, value=50, key="age_input")
    sex = st.selectbox("Sex", ["Male", "Female"], key="sex_input")
    albumin = st.number_input("Albumin", min_value=0.0, max_value=10.0, value=4.0, key="albumin_input")
    alkaline_phosphatase = st.number_input("Alkaline Phosphatase", min_value=0.0, max_value=500.0, value=80.0, key="alk_phosphatase_input")
    alanine_aminotransferase = st.number_input("Alanine Aminotransferase", min_value=0.0, max_value=500.0, value=30.0, key="alanine_input")
    aspartate_aminotransferase = st.number_input("Aspartate Aminotransferase", min_value=0.0, max_value=500.0, value=30.0, key="aspartate_input")
    bilirubin = st.number_input("Bilirubin", min_value=0.0, max_value=5.0, value=1.0, key="bilirubin_input")
    cholinesterase = st.number_input("Cholinesterase", min_value=0.0, max_value=20.0, value=8.0, key="cholinesterase_input")
    cholesterol = st.number_input("Cholesterol", min_value=0.0, max_value=500.0, value=200.0, key="cholesterol_input")
    creatinina = st.number_input("Creatinina", min_value=0.0, max_value=10.0, value=1.0, key="creatinina_input")
    gamma_glutamyl_transferase = st.number_input("Gamma Glutamyl Transferase", min_value=0.0, max_value=200.0, value=50.0, key="gamma_glutamyl_input")
    protein = st.number_input("Protein", min_value=0.0, max_value=10.0, value=7.0, key="protein_input")

    # Prepare the input data for prediction
    input_data = pd.DataFrame({
        'age': [age],
        'sex': [1 if sex == "Male" else 0],
        'albumin': [albumin],
        'alkaline_phosphatase': [alkaline_phosphatase],
        'alanine_aminotransferase': [alanine_aminotransferase],
        'aspartate_aminotransferase': [aspartate_aminotransferase],
        'bilirubin': [bilirubin],
        'cholinesterase': [cholinesterase],
        'cholesterol': [cholesterol],
        'creatinina': [creatinina],
        'gamma_glutamyl_transferase': [gamma_glutamyl_transferase],
        'protein': [protein]
    })

    # Prediction button
    if st.button("Predict", key="predict_button"):
        prediction = model.predict(input_data)[0]
        st.write(f"Predicted Disease Category: {prediction}")