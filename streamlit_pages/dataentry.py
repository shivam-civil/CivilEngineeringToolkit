import streamlit as st 
import pandas as pd 
from logics.dataentry_logics import concat_data

with st.form("data_key"):
    st.header("DataEntry Utils")

    # RAW INPUTS
    headers = st.text_input("Headers [In CSV Format] ")
    default_values = st.text_input("Default Values [In CSV Format]",help="Don't skip any , instead add string space")
    concat_type = st.selectbox("Concat Type",["Left To Right","Right To Left"])
    
    # CLEANING THE RAW DATAS 
    headers = headers.strip().lower().split(",")
    default_values = default_values.strip().lower().split(",")
    nums = int(st.number_input("Number Of Datas", min_value=1, key="num_rows"))
    if isinstance(headers,list) and len(headers)>1:
        df = pd.DataFrame({header:[0]*nums for header in headers})
        remaining_datas = st.data_editor(df,num_rows="dynamic",width="stretch",hide_index=True,key="num_datas")

    
    button1=st.form_submit_button("Submit") 
if button1 :
    new_df =concat_data(remaining_datas,default_values,concat_type,headers)
    st.dataframe(new_df)


