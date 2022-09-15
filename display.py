import datetime
from tkinter import *
import tkinter
from tkinter import ttk
import pandas as pd
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import talib
from PIL import Image
from PIL import ImageTk
import quantstats as qs
import pandas_ta as ta
import vectorbt as vbt

master = Tk()
newWindow = ""
counter = 1
widget = []
name_var = StringVar()
name_var1 = StringVar()
name_var2 = StringVar()
indicators = ["NUMBER", "CLOSE", "MA", "RSI", "VOLUME", "MACD"]
comparison = ["LESS THAN", "GREATER THAN", "EQUALS"]
df = pd.read_csv('ind_nifty200list.csv')
stocks = list(df['Symbol'])
#stocks = ["ACC"]
stock_dict = {}

for i in stocks:
	stock_dict[i] = pd.DataFrame()

def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

def submit_number(m):
	global name_var, newWindow
	s = str(m.get()) + "_" + str(name_var.get())
	m.set(s)
	newWindow.destroy()

def submit_ma(m):
	global name_var, newWindow
	s = str(m.get()) + "_" + str(name_var.get())
	m.set(s)
	newWindow.destroy()

def submit_rsi(m):
	global name_var, newWindow
	s = str(m.get()) + "_" + str(name_var.get())
	m.set(s)
	newWindow.destroy()

def submit_macd(m):
	global name_var, name_var1, name_var2, newWindow
	s = str(m.get()) + "_Slow" + str(name_var.get()) + "_Fast" + str(name_var1.get()) + "_Sigl" + str(name_var2.get())
	m.set(s)
	newWindow.destroy()

def callbackFunc1(event):
	global name_var, newWindow
	widget = event.widget
	if(str(widget.get()) == 'NUMBER'):
		newWindow = Toplevel(master)
		newWindow.title("Number")
		newWindow.geometry("240x60")
		newWindow.bind('<Return>', lambda t: submit_number(widget))
		label_name = Label(newWindow, text="Number : ",  font=('calibre',10,'normal'))
		label_name.grid(row=0, column=0)
		name_var.set("0")
		name_entry = Entry(newWindow, textvariable = name_var, font=('calibre',10,'normal'))
		name_entry.grid(row=0, column=1)
		name_entry.focus()
		sub_btn = Button(newWindow, text = 'Submit', command = lambda m=widget : submit_number(m))
		sub_btn.grid(row=1, column=1)
	
	if(str(widget.get()) == 'MA'):
		newWindow = Toplevel(master)
		newWindow.title("Moving Average")
		newWindow.geometry("240x60")
		newWindow.bind('<Return>', lambda t: submit_ma(widget))
		label_name = Label(newWindow, text="Period : ",  font=('calibre',10,'normal'))
		label_name.grid(row=0, column=0)
		name_var.set("20")
		name_entry = Entry(newWindow, textvariable = name_var, font=('calibre',10,'normal'))
		name_entry.grid(row=0, column=1)
		name_entry.focus()
		sub_btn = Button(newWindow, text = 'Submit', command = lambda m=widget : submit_ma(m))
		sub_btn.grid(row=1, column=1)
		
	elif(str(widget.get()) == 'RSI'):
		newWindow = Toplevel(master)
		newWindow.title("RSI")
		newWindow.geometry("240x60")
		newWindow.bind('<Return>', lambda t: submit_rsi(widget))
		label_name = Label(newWindow, text="Period : ",  font=('calibre',10,'normal'))
		label_name.grid(row=0, column=0)
		name_var.set("14")
		name_entry = Entry(newWindow, textvariable = name_var, font=('calibre',10,'normal'))
		name_entry.grid(row=0, column=1)
		name_entry.focus()
		sub_btn = Button(newWindow, text = 'Submit', command = lambda m=widget : submit_rsi(m))
		sub_btn.grid(row=1, column=1)
		
	elif(str(widget.get()) == 'MACD'):
		newWindow = Toplevel(master)
		newWindow.title("MACD")
		newWindow.geometry("270x120")
		newWindow.bind('<Return>', lambda t: submit_macd(widget))
		label_name = Label(newWindow, text="Shorter Period : ",  font=('calibre',10,'normal'))
		label_name.grid(row=0, column=0)
		name_var.set("12")
		name_entry = Entry(newWindow, textvariable = name_var, font=('calibre',10,'normal'))
		name_entry.grid(row=0, column=1)
		name_entry.focus()
		label_name1 = Label(newWindow, text="Longer Period : ",  font=('calibre',10,'normal'))
		label_name1.grid(row=1, column=0)
		name_var1.set("26")
		name_entry1 = Entry(newWindow, textvariable = name_var1, font=('calibre',10,'normal'))
		name_entry1.grid(row=1, column=1)
		label_name2 = Label(newWindow, text="Signal Period : ",  font=('calibre',10,'normal'))
		label_name2.grid(row=2, column=0)
		name_var2.set("9")
		name_entry2 = Entry(newWindow, textvariable = name_var2, font=('calibre',10,'normal'))
		name_entry2.grid(row=2, column=1)
		sub_btn = Button(newWindow, text = 'Submit', command = lambda m=widget : submit_macd(m))
		sub_btn.grid(row=3, column=1)
		
		
def switch(n):
	global is_on
	# Determine is on or off
	wid = all_children(master)
	on_button = n
	m = wid.index(n)
	m = int((m-1)/5 - 1)
	#print(wid)
	if is_on[m]:
		on_button.config(image = off)
		is_on[m] = False
	else:
		on_button.config(image = on)
		is_on[m] = True		

def remove_ind(m):
	global counter
	widget = all_children(master)
	n = widget.index(m)
	y_coord = m.winfo_rooty()
	for i in range(0,5,1):
		widget[n-i].destroy()
	del is_on[int((n-2)/5) - 1]
	#print(is_on)
	for i in range(int((n-2)/5), counter-1, 1):
		for j in range(3, 8, 1):
			widget[i*5 + j].place(y = 24*i)
	counter -= 1
	for i in range(0,3,1):
		widget[i].place(y = 10 + 24*counter)
		
	
def close_window():
	master.destroy()

def solve_logic(s1,s2,s3,company):
	l1 = s1.split("_")
	first = pd.Series(dtype = "float64")
	second = pd.Series(dtype = "float64")
	res = pd.Series(dtype = "float64")
	
	if(l1[0] == "MA"):
		first = company.ta.ema(length=int(l1[1]))
	elif(l1[0] == "RSI"):
		first = company.ta.rsi(length=int(l1[1]))
	elif(l1[0] == "MACD"):
		first = company.ta.macd(fast=int(l1[1][4:]), slow=int(l1[2][4:]), signal=int(l1[3][4:])).iloc[:,0]
	elif(l1[0] == "NUMBER"):
		temp = [int(l1[1])]*company.shape[0]
		first = pd.Series(temp, dtype = "float64", index = company.index)
	elif(l1[0] == "CLOSE"):
		first = company.Close
	elif(l1[0] == "VOLUME"):
		first = company.Volume
	else:
		print("Error", l1[0])
	
	l3 = s3.split("_")
	if(l3[0] == "MA"):
		second = company.ta.ema(length=int(l3[1]))
	elif(l3[0] == "RSI"):
		second = company.ta.rsi(length=int(l3[1]))
	elif(l3[0] == "MACD"):
		second, temp1, temp2 = company.ta.macd(fast=int(l3[1][4:]), slow=int(l3[2][4:]), signal=int(l3[3][4:]))
	elif(l3[0] == "NUMBER"):
		temp = [int(l3[1])]*company.shape[0]
		second = pd.Series(temp, dtype = "float64", index = company.index)
	elif(l3[0] == "CLOSE"):
		second = company.Close
	elif(l3[0] == "VOLUME"):
		second = company.Volume
	else:
		print("Error", l3[0])
	
	#print(first)
	#print(second)
	if(s2 == "GREATER THAN"):
		res = first > second
	elif(s2 == "LESS THAN"):
		res = first < second
	elif(s2 == "EQUALS"):
		res = first == second
	else:
		print("Error", s2)
	
	return res

def get_indicator():
	global stocks, stock_dict
	backtest = pd.DataFrame()
	widget = all_children(master)
	portfolio_return1 = pd.DataFrame()
	#print(widget)
	for i in range(0, len(is_on), 1):
		if(is_on[i]):
			s1 = str(widget[3+i*5].get())
			s2 = str(widget[4+i*5].get())
			s3 = str(widget[5+i*5].get())
			for comp in stocks:
				company = pd.read_csv("/home/lokesh/ML/NIFTY-200/"+comp+".csv")
				company = company.rename({'DATE':'Date', 'CLOSE':'Close', 'OPEN':'Open', 'HIGH':'High', 'LOW':'Low', 'VOLUME':'Volume'}, axis='columns')
				company.set_index(['Date'], inplace=True)
				company = company.iloc[::-1]
				stock_dict[comp]["Logic_" + str(i)] = solve_logic(s1,s2,s3,company)
			print(i)
	
	all_company = pd.DataFrame()
	all_entry = pd.DataFrame()
	all_exit = pd.DataFrame()
	
	for comp in stocks:
		#print(stock_dict["ACC"])
		company = pd.read_csv("/home/lokesh/ML/NIFTY-200/"+comp+".csv")
		company = company.rename({'DATE':'Date', 'CLOSE':'Close', 'OPEN':'Open', 'HIGH':'High', 'LOW':'Low', 'VOLUME':'Volume'}, axis='columns')
		company.set_index(['Date'], inplace=True)
		company = company.iloc[::-1]
		col_names = list(stock_dict[comp])
		ema_entries = stock_dict[comp][col_names[0]]
		for i in range(1,len(col_names),1):
			ema_entries = ema_entries & stock_dict[comp][col_names[i]]
		ema_exit = ~stock_dict[comp][col_names[0]]
		for i in range(1,len(col_names),1):
			ema_exit = ema_exit | ~stock_dict[comp][col_names[i]]
		
		pf_tikr = vbt.Portfolio.from_signals(company.Close, entries=ema_entries, exits=ema_exit, freq="D", init_cash=100000, fees=0.0025, slippage=0.0025)
		
		portfolio_return = pf_tikr.stats(settings=dict(required_return=0.15, risk_free=0.07))
		portfolio_return = portfolio_return.to_frame()#.reset_index()
		portfolio_return = portfolio_return.rename(columns= {0: comp})
		
		if(comp == "ACC"):
			portfolio_return1 = portfolio_return
			all_company["ACC"] = company.Close
			all_entry["ACC"] = ema_entries
			all_exit["ACC"] = ema_exit
		else:
			portfolio_return1 = pd.concat([portfolio_return1,portfolio_return], axis=1)
			all_company[comp] = company.Close
			all_entry[comp] = ema_entries
			all_exit[comp] = ema_exit
	
	all_entry.to_csv("all_entry.csv")
	all_exit.to_csv("all_exit.csv")
	all_company.to_csv("all_company.csv")
	print(all_entry)
	print(all_exit)
	print(all_company)	
	portfolio_return1 = portfolio_return1.T
	portfolio_return1.index.name = "Company"
	portfolio_return1.to_csv("total.csv")

def add_indicator():
	global counter
	global add_indicator
	global get_indicator
	global is_on
	E1 = ttk.Combobox(master, values=indicators, state='readonly')
	E1.place(x = 5, y = 24*counter)
	#E1.pack(side = 'left')
	E1.set('CLOSE_13456')
	E1.bind("<<ComboboxSelected>>", callbackFunc1)
	E2 = ttk.Combobox(master, values=comparison, state='readonly')
	E2.place(x = 170, y = 24*counter)
	E2.set("GREATER THAN")
	E3 = ttk.Combobox(master, values=indicators, state='readonly')
	E3.place(x = 320, y = 24*counter)
	#E1.pack(side = 'left')
	E3.set('CLOSE')
	E3.bind("<<ComboboxSelected>>", callbackFunc1)
	#temp = len(all_children(master))
	on_button = Button(master, image = on, bd=0, height = 18, width = 36)#, command = lambda m=temp : switch(m))
	on_button.config(command = lambda m=on_button : switch(m))
	on_button.place(x = 510, y = 24*counter)
	is_on.append(True)
	delete_ind = Button(master, image = cross, bd=0, height = 18, width = 18)#, command = lambda m=temp : switch(m))
	delete_ind.config(command = lambda m=delete_ind : remove_ind(m))
	delete_ind.place(x = 550, y = 24*counter)
	counter += 1
	get_indicator.place(x = 60, y = 10 + 24*counter)
	add_indicator.place(x = 5, y = 10 + 24*counter)
	close_window.place(x = 115, y = 10 + 24*counter)


width = 36
height = 18
img = Image.open("on.png")
img = img.resize((width,height), Image.ANTIALIAS)
on =  ImageTk.PhotoImage(img)

img = Image.open("off.png")
img = img.resize((width,height), Image.ANTIALIAS)
off =  ImageTk.PhotoImage(img)

img = Image.open("cross.jpeg")
img = img.resize((height,height), Image.ANTIALIAS)
cross =  ImageTk.PhotoImage(img)

add_indicator = Button(master, text="Add", command=add_indicator)
add_indicator.place(x = 5, y = 10)

get_indicator = Button(master, text="Run", command=get_indicator)
get_indicator.place(x = 60, y = 10)
is_on = []

close_window = Button(master, text="Exit", command=close_window)
close_window.place(x = 115, y = 10)

master.geometry('1520x750')
mainloop()
