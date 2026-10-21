import streamlit as st
import requests

API_URL="http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

st.title("Car Price Prediction")
st.write("Enter Your Car Details To Estimate Its Selling Price.")

#st.divider()

#car details form
with st.form("car_prediction_form"):
    car_name=st.text_input(
        "Car Name",
        value="swift"
    )
    col1,col2=st.columns(2)

    with col1:
        year=st.number_input(
            "Manufacturing Year",
            min_value=1990,
            max_value=2026,
            value=2020,
            step=1,
            key="year"
        )
        present_price=st.number_input(
            "Present Price",
            min_value=0.01,
            value=5.59,
            step=0.1,
            key="present_price"
        )
        kms_driven=st.number_input(
            "Kilmeters Driven",
            min_value=0,
            value=25000,
            step=1000,
            key="kms_driven"
        )
    with col2:
        fuel_type=st.selectbox(
            "Fuel Type",
            ["Petrol","Diesel","CNG"]
        )
        seller_type=st.selectbox(
            "Seller Type",
            ["Dealer","Individual"]
        )
        transmission=st.selectbox(
            "TransmissionType",
            ["Manual","Automatic"]
        )

    owner=st.selectbox(
        "Number of Previous Owners",
        [0,1,2,3]
    )
    submitted=st.form_submit_button(
        "Predict Car Price",
        use_container_width=True
    )

if submitted:
    payload={
        "Car_Name":car_name,
        "Year":int(year),
        "Present_Price":float(present_price),
        "Kms_Driven":int(kms_driven),
        "Fuel_Type":fuel_type,
        "Seller_Type":seller_type,
        "TransmissionType":transmission,
        "Owner":int(owner)
    }

    try:
        with st.spinner("Predicting car price..."):
            response=requests.post(
                API_URL,
                json=payload,
                timeout=30
            )
        if response.status_code==200:
            result=response.json()
            predicted_price=result["prediction_price"]
            st.success("Prediction completed successfully!")
            st.subheader("Estimated Selling Price")
            st.metric(
                label="Predicted Price",
                value=f"{predicted_price:.2f} lakhs"
            )
            st.caption(
                "This is machine-learning estimate,"
                "not a guaranted market price."
            )
        else:
            st.error(
                f"API error({response.status_code}):"
                f"{response.text}"
            )
    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI."
            "Start your FastAPI server and try again."
        )
    except requests.exceptions.Timeout:
        st.error("The Prediction request timed out.")

    except (ValueError,KeyError):
        st.error("The API returned an unexpected response.")