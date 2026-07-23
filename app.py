
import streamlit as st
import pandas as pd
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from google.colab import userdata

st.set_page_config(page_title='AI Support Intelligence', layout='wide')
DATA_PATH = '/content/support_tickets.csv'

def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['created_at'] = pd.to_datetime(df['created_at'])
        return df
    return None

st.title('🎫 Support Ticket Intelligence Dashboard')
df = load_data()

if df is not None:
    tab1, tab2 = st.tabs(['📊 Analytics', '🤖 AI Query'])
    
    with tab1:
        st.subheader('Dataset Overview')
        st.write(f'Total Tickets: {len(df)}')
        st.dataframe(df.head())
        
    with tab2:
        st.subheader('Ask anything about the tickets')
        user_query = st.text_input('e.g., How many tickets are unresolved?')
        if user_query:
            try:
                api_key = userdata.get('GOOGLE_API_KEY')
                llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=api_key)
                agent = create_pandas_dataframe_agent(llm, df, allow_dangerous_code=True)
                st.write(agent.run(user_query))
            except Exception as e:
                st.error(f'LLM Error: {e}')
else:
    st.error('Data file not found.')
