from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain.tools import Tool
from langchain.agents import AgentType
from app.config import settings
from app.database import get_sql_db

def build_rag_sql_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=settings.OPENAI_API_KEY)
    
    db = get_sql_db()
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    vector_store = PGVector(
        collection_name="product_knowledge",
        connection_string=settings.DATABASE_URL,
        embedding_function=embeddings,
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    def retrieve_unstructured_docs(query: str) -> str:
        docs = retriever.get_relevant_documents(query)
        return "\n---\n".join([d.page_content for d in docs])

    kb_tool = Tool(
        name="product_knowledge_base",
        func=retrieve_unstructured_docs,
        description="Useful for retrieving detailed unstructured product documentation, warranties, manuals, and specs."
    )

    tools = sql_toolkit.get_tools() + [kb_tool]

    system_prefix = """You are an enterprise assistant capable of querying structured SQL database records and unstructured product knowledge.
    When answering questions:
    1. Determine if you need relational quantitative data (SQL tables like customers, products, orders) or unstructured text facts (Knowledge Base).
    2. Execute valid SQL queries to gather structured facts, or query the product_knowledge_base for documentation.
    3. Synthesize both sources into a clear response.
    """

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=sql_toolkit,
        extra_tools=[kb_tool],
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        prefix=system_prefix
    )
    
    return agent_executor