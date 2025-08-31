import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# --- Doctor Recommendation Logic ---
# This is the "brain" for your new recommendation feature.

# Dummy Doctor Database
DOCTOR_DATABASE = {
    'Cardiologist': [
        {'name': 'Dr. Evelyn Reed', 'location': 'CardioCare Clinic, Downtown', 'rating': 4.8},
        {'name': 'Dr. Marcus Thorne', 'location': 'Heartbeat Center, Uptown', 'rating': 4.9},
    ],
    'Dermatologist': [
        {'name': 'Dr. Lena Petrova', 'location': 'Clear Skin Institute, South End', 'rating': 4.7},
        {'name': 'Dr. Samuel Cho', 'location': 'The Dermatology Group, West End', 'rating': 4.6},
    ],
    'Orthopedic Surgeon': [
        {'name': 'Dr. Isabella Rossi', 'location': 'Joint & Bone Specialists, North Park', 'rating': 4.9},
        {'name': 'Dr. Kenji Tanaka', 'location': 'Active Life Orthopedics, Eastside', 'rating': 4.8},
    ],
    'General Physician': [
        {'name': 'Dr. Alice Williams', 'location': 'Community Health Center', 'rating': 4.5},
        {'name': 'Dr. Ben Carter', 'location': 'Family Practice Associates', 'rating': 4.7},
    ],
    'Neurologist': [
        {'name': 'Dr. Omar Hassan', 'location': 'Mind & Brain Clinic, Central City', 'rating': 4.9},
        {'name': 'Dr. Sofia Chen', 'location': 'NeuroHealth Institute, Medical District', 'rating': 4.8},
    ],
    'Dentist': [
        {'name': 'Dr. Clara Santos', 'location': 'Bright Smile Dental, City Center', 'rating': 4.9},
        {'name': 'Dr. James Kwon', 'location': 'Downtown Dental Care, Metro Area', 'rating': 4.7},
    ]
}

# Symptom to Specialist Mapping
SYMPTOM_MAP = {
    'heart': 'Cardiologist', 'chest pain': 'Cardiologist', 'blood pressure': 'Cardiologist',
    'palpitations': 'Cardiologist', 'skin': 'Dermatologist', 'rash': 'Dermatologist',
    'acne': 'Dermatologist', 'mole': 'Dermatologist', 'eczema': 'Dermatologist',
    'bone': 'Orthopedic Surgeon', 'joint pain': 'Orthopedic Surgeon', 'fracture': 'Orthopedic Surgeon',
    'knee': 'Orthopedic Surgeon', 'arthritis': 'Orthopedic Surgeon', 'fever': 'General Physician',
    'cough': 'General Physician', 'cold': 'General Physician', 'sore throat': 'General Physician',
    'headache': 'Neurologist', 'migraine': 'Neurologist', 'dizziness': 'Neurologist',
    'numbness': 'Neurologist', 'ulcer': 'Dentist', 'mouth ulcer': 'Dentist',
    'mouth calculus': 'Dentist', 'calculus': 'Dentist', 'tooth caries': 'Dentist',
    'caries': 'Dentist', 'cavity': 'Dentist', 'toothache': 'Dentist',
}

def recommend_doctor(symptoms):
    """
    Recommends a doctor specialist based on user-provided symptoms.
    """
    symptoms_lower = symptoms.lower()
    for keyword, specialist in SYMPTOM_MAP.items():
        if keyword in symptoms_lower:
            return specialist, DOCTOR_DATABASE.get(specialist, [])
            
    # If no match, default to a General Physician
    return 'General Physician', DOCTOR_DATABASE.get('General Physician', [])

# --- End of Recommendation Logic ---


# ✅ Load trained model
try:
    model = tf.keras.models.load_model(r"C:\Users\abhis\OneDrive\c++\Hybrid Model\best_model.h5")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ✅ Class names
class_names = ['Calculus', 'Dental Caries', 'Ulcer']

# ✅ Page config
st.set_page_config(page_title="AI Health Assistant", page_icon="🩺", layout="wide")

# ✅ Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Detection", "Recommendation"])

# ---------------------------
# 🏠 HOME PAGE
# ---------------------------
if page == "Home":
    st.title("🩺 AI-Powered Health Assistant")
    st.markdown(
        """
        Welcome! This application combines AI-powered tools to help you manage your health.
        - **Image Detection:** Identify potential dental issues from an image.
        - **Doctor Recommendation:** Find the right specialist based on your symptoms.
        - **AI Chatbot:** Ask general health-related questions.

        *Navigate using the options on the left.*

        ⚠️ *Note: This app is for informational purposes and does not replace professional medical advice.*
        """
    )

# ---------------------------
# 🔍 DETECTION PAGE
# ---------------------------
elif page == "Detection":
    st.title("🦷 Dental Disease Detection")
    st.markdown("Upload an image for analysis and chat with our AI assistant below.")

    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("Image Analysis")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

        if uploaded_file is not None:
            try:
                pil_image = Image.open(uploaded_file).convert("RGB")
                st.image(pil_image, caption="Uploaded Image", use_container_width=True)

                with st.spinner('Analyzing the image...'):
                    # Preprocess image
                    img = pil_image.resize((224, 224))
                    img_array = image.img_to_array(img)
                    img_array = np.expand_dims(img_array, axis=0)
                    img_array /= 255.0

                    # Make prediction
                    prediction = model.predict(img_array)
                    prediction_label = class_names[np.argmax(prediction)]
                    confidence = np.max(prediction) * 100

                # Show prediction
                st.subheader("🔍 Prediction Results")
                st.metric(label="Detected Issue", value=prediction_label, delta=f"{confidence:.2f}% Confidence")
                
                if "Caries" in prediction_label:
                    st.warning("This is commonly known as tooth decay. We strongly recommend consulting a dentist.", icon="🦷")
                elif "Ulcer" in prediction_label:
                    st.error("If an ulcer persists for more than two weeks, please see a doctor.", icon="❗")
                elif "Calculus" in prediction_label:
                    st.error("Calculus, or tartar, requires professional cleaning by a dentist.", icon="❗")

            except Exception as e:
                st.error(f"❌ Error: Could not process the image.\n\n{e}")

    with col2:
        st.subheader("💬 Chat with our AI Health Bot")
        st.markdown("Ask any general health or dental-related questions!")
        
        # This URL points to the chatbot you run with 'python app.py'
        flask_chatbot_url = "http://127.0.0.1:5001"
        st.components.v1.iframe("https://cdn.botpress.cloud/webchat/v3.2/shareable.html?configUrl=https://files.bpcontent.cloud/2025/08/30/20/20250830203631-HW6WTM8B.json", height=600, scrolling=True)

# ---------------------------
# 👨‍⚕️ RECOMMENDATION PAGE
# ---------------------------
elif page == "Recommendation":
    st.title("👨‍⚕️ Find a Specialist")
    st.markdown("Describe your symptoms, and we'll suggest the right type of doctor for you.")
    
    with st.form("symptom_form"):
        symptoms = st.text_input("Enter your symptoms (e.g., 'toothache', 'skin rash', 'chest pain')", "")
        submitted = st.form_submit_button("Get Recommendation")

    if submitted and symptoms:
        with st.spinner("Finding a specialist..."):
            specialist, recommendations = recommend_doctor(symptoms)

            st.success(f"Based on your symptoms, we recommend seeing a **{specialist}**.")
            st.markdown("---")

            if recommendations:
                st.subheader("Here are some specialists you could consult:")
                for doctor in recommendations:
                    # Use columns for a card-like layout
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.image("https://placehold.co/100x100/3B82F6/FFFFFF?text=Dr.", use_container_width=True)
                    with col2:
                        st.subheader(f"{doctor['name']}")
                        st.write(f"**Location:** {doctor['location']}")
                        st.write(f"**Rating:** {'⭐' * int(round(doctor['rating']))} ({doctor['rating']})")
            else:
                st.warning(f"We couldn't find any doctors listed for the specialty: {specialist}.")
    elif submitted and not symptoms:
        st.error("Please enter your symptoms in the text box above.")

