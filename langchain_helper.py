import re
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, OpenAIEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

from prompts import question_prompt

# Load environment variables from .env file
load_dotenv()

# Instantiate embeddings tool
embeddings = OpenAIEmbeddings()


def create_vector_db_from_youtube_url(
    video_url: str, embeddings: OpenAIEmbeddings
) -> FAISS:
    """
    Create a vector database from a YouTube video URL.
    A vector database is a database that stores embeddings of text chunks.
    Args:
        video_url (str): The URL of the YouTube video
    Returns:
        db (FAISS): A vector database containing embeddings of text chunks
    """
    # Instantiate a YoutubeLoader
    loader = YoutubeLoader.from_youtube_url(video_url)
    # Load the document from the YouTube video
    # TODO: change if no English transcript
    transcript = loader.load()

    # Instantiate splitter with chunk size and overlap
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # Split the document into chunks
    docs = splitter.split_documents(transcript)

    # Create a vector database from the chunks
    db = FAISS.from_documents(docs, embeddings)

    # Return the vector database
    return db


def get_response_from_query(db: FAISS, query: str, k: int = 4) -> str:
    """
    Perform similarity search on the vector database and return the response
    Args:
        db (FAISS): A vector database containing embeddings of text chunks
        query (str): The query text
        k (int): The number of similar documents to return.
    Returns:
        response (str): The response text
    """

    # Perform similarity search on the vector database
    # k - number of similar documents to return
    # Default is 4 as it's close to 4096 tokens which gpt-3.5-turbo-instruct can handle in one request.
    docs = db.similarity_search(query, k=k)

    # Concatenate the page content of the similar documents
    docs_page_content = " ".join([doc.page_content for doc in docs])

    # Instantiate the OpenAI model
    llm = OpenAI(model="gpt-3.5-turbo-instruct")

    # Create a prompt template with input variables which will be filled in at runtime and the prompt text
    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template=question_prompt,
    )

    # Instantiate the LLMChain with the OpenAI model and the prompt template
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain with the query and the similar documents
    response = chain.run(question=query, docs=docs_page_content)

    # Replace newline characters with an empty string
    response = response.replace("\n", "")

    return response
