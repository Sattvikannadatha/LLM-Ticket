
from fastapi import FastAPI
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

app = FastAPI()
DATA_PATH = '/content/support_tickets.csv'

def load_df():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        return df
    return pd.DataFrame()

@app.get('/health')
def health():
    return {'status': 'healthy'}

@app.get('/anomalies')
def get_anomalies():
    df = load_df()
    if df.empty: return []
    now = df['created_at'].max()
    # Logic: Unresolved High/Critical older than 24h
    unresolved = df[(df['status'] != 'Resolved') & 
                    (df['priority'].isin(['High', 'Critical'])) & 
                    (df['created_at'] < (now - timedelta(hours=24)))]
    return unresolved.replace({np.nan: None}).to_dict(orient='records')

@app.get('/query')
def query_data(q: str):
    return {'query': q, 'answer': 'Backend received query successfully.'}
