import pandas as pd 


def concat_data(df,default_values,concat_type,headers):
    headers = [str(header) for header in headers]
    default_values = [str(default_value) for default_value in default_values]
    for i in range(0,len(headers)):
        if concat_type == "Left To Right":
            df[headers[i]] = default_values[i] + df[headers[i]].astype(str)
        elif concat_type == "Right To Left":
            df[headers[i]] =  df[headers[i]].astype(str) +  default_values[i]
    return df      