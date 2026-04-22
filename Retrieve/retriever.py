import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, CrossEncoder
 

BI_ENCODER_MODEL  = "intfloat/multilingual-e5-large"  
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
 
RETRIEVAL_TOP_K = 15   
RERANK_TOP_K    = 3    
 
 
def load_vector_database():
    doc_embedding = np.load("VectorDatabase/embeddings.npy", allow_pickle=True)
    texts         = np.load("VectorDatabase/texts.npy",      allow_pickle=True)
    bi_encoder    = SentenceTransformer(BI_ENCODER_MODEL)
    cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)
    return bi_encoder, cross_encoder, texts, doc_embedding
 
bi_encoder, cross_encoder, texts, doc_embedding = load_vector_database()

def retrieve_candidates(queries: list[str], top_k: int = RETRIEVAL_TOP_K) -> list[int]:
    prefixed = [f"query: {q}" for q in queries]
    query_embeddings = bi_encoder.encode(prefixed, normalize_embeddings=True)
 
    combined_scores: dict[int, float] = {}
 
    for q_emb in query_embeddings:
        scores  = cosine_similarity(q_emb.reshape(1, -1), doc_embedding)[0]
        indices = np.argsort(scores)[::-1][:top_k]
 
        for rank, idx in enumerate(indices):
            combined_scores[idx] = combined_scores.get(idx, 0) + 1 / (30 + rank)
 

    sorted_indices = sorted(combined_scores, key=combined_scores.get, reverse=True)
    return sorted_indices[:top_k]

def rerank(question: str, candidate_indices: list[int], top_k: int = RERANK_TOP_K) -> list[str]:

    candidates = [texts[idx] for idx in candidate_indices]
    pairs      = [(question, text) for text in candidates]
    scores     = cross_encoder.predict(pairs)
 
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [text for text, _ in ranked[:top_k]]

def hybrid_search(query: str, question: str, top_k: int = RERANK_TOP_K) -> list[str]:

    all_queries = list({query, question}) 
 
    candidate_indices = retrieve_candidates(all_queries, top_k=RETRIEVAL_TOP_K)
    results           = rerank(question, candidate_indices, top_k=top_k)
 
    return results
 
 
def retrieve(query: str, question: str, top_k: int = 5):
    all_queries      = [query, question]
    prefixed         = [f"query: {q}" for q in all_queries]
    query_embeddings = bi_encoder.encode(prefixed, normalize_embeddings=True)
 
    results = []
    for q_emb in query_embeddings:
        scores  = cosine_similarity(q_emb.reshape(1, -1), doc_embedding)[0]
        indices = np.argsort(scores)[::-1][:top_k]
        results.append(indices)
 
    return results[0], results[1]