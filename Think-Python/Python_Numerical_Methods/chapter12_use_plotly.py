#%%
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

#%%
df = pd.DataFrame(dict(x = [0, 1, 2, 3], y = [0, 1, 4, 9]))
fig = px.line(df, x="x", y="y") 
fig.show()

#%%
xlist = np.linspace(-5, 5, 100)
df = pd.DataFrame(dict(x = xlist, y = xlist**2))
fig = px.line(df, x="x", y="y") 
fig.show()

#%%
xlist = np.linspace(-5, 5, 20)
fig = go.Figure()
fig.add_trace(go.Scatter(x = xlist, y = xlist**2, name = 'x**2'))
fig.add_trace(go.Scatter(x = xlist, y = xlist**3, name = 'x**3'))
fig.update_layout(title=f'Plot of Various Polynomials from {xlist[0]} to {xlist[-1]}',
                   xaxis_title='X axis',
                   yaxis_title='Y axis')
fig.show()

#%% 直方圖
xlist = np.arange(11)
df = pd.DataFrame(dict(x = xlist, y = xlist**2))
fig = px.bar(df, x="x", y="y")
fig.show()

# %%
