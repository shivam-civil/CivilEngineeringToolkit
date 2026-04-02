import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
class Traverse:
    Traverse_Type=["Open Traverse","Closed Traverse"]
    Correction_Method=["Bowditch Method"]
    def __init__(self,df,traverse_type,correction_method,detailed=False):
        self.traverse_type=traverse_type
        self.correction_method=correction_method
        self.df=df
        self.detailed=detailed
        self.x_coords=None
        self.y_coords=None
        
    def dms_csv_to_decimal(self,dms_str: str):
        """
        This function converts the dms string to float decimal degree.
        This also can be used as parameter in .apply() for dataframe case.
        It returns float type value
        """
        parts=[p.strip() for p in dms_str.split(",")]  
        if 1<=len(parts)<=3 :
            if len(parts)== 1 :
                return float(parts[0])
            elif len(parts) == 2:
                d,m=list(map(float,parts))
                return d + m/60
            else :
                d,m,s=list(map(float,parts))
                return d + m/60 + s/3600
            

    def compute_traverse_bowditch(self):
        """
        This function returns a filtered rounded off dataframe of result of traverse.
        """
        self.df["decimal_degree"]=self.df["ForeBearing(WCB)"].apply(self.dms_csv_to_decimal)
        self.df["rad_degree"]=np.deg2rad(self.df["decimal_degree"])   # decimal degree to radians
        self.df['calculated_latitude']= self.df["Distance(m)"] * np.cos(self.df["rad_degree"])
        self.df['calculated_departure'] = self.df["Distance(m)"] * np.sin(self.df["rad_degree"])
        perimeter=self.df["Distance(m)"].sum()
        sumcl=self.df["calculated_latitude"].sum()     # SUM OF CALCULATED LATITUTE 
        sumcd=self.df["calculated_departure"].sum()    # SUM OF CALCULATED DEPARTURE
        self.df["correction_for_latitude"] = ( sumcl * self.df["Distance(m)"] ) / perimeter
        self.df["correction_for_departure"] = ( sumcd * self.df["Distance(m)"]) / perimeter
        self.df["CorrectedLatitude"]=self.df["calculated_latitude"] - self.df["correction_for_latitude"]
        self.df["CorrectedDeparture"]=self.df["calculated_departure"] - self.df["correction_for_departure"]
        SumCL=self.df["CorrectedLatitude"].sum()     # SUM OF CORRECTED LATITUDE
        SumCD=self.df["CorrectedDeparture"].sum()    # SUM OF CORRECTED DEPARTURE
        
        # EASTING AND NORTHING COORDINATES
        EO = 0
        NO = 0
        E = [EO]
        N = [NO]
        for i in range(len(self.df)) :
            dept = self.df.loc[i,"CorrectedDeparture"]
            lat  = self.df.loc[i,"CorrectedLatitude"]
            E.append(E[-1]+dept)
            N.append(N[-1]+lat)    
        self.df["Easting"]=E[1:]
        self.df["Northing"]=N[1:]

        # COORDINATES FOR PLOTTING
        self.x_coords=E
        self.y_coords=N



        # ROUNDS OFF THE SELF.DF TO 4 AND STORE NEW DF IN SHOWABLE_DF
        showable_df=self.df.round(4)

        # CLEANS THE NEGATIVE ZERO AND ANY NUMBER SMALLER THAN 1E-10
        colns_for_zero_clean =["CorrectedLatitude","CorrectedDeparture","correction_for_latitude","correction_for_departure","calculated_latitude","calculated_departure","Easting","Northing"]
        showable_df[colns_for_zero_clean]=showable_df[colns_for_zero_clean].mask(
            abs(showable_df[colns_for_zero_clean]) < 1e-6 , 0
        )

        # CONCATINATING EASTING AND NORTHING FOR COORDINATES
        showable_df["Coordinates"]=showable_df["Easting"].astype(str)+","+ showable_df["Northing"].astype(str)
        self.df["Coordinates"]=self.df["Easting"].astype(str)+","+ self.df["Northing"].astype(str)

        # LAST EXTRA ROW FOR TOTAL
        last_row ={
            "Station":"TOTAL",
            "Distance(m)":perimeter,
            "calculated_latitude":self.clean_zero(sumcl),
            "calculated_departure":self.clean_zero(sumcd),
            "CorrectedLatitude":self.clean_zero(SumCL),
            "CorrectedDeparture":self.clean_zero(SumCD),
            "ForeBearing(WCB)":None,
            "decimal_degree":None,
            "rad_degree":None,
            "correction_for_latitude":None,
            "correction_for_departure":None,
            "Easting":None,
            "Northing":None,
            "Coordinates":None
        }
        # ADD THE LAST ROW 
        showable_df = pd.concat([showable_df,pd.DataFrame([last_row])], ignore_index=True )
        if self.detailed == "Main Datas Only":
            main_colns=["Station","Distance(m)","ForeBearing(WCB)","Easting","Northing","Coordinates"]
            return showable_df[main_colns]

        return showable_df

    def compute_traverse(self):
        if self.correction_method == "Bowditch Method":
            return self.compute_traverse_bowditch()
        
    def clean_zero(self,val):
        return 0 if abs(val) < 1e-6 else val 

    def plot_traverse(self):
        """
        This function takes parameters as list of x and y from instance attributes .
        """
        if self.x_coords is None or self.y_coords is None:
            raise ValueError("compute_traverse() is not called yet")
        
          

        # TypeCasting 
        self.x_coords = [round(float(x_coord),4) for x_coord in self.x_coords]
        self.y_coords = [round(float(y_coord),4) for y_coord in self.y_coords]
         
        fig,ax = plt.subplots(figsize=(8,6))
        ax.plot(self.x_coords,self.y_coords,marker="o",linestyle="-")
        
        # Annotate points 
        for i,(x,y) in enumerate(zip(self.x_coords,self.y_coords),start=1) :
            if i != 1 and i != len(self.x_coords):
                ax.text(x,y,f"P{i}",fontsize=9,ha="right",va="bottom")
            else :
                ax.text(x,y,f"START",fontsize=9,ha="right",va="bottom")
        ax.set_title("Traverse Plot")
        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Northing (m)")
        ax.grid(True)
        ax.axis('equal')

        # DISPLAY IN STREMLIT 
        st.pyplot(fig)    
        
