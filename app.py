import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File to store data
DATA_FILE = "travel_experiences.csv"
IMAGE_FOLDER = "uploaded_images"

# Create folder if not exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Load existing data
if os.path.exists(DATA_FILE):
    experiences = pd.read_csv(DATA_FILE)
else:
    experiences = pd.DataFrame(columns=["Name", "Location", "Experience", "Image", "Date"])

st.set_page_config(page_title="GAMANAM - Travel Experiences", layout="wide")

st.title("🌏 GAMANAM - Share Your Travel Experience")
st.write("Preserve India's cultural heritage by sharing your unique travel stories.")

# Form to submit experience
with st.form("experience_form", clear_on_submit=True):
    name = st.text_input("Your Name")
    location = st.text_input("Place / Location Visited")
    experience_text = st.text_area("Describe Your Experience")
    image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Submit Experience")

    if submitted:
        if name and location and experience_text:
            image_path = ""
            if image_file:
                image_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.name}"
                image_path = os.path.join(IMAGE_FOLDER, image_filename)
                with open(image_path, "wb") as f:
                    f.write(image_file.read())

            # Save to dataframe
            new_entry = {
                "Name": name,
                "Location": location,
                "Experience": experience_text,
                "Image": image_path,
                "Date": datetime.now().strftime("%Y-%m-%d")
            }
            experiences = pd.concat([experiences, pd.DataFrame([new_entry])], ignore_index=True)
            experiences.to_csv(DATA_FILE, index=False)

            st.success("✅ Your travel experience has been submitted!")
        else:
            st.error("⚠️ Please fill all required fields.")

st.subheader("📌 Recent Travel Experiences")

if not experiences.empty:
    for idx, row in experiences[::-1].iterrows():  # Show latest first
        st.markdown(f"### {row['Location']} — by {row['Name']} ({row['Date']})")
        st.write(row['Experience'])
        if row['Image'] and os.path.exists(row['Image']):
            st.image(row['Image'], use_column_width=True)
        st.markdown("---")
else:
    st.info("No travel experiences yet. Be the first to share!")

