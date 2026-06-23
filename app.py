import streamlit as st
import pandas as pd
import joblib

model = joblib.load("churn_model.pkl")

st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📞",
    layout="wide"
)

st.title("📞 Customer Churn Predictor")
st.markdown("""
Predict whether a telecom customer is likely to leave the company using machine learning.
""")

st.sidebar.title("Project Info")
st.sidebar.info("""
Customer Churn Prediction

Model: Logistic Regression  
Goal: Predict if a customer will churn.

Key metric:
Recall for churn customers improved compared to Random Forest.
""")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["👤 Customer Info", "📡 Services", "💳 Billing"])

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.selectbox("Senior Citizen", ["No", "Yes"])

    with col2:
        partner = st.selectbox("Partner", ["No", "Yes"])
        dependents = st.selectbox("Dependents", ["No", "Yes"])

    with col3:
        tenure = st.number_input("Tenure (months)", 0, 100, 12)

with tab2:
    col1, col2, col3 = st.columns(3)

    with col1:
        phone = st.selectbox("Phone Service", ["No", "Yes"])
        multiple = st.selectbox("Multiple Lines", ["No", "Yes"])

    with col2:
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["No", "Yes"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes"])

    with col3:
        device = st.selectbox("Device Protection", ["No", "Yes"])
        tech = st.selectbox("Tech Support", ["No", "Yes"])
        tv = st.selectbox("Streaming TV", ["No", "Yes"])
        movies = st.selectbox("Streaming Movies", ["No", "Yes"])

with tab3:
    col1, col2, col3 = st.columns(3)

    with col1:
        paperless = st.selectbox("Paperless Billing", ["No", "Yes"])
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

    with col2:
        payment = st.selectbox(
            "Payment Method",
            [
                "Bank transfer (automatic)",
                "Credit card (automatic)",
                "Electronic check",
                "Mailed check"
            ]
        )

    with col3:
        monthly = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
        total = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)

input_data = pd.DataFrame({
    "gender": [1 if gender == "Male" else 0],
    "SeniorCitizen": [1 if senior == "Yes" else 0],
    "Partner": [1 if partner == "Yes" else 0],
    "Dependents": [1 if dependents == "Yes" else 0],
    "tenure": [tenure],
    "PhoneService": [1 if phone == "Yes" else 0],
    "MultipleLines": [1 if multiple == "Yes" else 0],
    "OnlineSecurity": [1 if online_security == "Yes" else 0],
    "OnlineBackup": [1 if online_backup == "Yes" else 0],
    "DeviceProtection": [1 if device == "Yes" else 0],
    "TechSupport": [1 if tech == "Yes" else 0],
    "StreamingTV": [1 if tv == "Yes" else 0],
    "StreamingMovies": [1 if movies == "Yes" else 0],
    "PaperlessBilling": [1 if paperless == "Yes" else 0],
    "MonthlyCharges": [monthly],
    "TotalCharges": [total],
    "InternetService_Fiber optic": [1 if internet == "Fiber optic" else 0],
    "InternetService_No": [1 if internet == "No" else 0],
    "Contract_One year": [1 if contract == "One year" else 0],
    "Contract_Two year": [1 if contract == "Two year" else 0],
    "PaymentMethod_Credit card (automatic)": [1 if payment == "Credit card (automatic)" else 0],
    "PaymentMethod_Electronic check": [1 if payment == "Electronic check" else 0],
    "PaymentMethod_Mailed check": [1 if payment == "Mailed check" else 0],
})

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🔮 Predict Customer Churn", use_container_width=True):
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        st.metric(
            label="Churn Probability",
            value=f"{probability:.2%}"
        )

        if prediction == 1:
            st.error("High Risk: This customer is likely to churn.")
            st.write("Business recommendation: Offer a discount, improve support, or suggest a longer contract.")
        else:
            st.success("Low Risk: This customer is likely to stay.")
            st.write("Business recommendation: Maintain engagement and continue good customer support.")