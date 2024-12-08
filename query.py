from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import ollama

# Initialize the embedding function (using HuggingFace embeddings)
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load Chroma as a retriever
persist_directory = "explain"  # Your Chroma database folder
vector_store = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_function
)

retriever = vector_store.as_retriever()

# Define a custom prompt template for your RAG pipeline
prompt_template = """
You are an expert assistant. Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

# Function to use Ollama for generating responses
def ollama_generate(prompt):
    """
    Generate a response using the Ollama API.

    Args:
        prompt (str): The input prompt for the model.

    Returns:
        str: The generated response text.
    """
    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
    
    # Check if the response has the desired field
    if hasattr(response, "content"):
        return response.content  # Access content if it's directly available
    elif isinstance(response, dict) and "content" in response:
        return response["content"]  # For JSON-like responses
    else:
        raise ValueError(f"Unexpected response format: {response}")

# Create a Retrieval-QA Chain with a custom function for Ollama
def rag_with_ollama(query):
    """
    Perform Retrieval-Augmented Generation (RAG) using Chroma for retrieval
    and Ollama for generating the final response.

    Args:
        query (str): The user question or query.

    Returns:
        str: The generated response from Ollama.
    """
    # Retrieve relevant documents from Chroma
    results = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in results])

    # Combine context and query into a final prompt
    final_prompt = prompt.template.format(context=context, question=query)

    # Get the generated answer from Ollama
    answer = ollama_generate(final_prompt)
    return answer

# Command-line interactive input
def main():
    # Prompt the user to enter a query
    query = input("Please enter your query: ")
    
    # Process the query and get the answer
    try:
        result = rag_with_ollama(query)
        print("Generated Answer:", result)
    except Exception as e:
        print("An error occurred:", e)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
