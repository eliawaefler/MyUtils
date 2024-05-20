from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # Choose a model that suits your needs


def get_embedding(text: str) -> list:
    return model.encode(text)


def get_embeddings(texts: list[str]) -> list:
    return [get_embedding(t) for t in texts]


if __name__ == '__main__':
    embedding = get_embedding("any text to embed")
    print(len(embedding))
