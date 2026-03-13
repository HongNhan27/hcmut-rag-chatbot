import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


def load_vector_database():

    # Load embeddings và texts đã lưu
    doc_embedding = np.load("VectorDatabase/embeddings.npy", allow_pickle=True)
    texts = np.load("VectorDatabase/texts.npy", allow_pickle=True)

    # Load embedding model
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    return model, texts, doc_embedding

model, texts, doc_embedding = load_vector_database()

def retrieve(query: str, question: str, top_k: int = 5):

    query_embedding = model.encode([query], normalize_embeddings=True)

    scores = cosine_similarity(query_embedding, doc_embedding)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]

    question_embedding = model.encode([question], normalize_embeddings=True)

    scores_question = cosine_similarity(question_embedding, doc_embedding)[0]
    top_indices_question = np.argsort(scores_question)[::-1][:top_k]

    return top_indices, top_indices_question

def hybrid_search(query: str, question: str, top_k=3):

    query_indices, question_indices = retrieve(query, question)

    combined_scores = {}

    for rank, idx in enumerate(query_indices):
        combined_scores[idx] = combined_scores.get(idx, 0) + 1/(30 + rank)

    for rank, idx in enumerate(question_indices):
        combined_scores[idx] = combined_scores.get(idx, 0) + 1/(30 + rank)

    sorted_indices = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    return [texts[idx] for idx, score in sorted_indices[:top_k]]
