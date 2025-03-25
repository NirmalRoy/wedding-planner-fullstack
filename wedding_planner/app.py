import streamlit as st
import requests

# URLs for your Cloud Functions
GET_VENUES_URL = "https://us-central1-nirmal-maven.cloudfunctions.net/get_venues"
SEARCH_VENUES_URL = "https://us-central1-nirmal-maven.cloudfunctions.net/search_venues_basic"

# Fetch options for dropdowns
def get_options():
    response = requests.get(GET_VENUES_URL)
    if response.status_code == 200:
        data = response.json()
        return data["venue_styles"], data["locations"], data["capacities"]
    else:
        st.error("Failed to load options. Try again later.")
        return [], [], []

# Main app
st.title("Wedding Venue Finder")

# Load dropdown options
venue_styles, locations, capacities = get_options()

# Dropdowns
style = st.selectbox("Venue Style", ["Select a style"] + venue_styles)
location = st.selectbox("Location", ["Select a location"] + locations)
capacity = st.selectbox("Guest Capacity", ["Select a capacity"] + capacities)

# Search button
if st.button("Find Venues"):
    if style == "Select a style" or location == "Select a location" or capacity == "Select a capacity":
        st.warning("Please select all options.")
    else:
        # Call search_venues_basic
        payload = {
            "venue_style": style,
            "location": location,
            "guest_capacity": capacity
        }
        response = requests.post(SEARCH_VENUES_URL, json=payload)
        if response.status_code == 200:
            venues = response.json().get("venues", [])
            if venues:
                st.subheader("Matching Venues")
                for venue in venues:
                    st.write(f"**{venue['venue_name']}**")
                    st.write(f"Location: {venue['location']}")
                    st.write(f"Capacity: {venue['guest_capacity']}")
                    st.write(f"About: {venue['about']}")
                    st.write("---")
            else:
                st.info("No venues found for these selections.")
        else:
            st.error("Search failed. Please try again.")

# Run with: streamlit run app.py