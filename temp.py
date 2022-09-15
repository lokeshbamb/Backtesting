import datetime
from tkinter import *
import tkinter
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import talib
from PIL import Image
from PIL import ImageTk
import quantstats as qs
import pandas_ta as ta
import vectorbt as vbt

company = pd.read_csv("all_company.csv",index_col=0,parse_dates=True,infer_datetime_format=True)
#company.set_index(['Date'],inplace=True)
entry = pd.read_csv("all_entry.csv",index_col=0,parse_dates=True,infer_datetime_format=True)
#entry.set_index(['Date'],inplace=True)
entry.fillna(False,inplace=True)
exit = pd.read_csv("all_exit.csv",index_col=0,parse_dates=True,infer_datetime_format=True)
#exit.set_index(['Date'],inplace=True)
exit.fillna(False,inplace=True)

pf = vbt.Portfolio.from_signals(company, entry, exit)

print("fhgj")

#fig = pf.total_return().vbt.barplot()
#fig = pf.qs.plot_snapshot()
#fig.update_layout(autosize=False, width=1900, height=930, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="LightSteelBlue",)

#fig.show()

#print(pf.stats(settings=dict(required_return=0.1, risk_free=0.07)))
#print(pf)
#print(dir(pf))
#pf.plot_trade_pnl().show()
#print(pf.daily_returns())

fig = pf.loc["HDFCBANK"].positions.plot()
fig.update_layout(autosize=False, width=1900, height=930, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="LightSteelBlue",)

fig.show()
