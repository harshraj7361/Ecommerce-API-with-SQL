# from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
# from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
# from datetime import datetime
# DATABASE_URL = "sqlite:///./ecommerce.db"
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(
#     bind=engine,
#     autocommit=False,
#     autoflush=False
# )

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "Hello E-commerce API"}

# @app.get("/db-check")
# def db_check():
#     try:
#         # Engine se ek connection lo
#         with engine.connect() as conn:
#             return {"status": "connected", "database": "sqlite"}
#     except Exception as e:
#         return {"status": "failed", "error": str(e)}