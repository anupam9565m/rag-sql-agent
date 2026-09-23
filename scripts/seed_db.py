import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text, create_engine
from langchain_community.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain.core.documents import Document
from app.config import settings

def seed():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        # 1. Seed Relational Schema
        conn.execute(text("""
            DROP TABLE IF EXISTS orders, products, customers CASCADE;
            
            CREATE TABLE customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            );
            
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                category VARCHAR(50),
                price NUMERIC(10, 2)
            );
            
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                customer_id INT REFERENCES customers(id),
                product_id INT REFERENCES products(id),
                quantity INT,
                order_date DATE
            );
            
            INSERT INTO customers (name, email) VALUES 
            ('Alice Smith', 'alice@example.com'),
            ('Bob Jones', 'bob@example.com');
            
            INSERT INTO products (name, category, price) VALUES 
            ('UltraBook Pro 15', 'Electronics', 1299.99),
            ('Ergonomic Chair', 'Furniture', 299.50),
            ('Noise-Canceling Headphones', 'Electronics', 199.00);
            
            INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES 
            (1, 1, 1, '2026-01-15'),
            (1, 3, 2, '2026-01-20'),
            (2, 2, 1, '2026-02-01');
        """))

    # 2. Seed Vector Store (Unstructured Product Knowledge & Documentation)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=settings.OPENAI_API_KEY)
    
    docs = [
        Document(
            page_content="UltraBook Pro 15 Warranty & Support: Covers manufacturing defects for 24 months. Return policy allows full refunds within 30 days.",
            metadata={"product_id": 1, "doc_type": "policy"}
        ),
        Document(
            page_content="Ergonomic Chair Assembly Guide: Maximum load capacity is 150 kg. Features lumbar support adjustment with 4D armrests.",
            metadata={"product_id": 2, "doc_type": "manual"}
        ),
        Document(
            page_content="Noise-Canceling Headphones Spec Sheet: Battery life extends to 30 hours with Active Noise Cancellation (ANC) enabled. Supports Bluetooth 5.3.",
            metadata={"product_id": 3, "doc_type": "specs"}
        ),
    ]
    
    PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name="product_knowledge",
        connection_string=settings.DATABASE_URL,
        pre_delete_collection=True
    )
    print("Database seeding & vector indexing complete.")

if __name__ == "__main__":
    seed()