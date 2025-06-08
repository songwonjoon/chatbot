from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-nli",
    model_kwargs={"device": "cpu"}
)

loader = DirectoryLoader('./document', glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

db = FAISS.from_documents(documents, embeddings)
retriever = db.as_retriever()

llm = OllamaLLM(
    model="exaone3.5",
    base_url="http://host.docker.internal:11434"
)

# 5. 사용자 프롬프트 템플릿 (한국어 시스템 명시)
prompt_template = """
너는 RISE 가입 문의봇이야
다음은 사용자의 질문이며, 관련된 문서를 참고하여 한국어로만 정확하게 답변해주세요.

[문서 요약]
{context}

[질문]
{question}

[답변]
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True
)

def send_to_exaone(question: str):
    response = qa_chain.invoke({"query": question})
    return response["result"]
