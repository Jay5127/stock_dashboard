import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px


st.title('Stock Dashboard')
search = st.sidebar.text_input('Search Name')
start = st.sidebar.date_input('Start Date')
end = st.sidebar.date_input('End Date')


if search and start and end:
    data = yf.download(search, start=start, end=end)
    
    if not data.empty:
        fig = px.line(data, x=data.index, y='Adj Close', title='Stock Price Over Time')
        st.plotly_chart(fig)
    else:
        st.error("No data available for the given search term and date range.")
else:
    st.info("Please fill in the search term, start date, and end date to display the stock data.")

pricing_data , news = st.tabs(['Pricing Data', 'News'])


with pricing_data:
    st.header('Price Movement')
    if search and start and end:
        data = yf.download(search, start=start, end=end)
        data2 = data
        data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
        data2.dropna(inplace = True)
        st.write(data2)
        
        annual_return = data2['% Change'].mean()*252*100
        st.write('The annual return is',annual_return,'%')  


        std = np.std(data2['% Change'])*np.sqrt(252)
        st.write('Standard deviation is',std*100,'%')

        st.write('Risk Adj. Return is',annual_return/(std*100))


from stocknews import StockNews
with news:
    st.header('News')
    sn = StockNews(search , save_news= False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News sentiment {news_sentiment}')

