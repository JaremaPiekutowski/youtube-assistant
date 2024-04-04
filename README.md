# YouTube Assistant

YouTube Assistant is a Streamlit application designed to provide insights and answers about YouTube videos based on their transcripts. By utilizing a combination of the LangChain library and OpenAI's embeddings, this app can create a vector database from a YouTube video's transcript and perform similarity searches to answer user queries.

Created based on freeCodeCamp's [Langchain Crash Course for Beginners](https://www.youtube.com/watch?v=lG7Uxts9SXs).

## Requirements

To run the YouTube Assistant app, you will need:

- Python 3.6+
- Streamlit
- LangChain
- FAISS for vector storage and similarity search
- OpenAI API for embeddings and language model queries
- `youtube_transcript_api` for fetching YouTube video transcripts
- A `.env` file containing your OpenAI API key

## Installation

1. Clone the repository to your local machine:

   ```sh
   git clone https://your-repository-url-here.git
   cd your-repository-directory
   ```

2. Install the required Python packages:

    ```sh
    pip install streamlit langchain langchain-community faiss-cpu python-dotenv openai youtube_transcript_api


3. Create a .env file in the root directory of your project and add your OpenAI API key:

    ```
    OPENAI_API_KEY='your_openai_api_key_here'
    ```
# Usage

1. Start the Streamlit app:

    ```sh
    streamlit run main.py
    ```

2. Open your web browser and navigate to the URL provided by Streamlit, usually http://localhost:8501.

3. In the sidebar, enter the URL of the YouTube video you're interested in and the question you want to ask about the video.

4. Click the "Submit" button to process your query. The app will then display the answer based on the video's transcript.

# How It Works

The app extracts the transcript of the provided YouTube video URL using youtube_transcript_api and creates a vector database of the transcript's text. When a user submits a query, it performs a similarity search in this database to find relevant parts of the transcript and uses a language model to generate a coherent and contextually relevant answer.

# Contributing

Contributions to improve YouTube Assistant are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

