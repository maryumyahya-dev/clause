# from typing import Annotated
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, Request
# from pydantic import BaseModel, StringConstraints

# from app.services.chat import RagService, Answer

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     rag_service = RagService()
#     app.state.rag_service = rag_service
#     yield
#     rag_service.close()

# app = FastAPI(title="clause AI APIs",lifespan=lifespan)

# @app.get(path="/")
# def health():
#     return {"status": "ok"}

# class AskQuestion(BaseModel):
#     question: Annotated[
#         str, StringConstraints( strip_whitespace=True, min_length=1,max_length=1000)]

#     @app.get(path="/")
#     def health():
#         return{"status": "ok"}


#     @app.post(path="/ask", response_model=Answer)
#     def ask_query(body: AskQuestion, req:Request):
#         # return req.app.state.rag_service(body.question)
#         # rag_service: RagService = app.state.rag_service
#         rag_service: RagService = req.app.state.rag_service
#         return rag_service.ask(body.question)



# from typing import Annotated
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, Request
# from pydantic import BaseModel, StringConstraints

# from app.services.chat import RagService, Answer


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     rag_service = RagService()
#     app.state.rag_service = rag_service
#     yield
#     rag_service.close()


# app = FastAPI(title="Clause AI APIs", lifespan=lifespan)


# @app.get("/")
# def health():
#     return {"status": "ok"}


# class AskQuestion(BaseModel):
#     question: Annotated[
#         str,
#         StringConstraints(
#             strip_whitespace=True,
#             min_length=1,
#             max_length=1000
#         )
#     ]


# @app.post("/ask", response_model=Answer)
# def ask_query(body: AskQuestion, req: Request):
#     rag_service: RagService = req.app.state.rag_service
#     return rag_service.ask(body.question)



from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request
from pydantic import BaseModel, StringConstraints

from app.services.chat import RAGService, Answer

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag = RAGService()
    yield
    app.state.rag.close()

app = FastAPI(title="Clause AI APIs", lifespan=lifespan)

class ASKQuestion(BaseModel):
    question: Annotated[
      str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)
    ]

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=Answer)
def ask_query(body: ASKQuestion, req: Request):
    return req.app.state.rag.ask(body.question)

