import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import datetime
import requests

KEY = "OQ54ZUXF90F2KGHL"
def subtract_years(dt, years):
    try:
        dt = dt.replace(year=dt.year-years)
    except ValueError:
        dt = dt.replace(year=dt.year-years, day=dt.day-1)
    return dt
dt = subtract_years(datetime.datetime.now(),1)
print(dt.date())


stock = st.sidebar.text_input('Ticker',value="AAPL")
stocks = yf.Ticker(stock)
start_date = st.sidebar.date_input('Start Date',value=dt.date())
end_date = st.sidebar.date_input('End Date')
st.title(stock+' Stock Dashboard')
data = yf.download(stock,start=start_date,end=end_date)
fig = px.line(data, x = data.index, y = data['Adj Close'], title = stock)
st.plotly_chart(fig)
isin = st.sidebar.text(f"ISIN: {stocks.isin}")
# st.write(stocks.info)
pricing_data,fundamental_data,news,ca,holding,recc= st.tabs(["Pricing Data", "Fundamentals","News" , "Corporate Actions","Shareholding", "Experts Recommedation"])

with pricing_data:
    st.header = ('Price Movements')
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1)-1
    data2.dropna(inplace = True)
    st.write(data2.iloc[::-1])
    annual_return = data2['% Change'].sum()*100
    st.write('1 year Return is',annual_return,'%')
    
    
with fundamental_data:
    st.subheader('Annual Income Statement')
    ais = stocks.income_stmt
    st.write(ais.iloc[::-1])
    
    st.subheader('Quarterly Income Statement')
    qis = stocks.quarterly_income_stmt
    st.write(qis.iloc[::-1])
    
    st.subheader('Annual Balance Sheet')
    abs = stocks.balance_sheet
    st.write(abs.iloc[::-1])
    
    st.subheader('Quarterly Balance Sheet')
    qbs = stocks.quarterly_balance_sheet
    st.write(qbs.iloc[::-1])
    
    st.subheader('Annual Cashflow Statement')
    acf = stocks.cash_flow
    st.write(acf.iloc[::-1])
    
    st.subheader('Quarterly Cashflow Statement')
    qcf = stocks.quarterly_cash_flow
    st.write(qcf.iloc[::-1])
       
with news:
    nd = stocks.news
    c = 1
    for i in nd:
        h = f'{c}. '+i['title']
        st.subheader(h)
        st.write(f'By- {i["publisher"]}')
        st.write(i["link"])
        c+=1


with ca:
    stocks = yf.Ticker(stock)
    st.subheader('Dividends')
    dividend = stocks.dividends
    st.write(dividend.iloc[::-1])
    st.subheader('Splits')
    split = stocks.splits
    st.write(split.iloc[::-1])

with holding:
    stocks = yf.Ticker(stock)
    st.subheader("Institutional Investors")
    st.write(stocks.institutional_holders) 
    st.subheader("MF Investors")
    st.write(stocks.mutualfund_holders) 
    st.subheader("Insider Investors")
    st.write(stocks.insider_roster_holders) 
    st.subheader("insidor")
    st.write(stocks.sustainability)
     
with recc:
    stocks = yf.Ticker(stock)
    recc = stocks.recommendations
    st.write(recc)