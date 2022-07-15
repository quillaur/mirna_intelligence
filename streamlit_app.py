import streamlit as st
import pandas as pd
import pygsheets
from google.oauth2 import service_account

SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
my_credentials = service_account.Credentials.from_service_account_info(st.secrets, scopes=SCOPES)
gc = pygsheets.authorize(custom_credentials=my_credentials)

sheet_url = st.secrets["public_gsheets_url"]
sh = gc.open_by_url(sheet_url)
ws = sh.sheet1
data = ws.range("A:I", returnas='matrix')
header = data.pop(0)
df = pd.DataFrame(data, columns=header)
st.dataframe(df)
