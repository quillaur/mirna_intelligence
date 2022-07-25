import streamlit as st
import pandas as pd
import pygsheets
from google.oauth2 import service_account

SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
my_credentials = service_account.Credentials.from_service_account_info(st.secrets, scopes=SCOPES)
gc = pygsheets.authorize(custom_credentials=my_credentials)
sheet_url = st.secrets["public_mirtarbase_gsheets_url"]
sh = gc.open_by_url(sheet_url)
ws = sh.sheet1
data = ws.range("A:I", returnas='matrix')
header = data.pop(0)
df = pd.DataFrame(data, columns=header)

all_species = df["Species (miRNA)"].unique()
all_exp_types = []

for exp_type in df["Experiments"].unique():
    if "//" in exp_type:
        all_exp_types.extend(exp_type.split("//"))
    else:
        all_exp_types.append(exp_type)

all_exp_types = list(set(all_exp_types))

with st.form("Parameters:"):
    selected_species = st.multiselect("Filter by species:", options=all_species, default=all_species)
    selected_exp_types = st.multiselect("Filter by experiment types:", options=all_exp_types, default=all_exp_types)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(f"You have selected: {selected_species} and {selected_exp_types}")

        def select_exp_type(row):
            for exp_type in selected_exp_types:
                if exp_type in row["Experiments"]:
                    return row


        df = df.loc[df["Species (miRNA)"].isin(selected_species) & df.apply(lambda x: select_exp_type(x), axis=1)]

st.dataframe(df)

