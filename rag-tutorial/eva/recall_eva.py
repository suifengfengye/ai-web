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
