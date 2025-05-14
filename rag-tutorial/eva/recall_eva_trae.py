"""
python文件说明：
1. 需要启动chromadb服务端，使用chroma run启动
  - host: localhost
  - port: 8000
  - collection_name: rag-video-collection
2. 需要本地启动ollama，并有"qwen2.5:latest"模型提供服务
3. 需要启动llama.cpp的CrossEncoder(交叉编码器)服务,命令如下:
  llama-server -m bge-reranker-large-f16.gguf --port 11433  --reranking --pooling rank
  (说明：确保启动命令的当前目录下有"bge-reranker-large-f16.gguf"模型文件)
"""
"""
使用langchain 0.3.14版本 实现如下功能：
1. 分批从./questions.txt文件中读取数据，每次读取10条。该文件中一行为一条数据，
数据格式为：
{"question": "问题1", "id": "xxx"}
其中question为问题，格式为中文，请正确读取。
2. 将1中读取到的数据逐条到chromadb当中进行检索，在检索到的结果当中，记录如下
连个指标：
（1）命中率：从chromadb检索到的数据中，如果包含问题对应的id，则记录命中一次；
（2）MRR：mean reciprocal rank，平均倒数排名，计算公式为：
    1 / (rank + 1)，其中rank为检索到的结果中，问题对应的id所在的位置。
3. 计算2中记录的两个指标的平均值，作为本次检索的评估指标。
4. 输出2中记录的两个指标的平均值。
5. 使用chromadb客户端的方式连接到chromadb服务端，使用默认的配置。
    由于使用了langchain，请使用Chroma类来连接chromadb服务端。
    from langchain_chroma import Chroma
    chromadb的连接信息：
    - host: localhost
    - port: 8000
    - collection_name: rag-video-collection
    - embedding_function: OllamaEmbeddings(model="nomic-embed-text:latest")
6. 请将上面的需求封装到 RecallEva 类当中，提供一个 run 方法，用于运行评估。
"""


from langchain.retrievers.document_compressors.cross_encoder import BaseCrossEncoder
import requests
from langchain_core.documents import BaseDocumentCompressor, Document
from langchain_core.callbacks import Callbacks
from typing import Optional, Sequence
import operator
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import ContextualCompressionRetriever
import chromadb
import json


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
            scores = [score_item.get("relevance_score")
                      for score_item in scores]
            # return []
            docs_with_scores = list(zip(documents, scores))
            # lambda x:x[1]
            result = sorted(docs_with_scores,
                            key=operator.itemgetter(1), reverse=True)
            return [doc for doc, _ in result[: self.top_n]]
        else:
            raise Exception("Failed to compress_documents")


class RecallEva:
    def __init__(self):
        # 初始化嵌入函数
        self.embedding_function = OllamaEmbeddings(
            model="nomic-embed-text:latest")
        # 连接到 ChromaDB 服务端
        self.chroma = Chroma(
            client=chromadb.HttpClient(
                host="localhost",
                port=8000,
            ),
            collection_name="rag-video-collection",
            embedding_function=self.embedding_function,
            # client_settings={
            #     "host": "localhost",
            #     "port": "8000"
            # }
        )

    def read_questions_in_batches(self, offset, batch_size=10):
        """
        分批从 questions.txt 文件中读取问题数据。

        :param batch_size: 每批读取的问题数量，默认为 10。
        :return: 分批的问题数据列表。
        """
        with open('./questions.txt', 'r', encoding='utf-8') as file:
            # 跳过offset之前的行
            for _ in range(offset):
                line = file.readline()
                if not line:
                    return []
            questions = []
            for _ in range(batch_size):
                line = file.readline()
                if not line:
                    break
                try:
                    question_data = json.loads(line)
                    questions.append(question_data)
                except json.JSONDecodeError:
                    print(f"Error parsing JSON line: {line}")
            return questions

    def query_from_vectorstore(self, question):
        retriever = self.chroma.as_retriever(
            # search_type="mmr",
            # search_kwargs={"k": 16, "fetch_k": 20, "lambda_mult": 0.1}
            search_kwargs={"k": 20}
        )

        compressor = LlamaCppReranker(
            url="http://localhost:11433/reranking",
            top_n=4
        )
        compressor_retriever = ContextualCompressionRetriever(
            base_retriever=retriever,
            base_compressor=compressor,
        )

        docs = compressor_retriever.invoke(question)
        return docs

    def run(self):
        """
        运行评估流程，计算命中率和 MRR 指标的平均值并输出。
        """
        total_hits = 0
        total_mrr = 0
        total_questions = 0
        offset = 0
        batch_size = 10
        # batches = self.read_questions_in_batches()
        # for batch in batches:
        while True:
            batch = self.read_questions_in_batches(offset, batch_size)
            if not batch:
                break
            offset += batch_size
            for question_data in batch:
                question = question_data["question"]
                document_id = question_data["id"]
                # 从 ChromaDB 中检索数据
                # Document[]: {id: 'xx', page_conent: 'xxx'}
                # results = self.chroma.similarity_search(question, k=20)
                results = self.query_from_vectorstore(question)
                # hit = False
                for rank, result in enumerate(results):
                    if result.id == document_id:
                        total_hits += 1
                        total_mrr += 1 / (rank + 1)
                        # hit = True
                        break
                # if not hit:
                #     total_mrr += 0
                total_questions += 1

        if total_questions == 0:
            avg_hit_rate = 0
            avg_mrr = 0
        else:
            avg_hit_rate = total_hits / total_questions
            avg_mrr = total_mrr / total_questions

        print(f"平均命中率: {avg_hit_rate}")
        print(f"平均 MRR: {avg_mrr}")
        return avg_hit_rate, avg_mrr


if __name__ == "__main__":
    recall_eva = RecallEva()
    recall_eva.run()
