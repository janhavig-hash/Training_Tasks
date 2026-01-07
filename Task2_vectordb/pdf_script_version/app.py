import requests
import chromadb
import json
from pypdf import PdfReader

import numpy as np

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


#connect to chromadb
client = chromadb.Client()
collection = client.create_collection(name = "policies")

#Function to Get the embedding model from ollama
def get_embedding(text):
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model" : "nomic-embed-text",
        "prompt": text
    }

    response = requests.post(url, json = payload)
    response.raise_for_status()
    return response.json()["embedding"]

#Read the text from pdf

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


#split the text into chunks 
def split_text(text, chunk_size = 400):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [] 

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

#Load pdf and store the embeddings
pdf_path = "RAG_pdf.pdf" 
pdf_text = read_pdf(pdf_path)

chunks = split_text(pdf_text)

print(f"Loaded {len(chunks)} chunks from PDF")

for i, chunk in enumerate(chunks):
    embedding = get_embedding(chunk)
    collection.add(
        documents = [chunk],
        embeddings = [embedding],
        ids = [f"chunk_{i}"]
    )

print("Pdf content stored in vectore DB ")

#save embedding to file
data = collection.get(include=["embeddings"])

if len(data["embeddings"]) == 0:
    print(" No embeddings found in collection.")
else:
    sample_embedding = data["embeddings"][0][:50].tolist() # first 50 values

    with open("embedding_sample.json", "w") as f:
        import json
        json.dump(sample_embedding, f, indent=2)

    print(" Saved sample embedding to embedding_sample.json")

# Query 


COSINE_THRESHOLD = 0.55

while True:
    user_query = input("\nAsk a Question (or type 'EXIT'): ")

    if user_query.lower() == "exit":
        print("Thank you for asking. Goodbye !!")
        break

    query_embedding = get_embedding(user_query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1,
        include=["documents", "embeddings"]
    )

    matched_doc = results["documents"][0][0]
    matched_embedding = results["embeddings"][0][0]

    similarity = cosine_similarity(query_embedding, matched_embedding)

    print(f"\n Cosine Similarity Score: {similarity:.3f}")

    if similarity < COSINE_THRESHOLD:
        print(" No relevant data found for this question.")
    else:
        print("\n Best Match:")
        print(matched_doc[:500], "...")

        print("\n Embedding Vector (first 20 values):")
        print(matched_embedding[:20])