import pandas as pd
from sqlalchemy import create_engine

DB_URL = 'postgresql://postgres:retail2024buddy@db.wwdodoeohmbirvyiatba.supabase.co:5432/postgres'
engine = create_engine(DB_URL)

print('Loading households...')
hh = pd.read_csv('400_households.csv')
hh.columns = hh.columns.str.strip()
hh.to_sql('households', engine, if_exists='replace', index=False)
print('Done!')

print('Loading products...')
pr = pd.read_csv('400_products.csv')
pr.columns = pr.columns.str.strip()
pr.to_sql('products', engine, if_exists='replace', index=False)
print('Done!')

print('Loading transactions...')
tx = pd.read_csv('400_transactions.csv')
tx.columns = tx.columns.str.strip()
tx.to_sql('transactions', engine, if_exists='replace', index=False, chunksize=1000)
print('ALL DONE!')
