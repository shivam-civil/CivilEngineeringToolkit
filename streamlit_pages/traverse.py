import streamlit as st 
import pandas as pd

with st.form("myform"):
    # --- HEADER ----------
    st.title("Traverse Automation Tool")
    st.write(" ")
    st.markdown("Note: Enter the ForeBearings in ***decimal format*** not in degree-minute-second format.")
    st.write(" ")

    # ----INPUT SECTION ---
    data=pd.DataFrame(
        {
            "Station": ["AB","BC"],
            "Distance(m)":[0.0,0.0],
            "ForeBearing(WCB)":[0.0,0.0]
        }
    )
    edited_data=st.data_editor(
        data,
        num_rows="dynamic",
        width="stretch",
        hide_index=True
    )
    


    # --- SUBMIT SECTION --
    submitted=st.form_submit_button("Compute Traverse")

if submitted:
    st.write(edited_data)
    