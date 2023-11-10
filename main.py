from fastapi import FastAPI
from app import router as stock_router
# from fastapi_cors import CORS


from db import init_db

app = FastAPI()

# origins = ["*"]

# app.add_middleware(
#     CORS,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(stock_router.router)
