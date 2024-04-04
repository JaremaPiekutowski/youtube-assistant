import textwrap

import streamlit as st

import langchain_helper as lch

# Set page title
st.title("YouTube Assistant")

# Add sidebar
with st.form(key="my_form"):
    with st.sidebar:
        youtube_url = st.sidebar.text_area(
            label="What is the YouTube video URL?",
            max_chars=50
        )
        query = st.sidebar.text_area(
            label="Ask me about the video?",
            max_chars=100,
            key="query"
        )
        submit_button = st.form_submit_button(label="Submit")


if query and youtube_url and submit_button:
    # Create a vector database from the YouTube video URL
    db = lch.create_vector_db_from_youtube_url(
        video_url=youtube_url,
        embeddings=lch.embeddings
        )

    # Get response from the query
    response = lch.get_response_from_query(
        db=db,
        query=query,
        k=4
    )

    # Add subheader and display the response
    st.subheader("Answer:")
    st.text(textwrap.fill(response, width=80))
