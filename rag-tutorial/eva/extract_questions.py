"""
python文件说明：
1. 需要启动chromadb服务端，使用chroma run启动
  - host: localhost
  - port: 8000
  - collection_name: rag-video-collection
2. 需要本地启动ollama，并有"qwen2.5:latest"模型提供服务
"""
"""
使用langchain 0.3.14版本 实现如下功能：
（1）使用客户端 HttpClient 连接的方式连接到chromadb,chromadb的连接信息如下：
 - host: "localhost" 
 - port: 8000
 - collection_name: "rag-video-collection"
 （2）分批从chromadb当中取出文档片段，每次取出10条。
 （3）遍历每个批次当中的文档片段，结合提示词传递给Ollama提供的LLM服务当中。
    - 1. 提示词信息如下：
    背景信息如下：----------------------------------------
    {context}
    ----------------------------------------
    根据提供的背景信息（而非先前的知识），仅基于以下查询生成问题。
    你是一名教师/教授。你的任务是为即将到来的测验/考试设置 {num_questions_per_chunk} 个问题。
     这些问题应覆盖文档中的不同方面。限制问题范围在提供的背景信息内。
     将你的回复作为一个 JSON 块返回，包含 “questions” 键，“questions” 键对应的值为一个字符串列表，也就是问题列表。

    - 2. Ollama信息如下： url为默认即可。模型使用"qwen2.5:latest"
    （4）遍历(3)当中得到的问题列表，将每个问题和对应的文档片段ID作为一条记录，
    追加保存到"./questions.txt"文件当中。 问题和文档片段ID的数据结构:{"id": "xxx1", "question": "具体问题xxx"}
    （5）将上面的要求封装到ExtractQuestion类当中
"""

import chromadb
import json
from langchain_chroma import Chroma
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class ExtractQuestion:
    def __init__(self,
                 host="localhost",
                 port=8000,
                 collection_name="rag-video-collection",
                 model_name="qwen2.5:latest",
                 num_questions_per_chunk=3):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.model_name = model_name
        self.num_questions_per_chunk = num_questions_per_chunk
        self.prompt_template = """背景信息如下：----------------------------------------
{context}
----------------------------------------
根据提供的背景信息（而非先前的知识），仅基于以下查询生成问题。
你是一名教师/教授。你的任务是为即将到来的测验/考试设置 {num_questions_per_chunk} 个问题。
这些问题应覆盖文档中的不同方面。限制问题范围在提供的背景信息内。
将你的回复作为一个 JSON 块返回，包含 “questions” 键，“questions” 键对应的值为一个字符串列表，也就是问题列表。"""

    # 从chromadb当中获取文档片段列表
    def fetch_documents(self, offset=0, limit=10):
        chromadb_client = chromadb.HttpClient(
            host=self.host,
            port=self.port
        )
        embedding_fn = OllamaEmbeddings(
            model="nomic-embed-text:latest"
        )
        vectorstore = Chroma(
            client=chromadb_client,
            collection_name=self.collection_name,
            embedding_function=embedding_fn
        )
        # {"ids": [], "documents": []}
        doc_infos = vectorstore.get(
            limit=limit,
            offset=offset
        )
        return doc_infos

    def generate_questions(self, context):
        # 根据传入的context,调用langchain提供的功能，结合self.prompt_template,
        # 生成内容
        prompt = ChatPromptTemplate.from_template(self.prompt_template)
        llm = ChatOllama(model=self.model_name)
        chain = prompt | llm | JsonOutputParser()
        try:
            # {"questions": []}
            result = chain.invoke(
                {"context": context, "num_questions_per_chunk": self.num_questions_per_chunk}
            )
            return result["questions"]
        except Exception as e:
            print(f" error occurred, {e}")
            return []

    def save_questions(self, questions, id):
        # 遍历 questions, 将每一个元素结合id,组成一个json数据{"id": "xxx", "question": "xx"}
        # 保存到当前文件夹当中的 "./questions.txt" 文件当中
        questions_with_id = [{"id": id, "question": question}
                             for question in questions]
        with open("./questions.txt", "a") as f:
            for question_with_id in questions_with_id:
                f.write(json.dumps(question_with_id) + "\n")

    def extract_questions(self):
        """
        1. 循环调用 self.fetch_documents 分批从chromadb当中获取文档片段列表
        2. 遍历 1 中得到的文档片段列表，调用  self.generate_questions 生成问题列表
        3. 将 2 中得到的问题列表，结合文档片段id，传入到 self.save_questions
        """
        offset = 0
        while True:
            doc_infos = self.fetch_documents(offset=offset)
            if not doc_infos["documents"]:
                break
            ids = doc_infos["ids"]
            for i, doc in enumerate(doc_infos["documents"]):
                questions = self.generate_questions(doc)
                self.save_questions(questions, ids[i])
            offset += len(doc_infos["documents"])


# 示例用法
if __name__ == "__main__":
    extractor = ExtractQuestion()
    extractor.extract_questions()
