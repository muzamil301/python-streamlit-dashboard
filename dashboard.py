import streamlit as st
import requests
import pandas as pd

@st.cache
def fetch_data(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data from {endpoint}")
        return None

def run():
    posts = fetch_data("https://jsonplaceholder.typicode.com/posts")
    users = fetch_data("https://jsonplaceholder.typicode.com/users")

    posts_df = pd.DataFrame(posts)
    users_df = pd.DataFrame(users)

    selected_user = st.sidebar.selectbox(
        "Filter Posts by User",
        options=users_df['name'],
        index=0
    )
    selected_user_id = users_df[users_df['name'] == selected_user]['id'].values[0]
    filtered_posts = posts_df[posts_df['userId'] == selected_user_id]

    st.header(f"Posts by {selected_user}")
    st.write(filtered_posts[['title', 'body']])

    st.subheader("Post Statistics: Number of Posts by User")
    post_stats = posts_df['userId'].value_counts().sort_index()
    st.bar_chart(post_stats)

    st.subheader("Search Posts by Keyword")
    search_term = st.text_input("Enter a Keyword to Search in Posts")
    if search_term:
        search_results = posts_df[posts_df['body'].str.contains(search_term, case=False, na=False)]
        st.write(search_results[['title', 'body']])
    else:
        st.write("Enter a keyword to filter posts.")

    comments = fetch_data("https://jsonplaceholder.typicode.com/comments")
    comments_df = pd.DataFrame(comments)

    st.subheader("Comments on Posts")
    if st.checkbox("Show comments for posts"):
        st.write(comments_df[['postId', 'name', 'body']])