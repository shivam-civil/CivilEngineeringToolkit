


def analyze_sieve(df,total_mass = None):
    '''
    This function should return a dataframe,list of [d10,d30,d60] and lits of [Cv,Cc]
    '''
    import pandas as pd 
    import numpy as np
    if not isinstance(total_mass,float) :
        total_mass = round(df['MassRetained(gm)'].sum(),3)
    else : 
        total_mass = round(total_mass, 3)  

    df['PercentageRetained'] = round((df["MassRetained(gm)"]/total_mass)*100,3)
    df['CumulativePercentage'] = round(df["PercentageRetained"].cumsum(),3)
    df['PercentagePassing'] = round(100-df['CumulativePercentage'],3)
    df['PercentagePassing'] = df['PercentagePassing'].clip(lower=0)

    
    df.sort_values("SieveSize(mm)").reset_index(drop=True)
    sizes = df["SieveSize(mm)"].values
    passing = df["PercentagePassing"].values 

    sizes = sizes[::-1]
    passing = passing[::-1]

    log_sizes = np.log10(sizes)

    # interpolate in log scale
    d10 = round(10 ** np.interp(10, passing, log_sizes), 4)
    d30 = round(10 ** np.interp(30, passing, log_sizes), 4)
    d60 = round(10 ** np.interp(60, passing, log_sizes), 4)

    Cv = round(d60/d10,3)
    Cc = round((d30**2)/(d10*d60),3)
    d = [d10,d30,d60]
    coeff = [Cv,Cc]

    return df, d, coeff





def plot_psd(df, d_values):
    import plotly.graph_objects as go
    fig = go.Figure()

    # PSD curve
    fig.add_trace(go.Scatter(
        x=df["SieveSize(mm)"],
        y=df["PercentagePassing"],
        mode='lines+markers',
        name='PSD Curve'
    ))

    # D10, D30, D60 markers
    labels = ['D10', 'D30', 'D60']
    percents = [10, 30, 60]
    for label, d, p in zip(labels, d_values, percents):
        fig.add_trace(go.Scatter(
            x=[d],
            y=[p],
            mode='markers+text',
            name=label,
            text=[label],
            textposition='top center'
        ))

    fig.update_layout(
        xaxis=dict(type='log', title='Sieve Size (mm)'),
        yaxis=dict(title='% Passing'),
        title='Particle Size Distribution Curve'
    )

    return fig
