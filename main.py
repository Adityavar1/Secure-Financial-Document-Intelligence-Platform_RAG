from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import lru_cache
from pipeline import create_vector_store, load_vector_store, create_qa_chain
from auth import authenticate, create_access_token, verify_token, create_user

app = FastAPI()

security = HTTPBearer()

vectorstore = load_vector_store()
if vectorstore is None:
    vectorstore = create_vector_store()

qa_chain = create_qa_chain(vectorstore)




class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    department: str
    email: str


class QueryRequest(BaseModel):
    question: str


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

@app.get("/")
def home():
    return {"message": "Market Intelligence RAG API with JWT 🔐"}


# Register User
@app.post("/register")
def register(req: RegisterRequest):

    success, message = create_user(
        req.username,
        req.password,
        req.department,
        req.email
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}


# Login → Get JWT Token
@app.post("/login")
def login(req: LoginRequest):

    user = authenticate(req.username, req.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": req.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def normalize_query(q: str):
    return q.strip().lower()

@lru_cache(maxsize=50)
def cached_query(question: str):
    return qa_chain({"query": question})

@app.post("/query")
def query(req: QueryRequest, user=Depends(get_current_user)):

    try:
        result = cached_query(normalize_query(req.question))

        return {
            "user": user["sub"],
            "question": req.question,
            "answer": result["result"],
            "sources": [
                {
                    "content": doc.page_content[:200],
                    "source": doc.metadata.get("source", "unknown")
                }
                for doc in result["source_documents"]
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
def health():
    return {"status": "ok"}