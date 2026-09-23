from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from app.agent import build_rag_sql_agent

app = FastAPI(title="RAG SQL Agent Service", version="1.0.0")

# Cache agent execution instance on app launch
agent_instance = None

@app.on_event("startup")
def startup_event():
    global agent_instance
    agent_instance = build_rag_sql_agent()

class QueryRequest(BaseModel):
    query: str = Field(..., example="What is the total spend of Alice Smith, and what is the warranty policy on the UltraBook Pro 15?")

class QueryResponse(BaseModel):
    query: str
    result: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    if not agent_instance:
        raise HTTPException(status_code=500, detail="Agent is not initialized.")
    try:
        response = agent_instance.invoke({"input": request.query})
        return QueryResponse(query=request.query, result=response["output"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))