import streamlit as st
import requests
import pandas as pd

@st.cache  # Cache responses for performance
def fetch_data(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data from {endpoint}")
        return None

def run():
    users = fetch_data("https://jsonplaceholder.typicode.com/users")
    users_df = pd.DataFrame(users)

    st.header("User Profiles")

    st.subheader("View All User Profiles")
    st.dataframe(users_df[['name', 'email', 'website', 'phone']])

    selected_profile = st.selectbox(
        "Select a User to View Details",
        options=users_df['name'],
    )

    user_details = users_df[users_df['name'] == selected_profile].iloc[0]
    
    st.write("### User Details")
    st.write(f"- **Name**: {user_details['name']}")
    st.write(f"- **Email**: {user_details['email']}")
    st.write(f"- **Phone**: {user_details['phone']}")
    st.write(f"- **Website**: {user_details['website']}")
    st.write(f"- **Company Name**: {user_details['company']['name']}")
    st.write(f"- **Address**: {user_details['address']['suite']}, {user_details['address']['street']}, {user_details['address']['city']}")

    st.subheader("User Locations")
    geodata = pd.DataFrame(
        [{
            "lat": float(user['address']['geo']['lat']),
            "lon": float(user['address']['geo']['lng']),
            "name": user['name']
        } for user in users]
    )

    st.map(geodata)