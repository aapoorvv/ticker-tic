import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import datetime
import matplotlib.pyplot as plt


# Start date calculator
def subtract_years(dt, years):
    try:
        dt = dt.replace(year=dt.year-years)
    except ValueError:
        dt = dt.replace(year=dt.year-years, day=dt.day-1)
    return dt
dt = subtract_years(datetime.datetime.now(),1)

# return -ve +ve
def check_return(x):
    if float(x)>0.0:
        return '🟢'
    elif float(x)<0.0:
        return '🔴'
    else:
        return '🟡'

stock = st.sidebar.text_input('Ticker',value="AAPL")
ticker = yf.Ticker(stock)
st.title(stock+' Stock Dashboard')

# Sidebar
start_date = st.sidebar.date_input('Start Date',value=dt.date())
end_date = st.sidebar.date_input('End Date')


data = yf.download(stock,start=start_date,end=end_date)
data_1yr = yf.download(stock,end=datetime.datetime.now(),start=dt.date())

line_chart,candlestick_chart= st.tabs(["Line Chart", "Candlestick Chart"])

# Line chart
with line_chart:
    fig = px.line(data, x = data.index, y = data['Adj Close'], title = stock.upper())
    st.plotly_chart(fig)    

# Candle Stick chart
with candlestick_chart:
    interval = st.selectbox(
    'Select Interval',
    ('1d', '5d', '1wk', '1mo'),
    index=1)
    
    ticker_history = ticker.history(interval=interval,period='1y')
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                        open=ticker_history['Open'],
                                        high=ticker_history['High'],
                                        low=ticker_history['Low'],
                                        close=ticker_history['Close'],
                                        increasing_line_color= '#00913a', decreasing_line_color= '#920809')])
    fig.update_layout(xaxis_rangeslider_visible=True)
    fig.update_layout(title=stock.upper())
    st.plotly_chart(fig, theme='streamlit')

# Tabs
pricing_data,fundamental_data,news,ca,holding,recc= st.tabs(["Pricing Data", "Fundamentals","News" , "Corporate Actions","Shareholding", "Experts Recommedation"])

with pricing_data:
    #data modify
    data_copy = data
    data_copy['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1)-1
    data_copy.dropna(inplace = True)
    
    data_df = pd.DataFrame(data_copy)
    data_df.reset_index(inplace=True)
    data_df['Date'] = data_df['Date'].dt.strftime('%Y/%m/%d')
    
    blankIndex=[''] * len(data_df)
    data_df.index=blankIndex
    if '% Change' in data_df.columns:
        del data_df['% Change']
    
    #data_1yr modify
    data_1yr_copy = data_1yr
    data_1yr['% Change'] = data_1yr_copy['Adj Close'] / data_1yr_copy['Adj Close'].shift(1)-1
    data_1yr.dropna(inplace = True)
    data_1yr = data_1yr.iloc[::-1]

    len_yr = len(data_1yr_copy)
    
    st.subheader("Today's Performance")
    
    col1, col2, col3= st.columns(3) 
    
    cmp = data_1yr['Adj Close'][0]*1
    col1.metric(label="CMP:", value=str("%.2f" % cmp))
    
    open = data_1yr['Open'][0]*1
    col2.metric(label="Today\'s Open :", value=str("%.2f" % open))
    
    prev_close = data_1yr['Adj Close'][1]*1
    col3.metric(label="Prev. Close:", value=str("%.2f" % prev_close))
    
    col4, col5, col6= st.columns(3) 
    high = data_1yr['High'][0]*1
    col4.metric(label="Today\'s High:", value=str("%.2f" % high))
    
    low = data_1yr['Low'][0]*1
    col5.metric(label="Today\'s low:", value=str("%.2f" % low))
    
    vol = data_1yr['Volume'][0]*1
    col6.metric(label="Volume:", value=str("%.0f" % vol))
    
    st.subheader("Returns")
    
    col1, col2, col3= st.columns(3) 
    #Day retrun
    day_return = data_1yr['% Change'][0]*100
    dr = str("%.2f" % day_return+' %')
    col1.metric(label="Day Return", value='', delta=dr) 
    
    #Last 1 Week Return
    week_return = data_1yr['% Change'].head(5).sum()*100
    wr = str("%.2f" % week_return+' %')
    col2.metric(label="Last 1 Week Return", value='', delta=wr) 
    
    #Last 1 Month Return
    m1_return = data_1yr['% Change'].head(int(len_yr/12)).sum()*100
    m1r = str("%.2f" % m1_return+' %')
    col3.metric(label="Last 1 Month Return", value='', delta=m1r) 
    
    col4, col5, col6 = st.columns(3) 
    #Last 3 Months Return
    m3_return = data_1yr['% Change'].head(int(len_yr/4)).sum()*100
    m3r = str("%.2f" % m3_return+' %')
    col4.metric(label="Last 3 Months Return", value='', delta=m3r) 
    
    #Last 6 Months Return
    m6_return = data_1yr['% Change'].head(int(len_yr/2)).sum()*100
    m6r = str("%.2f" % m6_return+' %')
    col5.metric(label="Last 6 Months Return", value='', delta=m6r) 
    
    #Last 1 Year Return
    annual_return = (data_1yr['% Change']).sum()*100
    ar = str("%.2f" % annual_return+' %')
    col6.metric(label="Last 1 Year Return", value='', delta=ar) 
    
    #Pricing Data
    st.subheader("Price Movements")
    st.write(data_df.iloc[::-1])
    
    
with fundamental_data:
    
    income,balance,cash= st.tabs(["Income Statement", "Balance Sheet", "Cashflow Statement"])
    
    with income:
        st.subheader('Annual Income Statement')
        ais_df = pd.DataFrame(ticker.income_stmt)
        ais_df.columns = ais_df.columns.strftime('%Y')
        st.write(ais_df.iloc[::-1])
        
        st.subheader('Quarterly Income Statement')
        qis_df = pd.DataFrame(ticker.quarterly_income_stmt)
        qis_df.columns = qis_df.columns.strftime('%Y-%m')
        st.write(qis_df.iloc[::-1])
    
    with balance:
        st.subheader('Annual Balance Sheet')
        abs_df = pd.DataFrame(ticker.balance_sheet)
        abs_df.columns = abs_df.columns.strftime('%Y')
        st.write(abs_df.iloc[::-1])
        
        st.subheader('Quarterly Balance Sheet')
        qbs_df = pd.DataFrame(ticker.quarterly_balance_sheet)
        qbs_df.columns = qbs_df.columns.strftime('%Y-%m')
        st.write(qbs_df.iloc[::-1])
    
    with cash:    
        st.subheader('Annual Cashflow Statement')
        acs_df = pd.DataFrame(ticker.cash_flow)
        acs_df.columns = acs_df.columns.strftime('%Y')
        st.write(acs_df.iloc[::-1])
        
        st.subheader('Quarterly Cashflow Statement')
        qcs_df = pd.DataFrame(ticker.quarterly_cash_flow)
        qcs_df.columns = qcs_df.columns.strftime('%Y-%m')
        st.write(qcs_df.iloc[::-1])
       
with news:
    news_data = ticker.news
    c = 1
    for i in news_data:
        h = f'{c}. '+i['title']
        st.subheader(h)
        st.write(f'By- {i["publisher"]}')
        st.write(i["link"])
        c+=1


with ca:
    # Dividends
    ticker = yf.Ticker(stock)
    st.subheader('Dividends')
    dividend = ticker.dividends
    dividend_df = pd.DataFrame(dividend)
    dividend_df.reset_index(inplace=True)
    dividend_df['Date'] = dividend_df['Date'].dt.strftime('%Y/%m/%d')
    blankIndex=[''] * len(dividend_df)
    dividend_df.index=blankIndex
    st.write(dividend_df.iloc[::-1].head(10))
    
    # Splits
    st.subheader('Splits')
    split = ticker.splits
    split_df = pd.DataFrame(split)
    split_df.reset_index(inplace=True)
    split_df['Date'] = split_df['Date'].dt.strftime('%Y/%m/%d')
    blankIndex=[''] * len(split_df)
    split_df.index=blankIndex
    st.write(split_df.tail(10).iloc[::-1])

with holding:
    # Institutional Investors
    ticker = yf.Ticker(stock)
    st.subheader("Institutional Investors")
    inst_hold_df = pd.DataFrame(ticker.institutional_holders)
    inst_hold_df['Date Reported'] = inst_hold_df['Date Reported'].dt.strftime('%Y/%m/%d')
    blankIndex=[''] * len(inst_hold_df)
    inst_hold_df.index=blankIndex
    st.write(inst_hold_df)

    # Mutual Fund Investors
    st.subheader("Mutual Fund Investors")
    mf_hold_df = pd.DataFrame(ticker.mutualfund_holders) 
    mf_hold_df['Date Reported'] = mf_hold_df['Date Reported'].dt.strftime('%Y/%m/%d')
    blankIndex=[''] * len(mf_hold_df)
    mf_hold_df.index=blankIndex
    st.write(mf_hold_df)
    
    # Insider Investors
    st.subheader("Insider Investors")
    inside_hold_df = pd.DataFrame(ticker.insider_roster_holders)
    if 'URL' in inside_hold_df.columns:
        del inside_hold_df['URL']
    if 'Position Direct Date' in inside_hold_df.columns:
        del inside_hold_df['Position Direct Date']
    if 'Position Indirect Date' in inside_hold_df.columns:
        del inside_hold_df['Position Indirect Date']
    inside_hold_df['Latest Transaction Date'] = inside_hold_df['Latest Transaction Date'].dt.strftime('%Y/%m/%d')
    blankIndex=[''] * len(inside_hold_df)
    inside_hold_df.index=blankIndex
    st.write(inside_hold_df) 
    
     
with recc:
    # Experts Recommedation
    ticker = yf.Ticker(stock)
    recc_df = pd.DataFrame(ticker.recommendations)
    labels = list(recc_df.head(1).columns[1:6])
    sizes =list(recc_df.iloc[0])[1:]
    if 'period' in recc_df.columns:
        del recc_df['period']
    blankIndex=[''] * len(recc_df)
    recc_df.index=blankIndex
    st.write(recc_df.head(1))
    
    #piechart
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, startangle=90,wedgeprops={'edgecolor':'black',"alpha": 0.7},textprops={'color':"w"})
    ax1.axis('equal')
    fig1.set_facecolor('#0f1117')
    st.pyplot(fig1)
    
    # dic = {
    # "Recommendation": labels,
    # "No. of Experts": sizes
    # }
    # df = pd.DataFrame.from_dict(dic)
    # sns.set(rc={'axes.facecolor':'#0f1117', 'figure.facecolor':'#0f1117'})
    # plot = sns.barplot(x="Recommendation", y="No. of Experts", data=df)
    # st.pyplot(plot.get_figure())
    
    