import streamlit as st 
import pandas as pd
import numpy as np
from logics.traverse_logics import Traverse


with st.form("myform"):
    # --- HEADER ----------
    st.title("Traverse Automation Tool")
    st.write(" ")
    st.subheader("Note : ")
    st.markdown("""
        1) Enter readings in CSV Format like as 40,20,10.
        \n2) Readings Should be in WCB System                    
        """)
    st.write(" ")


    # ----INPUT SECTION ---
    coln1,coln2,coln3=st.columns(3)
    with coln1:
        traverse_type=st.selectbox(
            label="Select Type Of Traverse ",
            options=["Closed Traverse"]
        )
    with coln2:
        correction_method=st.selectbox(
            label="Correction Method",
            options=["Bowditch Method"]
        )
    with coln3:
        detailed=st.selectbox(
            label="Result Type",
            options=["Main Datas Only","Detailed Datas For Error Check"]
        )
    st.write(" ")    

    data=pd.DataFrame(
        {
            "Station": ["AB","BC"],
            "Distance(m)":[0.0,0.0],
            "ForeBearing(WCB)":["",""]
        }
    )
    edited_data=st.data_editor(
        data,
        num_rows="dynamic",
        width="stretch",
        hide_index=True
    )
    
    st.write(" ")

    # --- SUBMIT SECTION --
    submitted=st.form_submit_button("Compute Traverse")

if submitted:
    cleaned_data=edited_data.dropna()
    traverse_1=Traverse(cleaned_data,traverse_type,correction_method,detailed)
    results=traverse_1.compute_traverse()
    st.divider()
    st.write(" ")
    st.subheader("Traverse Computation Results")
    st.dataframe(results)
    traverse_1.plot_traverse()
    
    
    
    
     