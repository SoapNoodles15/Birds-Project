# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 12:57:11 2022
@author: Ja
"""

from  numpy import *
from  matplotlib.pyplot import *
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkcalendar import *
import tkcalendar
import astral
from astral import sun



'''
f = open('C:/Users/Ja/Desktop/Python Projects/bird_jan25jan16.txt', 'r')
linelist = f.readlines()
f.close
### Replace wrong gaps
f2 = open('C:/Users/Ja/Desktop/Python Projects/bird_jan25jan16.txt', 'w')
for line in linelist:
    if line[26:30] != "    ":
        line = line.replace(line[26:30], '    ')
    f2.write(line)
f2.close()
'''

df = pd.read_csv("D:/OLD SCHOOL STUFF/Python Projects/bird_jan25jan16.txt", 
                 sep='    ',engine='python',
                 names = ['Date','No. of movements'])

df['Date'] = pd.to_datetime(df['Date'],utc=True)
df['Date'] = df['Date'].dt.tz_convert('Europe/Copenhagen')

def func1(df):
    if isinstance(df, pd.DataFrame):
        df = df.set_index('Date').resample('2T').ffill().reset_index()
        df.fillna(method = 'bfill', inplace=True)
        for index, row in df.iterrows():
            if index != 0 and df.iloc[index][1] != 0 and abs((df.iloc[index][1]-df.iloc[index-1][1])) > 8:
                if abs((df.iloc[index-1][1]-df.iloc[index+1][1])) < 16:
                    df.at[index, 'No. of movements'] = (df.iloc[index-1][1]+df.iloc[index+1][1])//2       
                else:
                    df.at[index,'No. of movements'] = (df.iloc[index-1][1])+8
        return(df)
    else:
        return(f"{df} is not a dataframe")
    
data=func1(df)

### Data for plots
root = Tk()

def setmode(selection):
    global mode
    mode = selection
    return mode

options = StringVar()
menu = OptionMenu(root, options, 'Hourly', 'Daily', 'Weekly', command=setmode)
menu.pack()
options.set('Interval')

def date_range(start,stop):
    global dates
    dates = []
    dates.append(start)
    dates.append(stop)
    return dates
    

date1 = tkcalendar.DateEntry(root)
date1.pack(padx=10,pady=10)

date2 = tkcalendar.DateEntry(root)
date2.pack(padx=10,pady=10)

Button(root,text='Set range',command=lambda: date_range(date1.get_date(),date2.get_date())).pack()

root.mainloop()


input1 = str(dates[0])
input2 = str(dates[1])

date1 = data.index[data['Date'].astype(str).str.contains('|'.join([input1, input2]))].tolist()[0]
date2 = data.index[data['Date'].astype(str).str.contains('|'.join([input1, input2]))].tolist()[-1]

data['DT'] = None
Observer = astral.Observer(latitude = 55.6761, longitude = 12.5683)#Copenhagen

if mode == 'Hourly':
    data = data.iloc[date1-1:date2].set_index('Date').resample('H').bfill().reset_index()
    data['Movements hourly'] = data['No. of movements'] - data['No. of movements'].shift(periods = 1, fill_value = 0)
    
    for index, row in data.iterrows():
        if data.iloc[index]['Movements hourly'] < 0:
            data.at[index, 'Movements hourly'] == 0
            
    data = data.drop(0).reset_index()
    data = data.drop(columns='index')
    
    
    for index, row in data.iterrows():
        if astral.sun.sunrise(Observer, date=data.iloc[index]['Date']) < data.iloc[index]['Date'] < astral.sun.sunset(Observer, date=data.iloc[index]['Date']):
            data.at[index,'DT'] = 1
        else:
            data.at[index,'DT'] = 0
    data['Date'] = data['Date'].dt.strftime('%d-%m-%Y %H')
    
    fig, ax = plt.subplots(figsize=(20,15))
    ax.bar(data['Date'], data['Movements hourly'], color = 'green')
    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)
    plt.setp(ax.xaxis.get_ticklabels(), rotation = 45, fontsize = 15, ha = 'right', rotation_mode = 'anchor')
    ax.tick_params('y',labelsize = 20)
    ax.set_ylabel('Movements per hour', fontsize=25)
    ax.set_xlabel('Time in hours', fontsize=25)
    
    ax2 = ax.twinx()
    ax2.bar(data['Date'], data['DT'],color = 'yellow' ,alpha = 0.3)
    ax2.axes.get_yaxis().set_visible(False)
    
    plt.show()

elif mode == 'Daily':
    data = data.iloc[(date1-721):date2].set_index('Date').resample('D').bfill().reset_index()
    data['Movements daily'] = data['No. of movements'] - data['No. of movements'].shift(periods = 1, fill_value = 0)
    
    for index, row in data.iterrows():
        if data.iloc[index]['Movements daily'] < 0:
            data.at[index, 'Movements daily'] = df.iloc[index][1]
            
    data = data.drop([0,1]).reset_index()
    data = data.drop(columns='index')
    
    data['Date'] = data['Date'].dt.strftime('%d-%m')
    
    plot = data.plot.bar(x='Date', y='Movements daily')


elif mode == 'Weekly':
    data = data.iloc[date1-1:date2].set_index('Date').resample('W').bfill().reset_index()
    data['Movements weekly'] = data['No. of movements'] - data['No. of movements'].shift(periods = 1, fill_value = 0)
    
    for index, row in data.iterrows():
        if data.iloc[index]['Movements weekly'] < 0:
            data.at[index, 'Movements weekly'] == 0
            
    data = data.drop(0).reset_index()
    data = data.drop(columns='index')
    
    data['Date'] = data['Date'].dt.strftime('%Y week: %W')
    plot = data.plot.bar(x='Date', y='Movements weekly')