import streamlit as st
import pandas as pd
import pickle
import time

# Load model and data
model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
car_data = pd.read_csv("Cleaned_Car_data.csv")

# Page config
st.set_page_config(
    page_title="Used Car Price Predictor",
    page_icon="🚗",
    layout="centered",
)

# Custom CSS
st.markdown("""
    <style>
    .white-title {
        text-align: center;
        font-size: 2.8em;
        color: white;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #e04444;
    }
    .scrap-message {
        padding: 1em;
        margin-top: 1em;
        background: linear-gradient(90deg, #ff7e5f, #feb47b);
        border-radius: 12px;
        font-size: 1.2em;
        font-weight: bold;
        color: white;
        text-align: center;
        animation: fadeIn 1.2s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="white-title">🚗 Used Car Price Predictor</div>', unsafe_allow_html=True)
st.markdown("#### Enter the details below to get an estimated resale price:")

# Dropdown options
car_names = sorted(car_data['name'].unique())
fuel_types = sorted(car_data['fuel_type'].unique())

# Select car name
name = st.selectbox("🔤 Select Car Name", car_names)

# Auto-fill the company based on car name
company_lookup = car_data[car_data['name'] == name]['company'].values
company = company_lookup[0] if len(company_lookup) > 0 else "Unknown"
st.text_input("🏢 Company (auto-filled)", value=company, disabled=True)

# Other inputs
year = st.slider("📅 Year of Purchase", 1990, 2025, 2020)
kms_driven = st.number_input("🛣️ Kilometers Driven", value=100)
fuel_type = st.selectbox("⛽ Select Fuel Type", fuel_types)

# Predict button
if st.button("🚀 Predict Price"):
    st.markdown("#### ⌛ Processing your request...")
    with st.spinner("Analyzing engine specs, mileage and fuel rates..."):
        time.sleep(2.5)

    input_df = pd.DataFrame([[name, company, year, kms_driven, fuel_type]],
                            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])

    prediction = model.predict(input_df)[0]

    st.balloons()
    st.success("🎉 Prediction complete!")

    if prediction < 0:
        st.markdown("""
            <div class="scrap-message">
                🚮 This car may have no resale value.<br>
                Consider scrapping or recycling it.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("## 💰 Estimated Car Price:")
        st.markdown(f"<h2 style='color: green;'>₹ {int(prediction):,}</h2>", unsafe_allow_html=True)
