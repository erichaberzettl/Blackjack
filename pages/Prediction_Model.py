import streamlit as st
import joblib
import pandas as pd
import numpy as np
from zipfile import ZipFile
from io import BytesIO

st.set_page_config("Simulation Results", "🂡", layout="wide")

st.title("Blackjack Simulator")

st.header(f"Prediction Model")

model_3 = joblib.load("backend/model_3_log_reg.pkl")
X_cols = ["dealer_upcard", "hand_start_value", "is_soft", "dealer_ace", "is_blackjack"]

def predict_win_probability():
    data_df = pd.DataFrame([{"dealer_upcard": st.session_state.dealer_upcard, 
            "hand_start_value": st.session_state.hand_start_value, 
            "is_soft": int(st.session_state.is_soft), 
            "dealer_ace": int(st.session_state.dealer_ace), 
            "blackjack": int(st.session_state.is_blackjack)}])
    
    
    return model_3.predict_proba(data_df)[0]

with st.form("prediction_input", clear_on_submit=True, enter_to_submit=True):
    st.write("Predict the win/loss probability for a specific setup with Logistic Regression")
    
    st.number_input(label="Dealer upcard value (1 is Ace)", min_value=1, max_value=10, key="dealer_upcard")
    st.number_input(label="Hand start value ", min_value=4, max_value=21, key="hand_start_value")
    
    col1, col2, col3 = st.columns(3)
    col1.checkbox(label="Hand is soft", key="is_soft")
    col2.checkbox(label="Hand is a Blackjack", key="is_blackjack")
    col3.checkbox(label="Dealer has an Ace", key="dealer_ace")

    submitted = st.form_submit_button("Predict")
    coefficients = model_3.coef_
    intercept = model_3.intercept_
    if submitted:
        result = predict_win_probability()
    
        col1, col2 = st.columns(2)
        col1.metric("Win Probability", value=round(result[1], 4))
        col2.metric("Loss Probability", value=round(result[0], 4))
        
        contributions = {"intercept": intercept}
        for i, col in enumerate(X_cols):
            contributions[col] = st.session_state[col] * coefficients[0][i]

        st.bar_chart(contributions, sort=False  )
        

st.header("About the model")

st.write("The underlying model is a Logistic Regression model built with scikit-learn.")

st.write("The data consists of rounds of Blackjack (S17), where one player played one hand using Basic Strategy. " \
"A quarter of the rounds were played with a 2, 4, 6 and 8 deck shoe respectively. Push hands (neither win nor loss) are excluded.")

st.write("On the training data, the model achieved an accuracy of 64%. This is bad for a normal binary classifier, " \
"but not in this context. A Blackjack hand can't be classified as a win or loss with certainty. It remains a gamble with a random component. " \
"However, different hands offer different chances to win. " \
"The model is therefore a good indicator on how good/profitable a certain hand setup is based on the hands it was trained on.")
st.markdown("### Parameters")
st.dataframe(pd.DataFrame(model_3.get_params(), index=[0]).reset_index(drop=True), hide_index=True)
coefficients_df = pd.DataFrame(coefficients, columns=X_cols)
coefficients_df["intercept"] = intercept
st.markdown("### Coefficients")
st.dataframe(coefficients_df, hide_index=True, column_order=["intercept"]+X_cols)
