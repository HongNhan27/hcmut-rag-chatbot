from langchain_community.document_loaders import JSONLoader, TextLoader
import os
from langchain_text_splitters import CharacterTextSplitter
def loadData():

    data_folder = "Data"
    documents = []

    for file in os.listdir(data_folder):

        path = os.path.join(data_folder, file)

        # load jsonl
        if file.endswith(".jsonl"):

            loader = JSONLoader(
                file_path=path,
                jq_schema=".",
                content_key="text",
                json_lines=True
            )

            documents.extend(loader.load())

        # load txt
        elif file.endswith(".txt"):

            loader = TextLoader(path, encoding="utf-8")

            documents.extend(loader.load())

    print("Loaded documents:", len(documents))
    print(documents[0].page_content[:200])

    return documents
def chunkData(documents, chunk_size = 400, chunk_overlap = 100):
    text_spliter = CharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        separator = "\n"
    )
    
    chunks = text_spliter.split_documents(documents)
    
    return chunks
if __name__ == "__main__":
    documents = loadData()
    chunks = chunkData(documents)
    print(len(chunks))
    for i, chunk in enumerate(chunks):
        print(f"-----chunk {i+ 1} -----")
        print(chunk.page_content)