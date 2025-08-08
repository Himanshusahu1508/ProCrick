import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Cricket Data Analysis", layout="wide")
st.title("🏏 IPL Cricket Data Analysis Dashboard")

@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Top Batsmen", "Death Over Bowlers"])

if section == "Overview":
    st.header("📊 Dataset Overview")
    st.dataframe(matches.head())

elif section == "Top Batsmen":
    st.header("🏏 Top Batsmen by Runs")
    top_batsmen = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    top_batsmen.plot(kind='bar', ax=ax)
    st.pyplot(fig)

elif section == "Death Over Bowlers":
    st.header("🔥 Top Bowlers in Death Overs (16-20)")
    death_overs = deliveries[(deliveries['over'] >= 16)]
    death_bowlers = (death_overs.groupby('bowler')['player_dismissed']
                     .count().sort_values(ascending=False).head(10))
    fig, ax = plt.subplots()
    death_bowlers.plot(kind='bar', color='orange', ax=ax)
    st.pyplot(fig)

selected_team = st.sidebar.selectbox("Select Team", matches["team1"].unique())

import plotly.express as px
fig = px.bar(death_bowlers.reset_index(), x='bowler', y='player_dismissed')
st.plotly_chart(fig)

st.metric("Total Matches", len(matches))
st.metric("Unique Players", deliveries['batsman'].nunique())
