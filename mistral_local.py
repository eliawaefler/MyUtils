from openai import OpenAI


from transformers import AutoTokenizer, AutoModel
import torch
from nomic import Atlas

# Load model and tokenizer
model_name = "mistral-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to get embeddings
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state
    sentence_embedding = torch.mean(embeddings, dim=1)
    return sentence_embedding.detach().numpy()

# Example texts
texts = ["This is a sample sentence.", "Here is another example."]

# Generate embeddings for each text
embeddings = [get_embeddings(text) for text in texts]

# Initialize Atlas
atlas = Atlas()

# Create a dictionary of text and their corresponding embeddings
data = [{"text": text, "embedding": embedding.tolist()} for text, embedding in zip(texts, embeddings)]

# Add data to Atlas
atlas.add_data(data)

# Visualize the embeddings
atlas.visualize()
