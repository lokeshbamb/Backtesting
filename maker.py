import pandas as pd
import pandas_ta as ta
import vectorbt as vbt
import yfinance as yf
import nsepy
import quantstats as qs
import datetime

def portfolio_fun(tikr):
  portfolio_return1 = pd.DataFrame()
  for i in tikr:
     try:
      df2 = pd.read_csv("/home/lokesh/ML/NIFTY-200/"+i+".csv")
      df2 = df2.rename({'DATE':'Date', 'CLOSE':'Close', 'OPEN':'Open', 'HIGH':'High', 'LOW':'Low', 'VOLUME':'Volume'}, axis='columns')
      df2.set_index(['Date'], inplace=True)
      df2 = df2.iloc[::-1]
      
      ema_entries = ((df2.Close > df2.ta.ema(length=20, append=True)) & (df2.ta.rsi(length=14, append=True)>50) & (df2.Close > df2.ta.ema(length=13, append=True)) & 
                     (df2.Close < df2.ta.ema(length=13, append=True)*1.05) & (df2.ta.ema(length=20, append=True) > df2.ta.ema(length=50, append=True)))  | (df2.ta.rsi(length=14, append=True) < 30)
      ema_exits = (df2.ta.rsi(length=14, append=True) > 75)
      
      df2["TS_Entries"] = ema_entries
      df2["TS_Exits"] = ema_exits
      
      pf_tikr = vbt.Portfolio.from_signals(df2.Close, entries=ema_entries, exits=ema_exits, freq="D", init_cash=100000, fees=0.0025, slippage=0.0025)
      
      portfolio_return = pf_tikr.stats(settings=dict(required_return=0.15, risk_free=0.07))
      portfolio_return = portfolio_return.to_frame()#.reset_index()
      portfolio_return = portfolio_return.rename(columns= {0: i})
      
      if(i == 'ACC'):
          portfolio_return1 = portfolio_return
      else:
          portfolio_return1 = pd.concat([portfolio_return1,portfolio_return], axis=1)
     
     except:
      print(i)
      
  return(portfolio_return1)
  
df = pd.read_csv('ind_nifty200list.csv')
stocks = list(df['Symbol'])
tikr = ['TCS', 'RELIANCE', 'HDFCBANK', 'HDFC', 'INFY', 'ITC', 'SBIN', 'ONGC', 'COALINDIA', 'POWERGRID', 'NTPC', 'HCLTECH', 'WIPRO', 'ICICIBANK', 'TATACHEM', 'HINDZINC', 'TATASTEEL', 'HINDUNILVR', 'LT', 'GAIL', 'KOTAKBANK', 'PFC', 'MARUTI', 'ULTRACEMCO', 'JSWSTEEL', 'BAJAJ-AUTO', 'BAJFINANCE', 'TECHM', 'INDUSINDBK', 'HEROMOTOCO', 'NMDC', 'SUNPHARMA', 'BANDHANBNK', 'MUTHOOTFIN', 'NHPC', 'DRREDDY', 'HAL', 'PETRONET', 'BPCL', 'ASIANPAINT', 'HINDPETRO', 'OIL', 'SRTRANSFIN', 'LICHSGFIN', 'CIPLA', 'DLF', 'IBULHSGFIN', 'SAIL', 'ADANIPORTS', 'EICHERMOT', 'RTNPOWER', 'AUROPHARMA', 'BAJAJHLDNG', 'BEL', 'INDUSTOWER', 'HUDCO', 'SJVN', 'AXISBANK', 'OFSS', 'SHREECEM', 'LTI', 'FEDERALBNK', 'TITAN', 'BRITANNIA', 'SBILIFE', 'NIACL', 'NLCINDIA', 'CADILAHC', 'MRF', 'DIVISLAB', 'SUNTV', 'NIITLTD', 'GLENMARK', 'DMART', 'M&M', 'IOC', 'HDFCLIFE', 'GRASIM', 'ALKEM', 'HDFCAMC', 'SBICARD', 'TORNTPOWER', 'MANAPPURAM', 'CHAMBLFERT', 'MPHASIS', 'ICICIGI', 'GUJGASLTD', 'GODREJCP', 'DABUR', 'IGL', 'GSPL', 'PIDILITIND', 'ICICIPRULI', 'COROMANDEL', 'CHOLAFIN', 'RELINFRA', 'MARICO']
final = portfolio_fun(tikr)

final.to_csv("temp.csv")
