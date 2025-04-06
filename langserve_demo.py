import os
import uvicorn
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from langserve import add_routes

# Load environment variables from .env file
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-3.5-turbo")

parser = StrOutputParser()

system_template = "Translate the following into {language}:"

promt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

chain = promt_template | llm | parser

app = FastAPI(
    title="simpleTraslator",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces"
)


add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)


