import os
import openai
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings    # 임베딩용
from langchain_community.vectorstores import FAISS             # 벡터 스토어 종류
from langchain.chains import RetrievalQA             # 질문 답변 툴
from langchain_openai import ChatOpenAI      
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader

load_dotenv()

openapi_key = os.getenv("OPENAI_API_KEY")

loader = DirectoryLoader('./document', glob="*.txt", loader_cls=TextLoader)

documents = loader.load()

embeddings = OpenAIEmbeddings()

# 벡터스토어 만듭니다. 이것도 다음 파트에서 자세하게 다루겠습니다!
db = FAISS.from_documents(documents, embeddings)
retriever = db.as_retriever()

# 이제 언어모델 쓸 거 만들어두고요..
llm = ChatOpenAI(model_name="gpt-4")

def send_to_chatGpt(messages, model="gpt-4"):
    response = RetrievalQA.from_chain_type(
        llm=llm,
        # chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
     )
    message = response(messages)
    return message['result']