from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    return model.encode(text).tolist()


def get_embeddings(texts, batch_size=32):
    return model.encode(texts, batch_size=batch_size, show_progress_bar=False).tolist()