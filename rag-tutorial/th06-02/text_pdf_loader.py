# from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_ollama import ChatOllama
from dxh_pdf_loader import DxhPDFLoader

docs_loader = DxhPDFLoader(
    file_path="./pdf_1_5.pdf",
    extract_images=True,
    table_strategy="lines",
    images_parser=LLMImageBlobParser(
        model=ChatOllama(model="qwen2.5vl:latest"),
        prompt="""你是一名助理，负责对图片进行摘要以便检索。
    “1. 这些摘要将被嵌入并用于检索原始图片。”
    “请提供图片的简洁摘要，并针对检索进行优化\n”
    “2. 从图片中提取所有文本。”
    “请勿从页面中排除任何内容。\n”
    “请将答案格式化为 Markdown 格式，不包含解释性文字”
    “并且开头不包含 Markdown 分隔符 ```。"""
    )
)

docs = docs_loader.load()
# Document(page_content="")
for doc_item in docs:
    print(doc_item.page_content)
    print("*" * 100)
