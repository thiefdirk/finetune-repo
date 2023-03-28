from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain

# _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
# You can assume the question about the most recent state of the union address.

# Chat History:
# {chat_history}
# Follow Up Input: {question}
# Standalone question:"""
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
You can assume the question about Educational Institution Customer Consultation.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

# template = """You are an AI assistant for answering questions about the most recent state of the union address.
# You are given the following extracted parts of a long document and a question. Provide a conversational answer.
# If you don't know the answer, just say "잘 모르겠네요." Don't try to make up an answer.
# If the question is not about the most recent state of the union, politely inform them that you are tuned to only answer questions about the most recent state of the union.
# Question: {question}
# =========
# {context}
# =========
# Answer in Markdown:"""

template = """You are an AI assistant for answering questions about Educational Institution Customer Consultation.
You are given the following extracted parts of a long conversation between agent, customer and a question. Assume you are agent and provide a conversational answer to customer. 
If you don't know the answer, just say "잘 모르겠네요." Don't try to make up an answer.
If the question is not about Educational Institution Customer Consultation, politely inform them that you are tuned to only answer questions about Educational Institution Customer Consultation.
Question: {question}
=========
{context}
=========
Answer in Markdown:"""
QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])


def get_chain(vectorstore):
    llm = OpenAI(temperature=0)
    qa_chain = ChatVectorDBChain.from_llm(
        llm,
        vectorstore,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    )
    return qa_chain
