import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def seed_database():
    engine = create_engine(os.getenv("DATABASE_URL"))
    with engine.connect() as conn:
        # 1. Create the table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(100),
                units_sold INT,
                revenue DECIMAL(10, 2)
            );
        """))
        
        # 2. Clear existing data to avoid duplicates on re-runs
        conn.execute(text("TRUNCATE TABLE sales;"))
        
        # 3. Insert mock data
        conn.execute(text("""
            INSERT INTO sales (product_name, units_sold, revenue) VALUES 
            ('Enterprise AI License', 5, 250000.00),
            ('API Credits', 1200, 12000.50),
            ('Cloud Storage', 450, 4500.00),
            ('Consulting Retainer', 2, 30000.00);
        """))
        conn.commit()
        print("Database successfully seeded with mock sales data!")

if __name__ == "__main__":
    seed_database()