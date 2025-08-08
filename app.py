import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Page config
st.set_page_config(page_title="IPL Cricket Analysis Dashboard", layout="wide")
st.title("🏏 IPL Cricket Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Team Stats", "Player Stats", "Death Overs", "About"])

# Overview Section
if section == "Overview":
    st.subheader("IPL Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches", matches.shape[0])
    col2.metric("Total Seasons", matches["season"].nunique())
    col3.metric("Total Teams", matches["team1"].nunique())
    col4.metric("Unique Venues", matches["venue"].nunique())

    st.markdown("---")
    
    season_wins = matches["season"].value_counts().sort_index()
    fig = px.bar(x=season_wins.index, y=season_wins.values, labels={'x': 'Season', 'y': 'Number of Matches'}, title="Matches Per Season")
    st.plotly_chart(fig, use_container_width=True)

    win_counts = matches["winner"].value_counts()
    st.subheader("Most Successful Teams")
    fig2 = px.bar(win_counts.head(10), x=win_counts.head(10).index, y=win_counts.head(10).values, labels={'x': 'Team', 'y': 'Wins'}, title="Top Winning Teams")
    st.plotly_chart(fig2, use_container_width=True)

# Team Stats Section
elif section == "Team Stats":
    st.subheader("Team Performance")
    selected_team = st.selectbox("Select a Team", sorted(matches["team1"].unique()))

    team_matches = matches[(matches["team1"] == selected_team) | (matches["team2"] == selected_team)]
    total_wins = (matches["winner"] == selected_team).sum()
    win_percent = (total_wins / team_matches.shape[0]) * 100

    col1, col2 = st.columns(2)
    col1.metric("Matches Played", team_matches.shape[0])
    col2.metric("Win %", f"{win_percent:.2f}%")

    st.markdown("---")
    
    yearly_perf = team_matches[team_matches["winner"] == selected_team]["season"].value_counts().sort_index()
    fig = px.line(x=yearly_perf.index, y=yearly_perf.values, labels={'x': 'Season', 'y': 'Wins'}, title=f"{selected_team} Wins per Season")
    st.plotly_chart(fig, use_container_width=True)

# Player Stats Section
elif section == "Player Stats":
    st.subheader("Top Players")
    top_batsmen = deliveries.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(10)
    top_4s = deliveries[deliveries["batsman_runs"] == 4]["batsman"].value_counts().head(10)
    top_6s = deliveries[deliveries["batsman_runs"] == 6]["batsman"].value_counts().head(10)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Top Run Scorers**")
        fig3 = px.bar(top_batsmen, x=top_batsmen.values, y=top_batsmen.index, orientation='h', labels={'x': 'Runs', 'y': 'Player'})
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown("**Most 4s Hit**")
        fig4 = px.bar(top_4s, x=top_4s.values, y=top_4s.index, orientation='h', labels={'x': 'Fours', 'y': 'Player'})
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**Most 6s Hit**")
    fig5 = px.bar(top_6s, x=top_6s.values, y=top_6s.index, orientation='h', labels={'x': 'Sixes', 'y': 'Player'})
    st.plotly_chart(fig5, use_container_width=True)

# Death Overs Stats
elif section == "Death Overs":
    st.subheader("Top Bowlers in Death Overs (16-20)")
    death_bowling = deliveries[(deliveries["over"] >= 16) & (deliveries["over"] <= 20)]
    top_bowlers = death_bowling.groupby("bowler")["total_runs"].sum().sort_values().head(10)
    fig6 = px.bar(top_bowlers, x=top_bowlers.values, y=top_bowlers.index, orientation='h', labels={'x': 'Runs Conceded', 'y': 'Bowler'})
    st.plotly_chart(fig6, use_container_width=True)

# About Page
elif section == "About":
    st.markdown("""
    ## 🧾 About this App
    - This is an advanced cricket data analysis dashboard built with **Streamlit**.
    - Data Source: Kaggle IPL Dataset (matches & deliveries)
    - Features:
        - Interactive filters
        - Visual insights into teams, players, seasons
        - Death over bowling stats
        - Ready for integration with live data (e.g., Cricbuzz)

    #### 👨‍💻 Developed by: [Himanshu Sahu]
    """)
