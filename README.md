# PDF-Image-Based-Retrieval-Augmented-Generation-RAG-System
This project enables the conversion of PDF pages into images, the generation of detailed explanations for those images using Ollama’s large language model (LLM), and embedding these explanations into a Chroma vector store for efficient querying. The system implements a retrieval-augmented generation (RAG) approach, allowing you to query the stored explanations and generate context-aware answers.

## Features
- **PDF to Image Conversion:** Convert each page of a PDF into an image.
- **Image Explanation Generation:** Generate detailed textual explanations for each image using Ollama’s LLM.
- **Chroma Vector Store:** Embed the explanations and their embeddings into a Chroma vector store for efficient querying.
- **RAG Framework:** Query the stored explanations with context and generate responses using Ollama.

## Folder Structure

```
/pdf_ss
│
├── pdf_ss.py                    # Script to convert PDF pages into images
├── embedding.py                 # Script to generate explanations and embed them into Chroma
├── embedding_stock/             # Folder to store the generated Chroma database
│   ├── explain/                 # Folder to persist the vector store
│
└── query.py                     # Script to query the stored embeddings and generate responses
```

## Prerequisites

Make sure you have Python 3.x installed along with the required libraries. You can install them using:

```bash
pip install langchain ollama pymupdf langchain-community pillow sentence-transformers chromadb
```

## Usage

### Step 1: Convert PDF to Images

Use the script `pdf_ss.py` to convert each page of a PDF document into an image.

#### Running `pdf_ss.py`:

```bash
python pdf_ss.py
```

This script will:
1. Convert each page of the provided PDF into a PNG image.
2. Save the images in the `output_images` directory.

### Step 2: Generate Explanations and Embed into Chroma

Once the images are generated, the script `embedding.py` is used for the following tasks:
1. **Generate Explanations:** For each image, Ollama’s LLM generates a detailed explanation based on the image content.
2. **Split the Explanations:** The generated explanations are split into smaller chunks for better storage and retrieval.
3. **Embed Explanations into Chroma:** The explanations (along with their embeddings) are stored in a Chroma vector store, located in `embedding_stock/explain`.

#### Running `embedding.py`:

```bash
python embedding.py
```

This script will:
1. Generate explanations for each image in the `output_images` folder using Ollama.
2. Split the explanations into smaller text chunks for improved retrieval performance.
3. Store the text chunks and their embeddings in the Chroma vector store under the `embedding_stock/explain` directory.

### Step 3: Query the Vector Store

After the explanations have been embedded into Chroma, you can use the `query.py` script to query the Chroma vector store. This script allows you to search for relevant explanations based on a query and generates context-aware responses using Ollama.

#### Running `query.py`:

```bash
python query.py
```

The script will:
1. Accept a query from the user.
2. Retrieve relevant explanations from the Chroma vector store based on the query.
3. Pass the retrieved context to Ollama to generate a detailed and context-aware response.

## Code Walkthrough

### `pdf_ss.py`

This script performs the following operations:
1. **Convert PDF pages to images:** Uses `PyMuPDF` to convert each page into a PNG image.
2. **Save the images:** Each image is saved in the `output_images` folder.

### `embedding.py`

This script performs the following tasks:
1. **Generate explanations:** For each image, the explanation is generated using Ollama’s LLM (`llava:7b`).
2. **Split explanations:** The explanations are split into smaller chunks using `CharacterTextSplitter` to facilitate efficient retrieval.
3. **Embed explanations:** The chunks of text and their embeddings are stored in the Chroma vector store under `embedding_stock/explain`.

### `query.py`

This script handles querying:
1. **Query input:** Accepts user input for a query.
2. **Retrieve relevant documents:** Uses Chroma to retrieve relevant explanations based on the query.
3. **Generate context-aware responses:** Passes the retrieved context to Ollama to generate a detailed response.

## Example Usage

### Step 1: Convert PDF to Images

Run the following command to convert the PDF into images and generate the embeddings:

```bash
python pdf_ss.py
```

This will create images from the PDF in the `output_images` directory and store the explanations in the Chroma vector store located in `embedding_stock/explain`.

### Step 2: Generate Explanations and Embed into Chroma

Once the images are converted, you need to generate explanations and embed them into the Chroma vector store:

```bash
python embedding.py
```

This will:
1. Generate explanations for each image.
2. Split the explanations into smaller chunks.
3. Store the embeddings in `embedding_stock/explain`.

### Step 3: Querying the Vector Store

Once the embeddings are stored, you can run the query script to interact with the system:

```bash
python query.py
```

The system will prompt you for a query. For example, you can enter: "How is satellogica different from it's competitors?" The system will retrieve the relevant explanations, pass them to Ollama, and return the generated response.

## Troubleshooting

- **Missing dependencies:** Ensure you have installed all required packages using the `pip` command above.
- **Ollama API issues:** Make sure you have access to Ollama’s API and are using the correct model identifier (`llava:7b`).
- **Chroma issues:** Ensure the `embedding_stock/explain` directory is writable and the Chroma vector store is set up correctly.

