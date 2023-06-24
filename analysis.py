import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

#set a webpage title 

st.set_page_config(page_title= "Internet usage" 
                   , layout= "wide")
st.title("Internet Usage analysis(1980-2020)")
st.write("Ineract with this dashboard using widgets on sidebar")

internet = pd.read_csv("data/internet.csv")

internet.info()

#sidebar 
#creating sidebar widget  unique values 
year_list = internet['Year'].unique().tolist()

country_list = internet['Entity'].unique().tolist()

with st.sidebar:
    #create a selectbox option

    year = st.selectbox("Please choose a year to display the top 10 countries with the \
                        highest internet usage based onpopulation share and the top 5 countries\
                         with the largest number of internet users", year_list, 10 )

    country = st.selectbox("Choose a country to visualize the historical trend of internet usage.", country_list, 10 )

    user_country_selct= (internet['Entity'].isin(country_list)) 

    user_year_selct = (internet['Year'] == year)

#VISUALIZATION SECTION

col1, col2 = st.columns((2,1))

with col1:
    st.subheader("top 10 countries with the highest internet use (by population share)")
    top_ten = internet[user_year_selct].groupby(['Entity'])['Internet Users(%)'].sum()
    top_ten = top_ten.sort_values(ascending=False).head(10)
    st.dataframe(top_ten, width= 400)

    user_selection = (internet['Entity'] == country)
    specific_country = internet[user_selection]

    figpx = px.line(specific_country, x='Year', y='Internet Users(%)',
                 title="Internet usage over time for " + country)
    st.plotly_chart(figpx, use_container_width=True ,height=800)

with col2:
    figpx =px.choropleth(internet, 
                    locations='Entity',
                    locationmode='country names',
                    color='Internet Users(%)',
                    title='Internet Usage by Country')

    st.plotly_chart(figpx, use_container_width=True ,height=800)


    other = 'World', 'Asia', 'Upper-middle-income countries',  'High-income countries', 'Lower-middle-income countries', 'Europe', 'North America' , 'South America', 'Africa'
    no_other = internet[user_year_selct][~internet[user_year_selct]['Entity'].isin(other)]
    top_five_users = no_other.groupby('Entity')['No. of Internet Users'].sum().sort_values(ascending=False).head(5)
    
    figpx1 = px.bar(x = top_five_users.index, y = top_five_users,
                    title="Top 5 countries with most internet users")
    figpx1.update_layout(xaxis_title="Countries", yaxis_title="Number of Internet Users")

    colors = ['#FF5733', '#FFC300', '#C70039', '#900C3F', '#581845']
    figpx1.update_traces(marker=dict(color=colors))
    st.plotly_chart(figpx1, use_container_width=True ,height=800)
    
