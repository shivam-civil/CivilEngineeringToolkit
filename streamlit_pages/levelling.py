# IMPORT REQUIRED MODULES 
import streamlit as st 
import pandas as pd 
import json
from io import BytesIO
import openpyxl

# IMPORT METHODS FROM CivilTools Folder 
from logics.levelling_logics import CleanData
from logics.levelling_logics import HiMethod
from logics.levelling_logics import RiseFallMethod

st.set_page_config(
    page_title="Leveling Automation",
    page_icon="profile.png"
)
with st.form(key='myform'): 
    #  ------ HEADER --------
    st.title("Leveling Automation ")
    st.write("HI & RiseFall Method")

    st.divider()

    # ------ INPUT SECTION -------

    column1,column2 = st.columns(2)

    with column1 : 
        method = st.radio(
        "Select Method",
        ["HI METHOD","RISE FALL METHOD"]
        )

    with column2 :
        bm_rl=st.number_input("BenchMark RL ",
        value=100.000,
        step=0.001,
        format="%.3f"
        )

    st.divider()

    # ----- RAW READINGS INPUT ------

    raw_readings_str=st.text_input(
    "Enter Staff Readings (Comma Seperated) ",
    placeholder=" 1.03 , 1.3 , 2.3 , 4.6,  ...."
    ) 

    # ---- CHANGE POINTS INPUT ------

    cp_str=st.text_input(
    "Enter Change Point Indices (0 if no) ",
    placeholder=" 3 , 6 , 10 , ..."
    )

    st.divider()

    submitted=st.form_submit_button("Calculate")
if submitted==True:     
    try :
    # PARSE RAW READINGS 
        raw_readings_list=[round(float(x.strip()),3) for x in raw_readings_str.split(",")]

        # PARSE CHANGE POINTS 
        if cp_str.strip():
            cp_list=[int(x.strip()) for x in cp_str.split(",")]
        else :
            cp_list=[0]

        # CLEAN RAW DATA AND CALCULATE TOTAL BS,FS, AND FIRST,LAST RL 
        readings= CleanData(raw_readings_list,cp_list)
        total_bs= sum(r["value"] for r in readings if r["type"]=="BS")
        total_fs= sum(r["value"] for r in readings if r["type"]=="FS") 
        first_rl=bm_rl


        # RUN SELECTED METHOD
        if method.startswith("HI"):
            df,last_rl=HiMethod(readings,bm_rl)
        elif method.startswith("RISE"):
            df,last_rl=RiseFallMethod(readings,bm_rl)

        st.success("Calculation done...")

        st.divider()

        st.subheader("Result Table")
        st.dataframe(df,width='stretch')
        st.divider()
        # ----- ARITHMETIC CHECK ---- 
        st.subheader("ARITHMETIC CHECK")
        st.write(f"Total BS - Total FS = {round(abs(total_bs - total_fs),3)}")
        st.write(f"Last RL - First RL  = {round(abs(last_rl - first_rl),3)}")
        if round(abs(total_bs - total_fs),3) == round(abs(last_rl - first_rl),3) :
            st.success("Arithmetic Check Passed ✅")
        else :
            st.warning("Arithmetic Check Failed 👎") 
            st.warning("You messed up. Check your change points.")
            st.success("**Possible Solution** \n1. Remove Consecutive Change Points If there any.\n2. Dont keep the last reading as Change Point. ")
            


        st.divider()

        # ----- DOWNLOADS ----------

        csv_data=df.to_csv(index=False).encode("utf-8")
        download1,download2=st.columns(2)

        # CSV DOWNLOAD

        with download1:
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="leveling_result.csv",
                mime="text/csv"
            )

        #  EXCEL DOWNLOAD 

        # EXCEL BUFFER SETUP
        excel_buffer= BytesIO()
        df.to_excel(excel_buffer,index=False,engine="openpyxl")
        excel_buffer.seek(0)

        with download2:
            st.download_button(
                label="Download Excel",
                data=excel_buffer,
                file_name="leveling_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )    


    except Exception as e :
        st.error("Error in Calculation.\nCheck Your Inputs")
        st.code(str(e))