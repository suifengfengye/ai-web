import json

import chromadb
from langchain_chroma import Chroma

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings, ChatOllama

from pydantic import BaseModel, Field
from rag_langchain import RagLangChain
# {"QAList": [{"question": "q1", "answer": "a1"}]}

class QAPair(BaseModel):
    question: str = Field(description="A question")
    answer: str = Field(description="The answer to the question")

class LLMGenerateQA(BaseModel):
    QAList: list[QAPair] = Field(description="A list of QA pairs")

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
你是一名教师/教授。你的任务是为即将到来的测验/考试设置 {num_questions_per_chunk} 个问题,以及生成对应问题的参考答案。
这些问题应覆盖文档中的不同方面。限制问题范围在提供的背景信息内。
请按照如下的JSON Schema进行输出:{schema}"""


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
            schema_str = json.dumps(LLMGenerateQA.model_json_schema())
            result = chain.invoke({
                    "context": context,
                    "num_questions_per_chunk": self.num_questions_per_chunk,
                    "schema": schema_str
                })
            # {"questions": []}
            return result
        except Exception as e:
            print(f" error occurred, {e}")
            return None

    def generate_answers(self, result):
        # 1. 使用RagLangChain创建一个对象
        # 2. 遍历result字典当中的QAList, 取出每一个question, QAList的结构如下：
        # [{"question": "q1", "answer": "a1"}]
        # 3. 调用RagLangChain对象的query方法，传入question, 得到answer
        # 4. 将answer添加到QAList当中
        # 5. 返回QAList
        rag_lang_chain = RagLangChain()
        for qa_pair in result["QAList"]:
            question = qa_pair.get("question", "")
            if not question:
                continue
            answer, retrieved_docs = rag_lang_chain.query(question)
            qa_pair["response"] = answer
            qa_pair["retrieved_contexts"] = retrieved_docs
        return result["QAList"]

    def save_questions(self, answer_result, id, doc):
        # 遍历 questions, 将每一个元素结合id,组成一个json数据{"id": "xxx", "question": "xx"}
        # 保存到当前文件夹当中的 "./questions.txt" 文件当中
        # questions_with_id = [{"id": id, "question": question} for question in questions]
        with open("./questions_answers_01.txt", "a", encoding="utf-8") as f:
            for item in answer_result:
                final_item = {
                    "user_input": item.get("question", ""),
                    "reference": item.get("answer", ""),
                    "response": item.get("response", ""),
                    "retrieved_contexts": [doc_item.page_content for doc_item in item.get("retrieved_contexts", [])],
                    "retrieved_contexts_ids": [doc_item.id for doc_item in item.get("retrieved_contexts", [])],
                    "reference_contexts_ids": [id],
                    "reference_contexts": [doc],
                }
                f.write(json.dumps(final_item, ensure_ascii=False) + "\n")

    def extract_questions(self):
        """
        1. 循环调用 self.fetch_documents 分批从chromadb当中获取文档片段列表
        2. 遍历 1 中得到的文档片段列表，调用  self.generate_questions 生成问题列表
        3. 将 2 中得到的问题列表，结合文档片段id，传入到 self.save_questions
        """
        offset = 0
        limit = 10
        # flag = False
        while True:
            # if flag:
            #     break
            doc_infos = self.fetch_documents(offset=offset, limit=limit)
            if not doc_infos["documents"]:
                break
            # flag = True
            ids = doc_infos["ids"]
            for i, doc in enumerate(doc_infos["documents"]):
                result = self.generate_questions(doc)
                answer_result = self.generate_answers(result)
                # print(answer_result)
                self.save_questions(answer_result, ids[i], doc)
            offset += len(doc_infos["documents"])


# 示例用法
if __name__ == "__main__":
    extractor = ExtractQuestion()
    extractor.extract_questions()