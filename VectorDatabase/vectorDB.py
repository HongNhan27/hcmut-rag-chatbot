import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from Chunk.chunkingData import chunkData, loadData
def create_vector_database():
    
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    documents = loadData()
    chunks = chunkData(documents)
    
    texts = [chunk.page_content for chunk in chunks]
    doc_embedding = model.encode(texts)
    np.save("VectorDatabase/embeddings.npy", doc_embedding)
    np.save("VectorDatabase/texts.npy", texts)
    return model, texts, doc_embedding

if __name__ == "__main__":
    create_vector_database()

