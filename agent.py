
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
#from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
#from langchain.agents import create_tool_calling_agent, AgentExecutor 
#above  is the older version  na dbelow is the newer simpler version
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
def build_agent():
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY")
    )

    search_tool = TavilySearch(
        max_results=5,
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )

    tools = [search_tool]

    Prompt_teplate = ChatPromptTemplate.from_messages([
        ("system", """You are an AI News Agent. You ONLY answer questions related to {allowed_topics}.

        If the user asks about anything unrelated, politely decline and remind them you only cover AI news. Do not attempt to search for unrelated topics.

        For valid questions: use web search to find current, accurate information. Format your answers in clear bullet points. Always mention where the information came from.""")
    ])

    system_message = Prompt_teplate.format(
        allowed_topics ="artificial intelligence — AI news, AI companies, AI models, AI research, AI policy/regulation, and AI industry events "
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_message
    )

    return agent