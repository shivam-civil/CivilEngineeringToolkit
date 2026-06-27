import streamlit as st 
import pandas as pd
from logics.sieveanalysis_logics import analyze_sieve, plot_psd


with st.form("my_form"):
    st.title("Soil Sieve Analysis Tool")
    st.write(" ")
    st.write(" ")
    st.info("Note: Don't write units like mm or gm in input field",icon='🥷')
    st.write(" ")
    
    with st.expander("Optional Field"):
        col1,col2 = st.columns(2)
        with col1 :
            mass = float(st.number_input("Total mass of Soil (gm)",format="%g"))
    data = pd.DataFrame(
        {
            "SieveSize(mm)":["",""],
            "MassRetained(gm)":["",""]
        }
    )
    edited_data=st.data_editor(
        data,
        num_rows='dynamic',
        width='stretch',
        hide_index=True
        )
    button1 = st.form_submit_button("Submit")

if button1:
    data = edited_data.dropna()
    try:

        data["SieveSize(mm)"] = data["SieveSize(mm)"].astype(float)
        data["MassRetained(gm)"] = data["MassRetained(gm)"].astype(float)

        if not mass:
            result_df, plot_df, d_values, coeffs = analyze_sieve(data)
        elif isinstance(mass, (int, float)):
            result_df, plot_df, d_values, coeffs = analyze_sieve(data, total_mass=float(mass))

        fig = plot_psd(plot_df, d_values)
        st.plotly_chart(fig)

        st.subheader("Calculation Table")
        st.dataframe(result_df)

        d10, d30, d60 = d_values
        Cu, Cc = coeffs
        

        st.divider()
        
        col1, col2, col3 = st.columns(3)

        with col1: 
            st.metric("D10",value=d10)
        with col2: 
            st.metric("D30",value=d30)
        with col3: 
            st.metric("D60",value=d60) 

        coln1, coln2 = st.columns(2)

        with coln1 : 
            st.metric("Cu",value=Cu)

        with coln2 :
            st.metric("Cc",value=Cc)  

        st.divider()



    except ValueError:
        st.warning("Please make sure all inputs are valid numbers.")
    except Exception as e:
        st.warning(f"Error occurred: {e}")

   
