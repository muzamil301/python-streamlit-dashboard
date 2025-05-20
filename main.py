import streamlit as st
import dashboard
import user_profiles

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "User Profiles"])

if page == "Dashboard":
    dashboard.run()
elif page == "User Profiles":
    user_profiles.run()