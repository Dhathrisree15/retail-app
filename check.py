from sqlalchemy import create_engine, text
DB_URL = 'postgresql://postgres:retail2024!buddy@db.wwdodoeohmbirvyiatba.supabase.co:5432/postgres'
engine = create_engine(DB_URL)
with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM transactions'))
    print('Transactions:', result.fetchone()[0])
    result = conn.execute(text('SELECT COUNT(*) FROM households'))
    print('Households:', result.fetchone()[0])
