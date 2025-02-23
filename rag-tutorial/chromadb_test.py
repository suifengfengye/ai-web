from chromadb.utils import embedding_functions
import chromadb
import uuid
import asyncio

st_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="nomic-ai/nomic-embed-text-v2-moe",
    cache_folder="./models",
    trust_remote_code=True
)

async def main(documents):
    a_client = await chromadb.AsyncHttpClient(host='localhost', port=8000)
    collection = await a_client.get_or_create_collection(
        name="my_collection_03",
        embedding_function=st_ef,
    )
    ids = [uuid.uuid4().hex for _ in range(len(documents))]
    await collection.add(ids=ids, documents=documents)
    results = await collection.query(query_texts=["0001"], n_results=4)
    print(results)

if __name__ == "__main__":
    documents = ["文档0001", "文档0002"]
    asyncio.run(main(documents))