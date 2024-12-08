
import os
from langchain_community.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings  # Open-source embeddings
import base64
from io import BytesIO
from PIL import Image as PILImage

# Initialize Ollama LLM for explanations
llm = Ollama(model="llava:7b")

# Function to convert image to Base64
def convert_to_base64(pil_image):

    if pil_image.mode == "RGBA":
        pil_image = pil_image.convert("RGB")  # Convert RGBA to RGB
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Path to the folder containing images
image_folder_path = r"E:/output_images"
persist_directory = r"E:/stock/explain"

# Initialize Hugging Face embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize an empty list to collect all documents
all_documents = []

# Iterate through all files in the folder
for file_name in os.listdir(image_folder_path):
    file_path = os.path.join(image_folder_path, file_name)
    
    try:
        # Open the image file
        pil_image = PILImage.open(file_path)
        
        # Convert the image to Base64
        image_b64 = convert_to_base64(pil_image)
        
        # Bind the image to the LLM context and invoke it
        llm_with_image_context = llm.bind(images=[image_b64])
        explanation = llm_with_image_context.invoke("Provide a detailed explanation about the image and its content.")
        print(f"Generated Explanation for {file_name}:", explanation)
        
        # Create a Document object for the explanation
        document = Document(page_content=explanation, metadata={"image_path": file_path})
        
        # Split the document into smaller chunks
        text_splitter = CharacterTextSplitter(chunk_size=750, chunk_overlap=100)
        doc_splits = text_splitter.split_documents([document])
        
        # Add the document splits to the collection
        all_documents.extend(doc_splits)
        
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Store the explanation and embeddings in Chroma
vectorstore = Chroma.from_documents(
    documents=all_documents,
    collection_name="image-explanations",
    embedding=embedding_model,
    persist_directory=persist_directory
)

# Persist the vectorstore
vectorstore.persist()

print("All explanations and embeddings successfully stored in the Chroma database.")
