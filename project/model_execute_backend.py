import langchain
import pandas as pd

from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain.retrievers import ParentDocumentRetriever

from langchain import hub

from transformers import BitsAndBytesConfig
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA
import transformers

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

import argparse

from fastapi import FastAPI
import uvicorn

#### Embedding Model Load ####
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-base', model_kwargs={'device': 'cuda'})
# BAA/bge-m3

#### Vectorstore & Retriever Load ####
vectorstore = Chroma(
    collection_name="split_parents", embedding_function=embeddings, persist_directory='db'
)

retriever = vectorstore.as_retriever(search_type = "similarity_score_threshold", search_kwargs = {"score_threshold" : 0.7, "k" : 1})


#### RAG Prompt Load ####
prompt = hub.pull("rlm/rag-prompt")
prompt.messages[0].prompt.template = "You are an assistant in answering drug information. You need to know how to explain the ingredients, effects, side effects, etc. of the drug.Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Keep the answer concise and answer in Korean.\nQuestion: {question} \nContext: {context} \nAnswer:"


#### LLAMA3 Load ####
tokenizer = AutoTokenizer.from_pretrained('./model', use_fast = True, device_map = 'cuda')
model = AutoModelForCausalLM.from_pretrained('./model',
                                             low_cpu_mem_usage = True,      
                                             device_map = 'cuda'
                                             )

query_pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer = tokenizer,
    torch_dtype=torch.float16,
    device_map="auto",          # GPU 8개를 쓴다면 자동적으로 GPU 전체에 분산시켜줌
    max_new_tokens = 300,
    do_sample = True,
    # num_return_sequences = 1      # default 값임
)

llm = HuggingFacePipeline(pipeline=query_pipeline)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


## Backend ##
app = FastAPI()

@app.get("/")
def read_homepage():
    return None

@app.post("/question/")
def post_question(question: dict):
    question = question['question']
    
    answer = rag_chain.invoke(question)
    
    print(answer)
    
    context = answer.split("Context: ")[1].split("\nAnswer: ")[0]
    
    response_answer = answer.split("\nAnswer: ")[1]

    if "\n" in response_answer:
        response_answer = response_answer.split("\n")[0]
    
    answer = {
        "question" : question,
        "context" : context,
        "answer" : response_answer
    }
    
    return answer
    
    
if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
    
