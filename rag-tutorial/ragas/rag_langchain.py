import operator
from typing import Optional, Sequence

from langchain_core.callbacks import Callbacks
from langchain_core.documents import BaseDocumentCompressor, Document

import requests


class LlamaCppReranker(BaseDocumentCompressor):
    url: str = "http://localhost:8080/reranking"

    top_n: int = 3
    """Number of documents to return."""

    def compress_documents(
            self,
            documents: Sequence[Document],
            query: str,
            callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        payload = {
            # "model": "大小寒学AI",
            "query": query,
            "top_n": self.top_n,
            "documents": [item.page_content for item in documents]
        }
        response = requests.post(self.url, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            scores = response_json.get("results", [])
            scores = [score_item.get("relevance_score") for score_item in scores]
            # return []
            docs_with_scores = list(zip(documents, scores))
            # lambda x:x[1]
            result = sorted(docs_with_scores, key=operator.itemgetter(1), reverse=True)
            return [doc for doc, _ in result[: self.top_n]]
        else:
            raise Exception("Failed to compress_documents")


import chromadb
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import CrossEncoder

from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder


def get_metadata_str(metadata):
    if metadata is None:
        return ""
    _str = ""
    # (key, value)
    for key, value in metadata.items():
        _str += f"{key}:{value}\n"
    return _str


class RagLangChain():
    def __init__(self,
                 collection_name: str = "rag-video-collection",
                 host: str = "localhost",
                 port: int = 8000):
        self.collection_name = collection_name
        self.host = host
        self.port = port

    def __get_vector_store(self):
        chromadb_client = chromadb.HttpClient(host=self.host, port=self.port)
        embedding_fn = OllamaEmbeddings(model="nomic-embed-text:latest")

        vector_store = Chroma(collection_name=self.collection_name,
                              client=chromadb_client,
                              embedding_function=embedding_fn
                              )
        return vector_store

    def delete_collection(self):
        vector_store = self.__get_vector_store()
        vector_store.delete_collection()

    def add_file(self, file_path: str, metadata=None):
        loader = TextLoader(file_path)

        docs = loader.load()
        text_spliter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
        all_splits = text_spliter.split_documents(docs)

        if metadata is not None:
            for split_item in all_splits:
                split_metadata = split_item.metadata
                split_item.metadata = {**split_metadata, **metadata}

        vector_store = self.__get_vector_store()
        ids = vector_store.add_documents(documents=all_splits)
        return ids

    def __query_vector(self, info):
        vector_store = self.__get_vector_store()
        retriever = vector_store.as_retriever(
            # search_type="mmr",
            # search_kwargs={"k": 16, "fetch_k": 20, "lambda_mult": 0.1}
            search_kwargs={"k": 20}
        )

        # Document对象,id/page_content/metadata
        # docs = retriever.invoke(info["query"])

        # model = CrossEncoder("BAAI/bge-reranker-large")
        # # question = "2024年中东非智能手机的出货量为多少？"
        # scores = model.predict([(info["query"], doc_item.page_content) for doc_item in docs])
        # # [(score, Document), (score, Document), ...]
        # sorted_list = sorted(zip(scores, docs), reverse=True, key=lambda x:x[0])
        # docs = [doc for _, doc in sorted_list]
        # docs = docs[:4]

        # 2. 使用langchain的CrossEncoder进行重排
        # model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-large")
        # compressor = CrossEncoderReranker(
        #     model=model,
        #     top_n=4,
        # )
        compressor = LlamaCppReranker(
            url="http://localhost:11433/reranking",
            top_n=4
        )
        compressor_retriever = ContextualCompressionRetriever(
            base_retriever=retriever,
            base_compressor=compressor,
        )

        docs = compressor_retriever.invoke(info["query"])
        return docs
#         # (0, item0), (1, item1)
#         for index, doc_item in enumerate(docs):
#             print(f"文档片段{index}")
#             print(doc_item)
#             print("*" * 80)
#         # docs_str = "\n\n".join(doc.page_content for doc in docs)
#         docs_str = "\n\n".join(f"""
# {get_metadata_str(doc.metadata)}
# {doc.page_content}""" for doc in docs)
#         # print(f"@@@@@{docs_str}")
#         return docs_str

    def query(self, question: str):
        prompt = ChatPromptTemplate.from_template("""
你是一个问答机器人。你的任务是根据下述给定的已知信息回答用户问题。

已知信息:
{context}
用户问题：
{query}
如果已知信息不包含用户问题的答案，或者已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。
请不要输出已知信息中不包含的信息或答案。
请用中文回答用户问题。
""")

        llm = ChatOllama(model="qwen2.5:latest")

        output_parser = StrOutputParser()
        retrieved_docs = self.__query_vector({"query":question})
        # 返回值: {"query": "XXXX", "context": "XXXXX2"}
        # chain = ({"context": self.__query_vector, "query": lambda x: x["query"]} | prompt | llm | output_parser)
        chain = (prompt | llm | output_parser)
        docs_str = "\n\n".join(f"""
        # {get_metadata_str(doc.metadata)}
        # {doc.page_content}""" for doc in retrieved_docs)
        result = chain.invoke({
            "query": question,
            "context": docs_str
        })
        return result, retrieved_docs
