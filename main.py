from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from datetime import datetime,timedelta
DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    city = Column(String)
    joined_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__="products"

    id= Column(Integer,primary_key=True,index=True)
    name= Column(String,index =True)
    category=Column(String)
    price= Column(Float)
    stock= Column(Integer,default=0)
    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__="orders"

    id= Column(Integer,primary_key=True,index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id")) 
    quantity= Column(Integer)
    total_amount=Column(Float)
    status= Column(String,default="completed")
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel,Field
from typing import Annotated,List
import random


app = FastAPI()

class createcustomer(BaseModel):

    name: str
    email: str
    city: str

class customerOut(createcustomer):

    id: int
    joined_at: datetime

    class Config:
        from_attributes= True

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock: int = 0

class ProductOut(ProductCreate):
    id: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    status: str = "completed"


class OrderOut(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    total_amount: float
    order_date: datetime
    status: str

    class Config:
        from_attributes = True




@app.get("/")
def root():
    return {"message": "Hello E-commerce API"}

@app.get("/db-check")
def db_check():
    try:
        # Engine se ek connection lo
        with engine.connect() as conn:
            return {"status": "connected", "database": "sqlite"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/customers/", response_model=customerOut)
def create_customer(c:createcustomer, db: Session = Depends(get_db)):
    if db.query(Customer).filter_by(email=c.email).first():
        raise HTTPException(400, "Email already exists")
    
    obj = Customer(**c.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/customers/", response_model=List[customerOut])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()