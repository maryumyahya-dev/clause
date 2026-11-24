from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from qdrant_client.models import Distance, VectorParams, SparseVectorParams

from app.core.config import get_embeddings, get_qdrant_client, get_settings


def main():
    settings = get_settings()
    client = get_qdrant_client(settings)
    embeddings = get_embeddings(settings)

    # 1) Collection banao agar nahi hai
    if not client.collection_exists(settings.collection_name):
        dim = len(embeddings.embed_query("test"))  # embedding size khud nikal lo
        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config={"dense": VectorParams(size=dim, distance=Distance.COSINE)},
            sparse_vectors_config={"sparse": SparseVectorParams()},
        )

    # 2) Handbook load karo aur chunks banao
    docs = PyPDFLoader("files/shop_handbook.pdf").load()   # apna sahi path do
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    # 3) Qdrant mein daalo
    store = QdrantVectorStore(
        client=client,
        collection_name=settings.collection_name,
        embedding=embeddings,
        retrieval_mode=RetrievalMode.HYBRID,
        sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
        vector_name="dense",
        sparse_vector_name="sparse",
    )
    store.add_documents(chunks)
    print(f"{len(chunks)} chunks ingest ho gaye")
    client.close()


if __name__ == "__main__":
    main()