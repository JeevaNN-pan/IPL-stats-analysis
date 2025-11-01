import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B35, #004E89);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_data():
    """Load IPL datasets"""
    try:
        matches = pd.read_csv('matches.csv')
        deliveries = pd.read_csv('deliveries.csv')
        
        # Data cleaning
        matches['city'].fillna('Unknown', inplace=True)
        matches['winner'].fillna('No Result', inplace=True)
        matches['player_of_match'].fillna('Unknown', inplace=True)
        
        # Merge deliveries with matches to get season info
        deliveries = deliveries.merge(
            matches[['id', 'season']], 
            left_on='match_id', 
            right_on='id', 
            how='left'
        )
        
        return matches, deliveries
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

matches, deliveries = load_data()

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("🏏 IPL Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Team Analysis", "⭐ Player Stats", "🏟️ Venue Analysis", "📈 Trends & Insights"]
)

st.sidebar.markdown("---")
st.sidebar.info("**Data Source:** IPL 2008-2024\n\n**Created by:** Jeevan\n\n**Tech:** Python, Streamlit, Plotly")

# ============================================
# HOME PAGE
# ============================================

if page == "🏠 Home":
    st.markdown('<p class="main-header">🏏 IPL Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Analysis of Indian Premier League (2008-2024)")
    
    if matches is not None:
        # Key Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Matches", len(matches))
        with col2:
            st.metric("Total Seasons", matches['season'].nunique())
        with col3:
            st.metric("Total Teams", matches['team1'].nunique())
        with col4:
            st.metric("Total Venues", matches['venue'].nunique())
        
        st.markdown("---")
        
        # Matches per season
        st.subheader("📈 Matches Played Per Season")
        matches_per_season = matches.groupby('season').size().reset_index(name='matches')
        fig = px.bar(matches_per_season, x='season', y='matches',
                     color='matches', color_continuous_scale='Blues',
                     labels={'season': 'Season', 'matches': 'Number of Matches'})
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Two columns for additional stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top 5 Teams by Wins")
            team_wins = matches['winner'].value_counts().head(5).reset_index()
            team_wins.columns = ['Team', 'Wins']
            fig = px.bar(team_wins, x='Wins', y='Team', orientation='h',
                        color='Wins', color_continuous_scale='Greens')
            fig.update_layout(showlegend=False, height=300, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🪙 Toss Impact Analysis")
            matches_with_result = matches[matches['winner'] != 'No Result'].copy()
            matches_with_result['toss_winner_is_match_winner'] = (
                matches_with_result['toss_winner'] == matches_with_result['winner']
            )
            toss_impact = matches_with_result['toss_winner_is_match_winner'].value_counts()
            fig = go.Figure(data=[go.Pie(labels=['Won Match', 'Lost Match'], 
                                         values=toss_impact.values,
                                         hole=.3)])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# TEAM ANALYSIS PAGE
# ============================================

elif page == "📊 Team Analysis":
    st.markdown('<p class="main-header">📊 Team Performance Analysis</p>', unsafe_allow_html=True)
    
    if matches is not None:
        # Team selector
        teams = sorted(matches['team1'].unique())
        selected_team = st.selectbox("Select a Team", teams)
        
        # Team stats
        team_matches = matches[(matches['team1'] == selected_team) | (matches['team2'] == selected_team)]
        team_wins = matches[matches['winner'] == selected_team]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Matches", len(team_matches))
        with col2:
            st.metric("Total Wins", len(team_wins))
        with col3:
            win_rate = (len(team_wins) / len(team_matches) * 100) if len(team_matches) > 0 else 0
            st.metric("Win Rate", f"{win_rate:.1f}%")
        with col4:
            total_losses = len(team_matches) - len(team_wins)
            st.metric("Total Losses", total_losses)
        
        st.markdown("---")
        
        # Season-wise performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"🏆 {selected_team} - Season Wise Wins")
            season_wins = team_wins.groupby('season').size().reset_index(name='wins')
            fig = px.line(season_wins, x='season', y='wins', markers=True,
                         labels={'season': 'Season', 'wins': 'Wins'})
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader(f"🏟️ Top Venues for {selected_team}")
            venue_performance = team_wins['venue'].value_counts().head(5).reset_index()
            venue_performance.columns = ['Venue', 'Wins']
            fig = px.bar(venue_performance, x='Wins', y='Venue', orientation='h',
                        color='Wins', color_continuous_scale='Oranges')
            fig.update_layout(showlegend=False, height=350, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# PLAYER STATS PAGE
# ============================================

elif page == "⭐ Player Stats":
    st.markdown('<p class="main-header">⭐ Player Statistics</p>', unsafe_allow_html=True)
    
    if matches is not None and deliveries is not None:
        tab1, tab2, tab3 = st.tabs(["🏏 Batsmen", "⚾ Bowlers", "🏅 Awards"])
        
        with tab1:
            st.subheader("Top Run Scorers in IPL History")
            num_batsmen = st.slider("Number of batsmen to display", 5, 20, 10)
            
            # Fixed: using 'batter' instead of 'batsman'
            top_batsmen = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(num_batsmen).reset_index()
            top_batsmen.columns = ['Batsman', 'Total Runs']
            
            fig = px.bar(top_batsmen, x='Total Runs', y='Batsman', orientation='h',
                        color='Total Runs', color_continuous_scale='YlOrRd')
            fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Top Wicket Takers in IPL History")
            num_bowlers = st.slider("Number of bowlers to display", 5, 20, 10)
            
            # Fixed: using 'player_dismissed' to check for wickets
            wickets = deliveries[deliveries['player_dismissed'].notna()]
            top_bowlers = wickets.groupby('bowler').size().sort_values(ascending=False).head(num_bowlers).reset_index()
            top_bowlers.columns = ['Bowler', 'Total Wickets']
            
            fig = px.bar(top_bowlers, x='Total Wickets', y='Bowler', orientation='h',
                        color='Total Wickets', color_continuous_scale='Purples')
            fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Player of the Match Awards")
            num_players = st.slider("Number of players to display", 5, 20, 10)
            
            top_pom = matches['player_of_match'].value_counts().head(num_players).reset_index()
            top_pom.columns = ['Player', 'Awards']
            
            fig = px.bar(top_pom, x='Awards', y='Player', orientation='h',
                        color='Awards', color_continuous_scale='Greens')
            fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# VENUE ANALYSIS PAGE
# ============================================

elif page == "🏟️ Venue Analysis":
    st.markdown('<p class="main-header">🏟️ Venue Analysis</p>', unsafe_allow_html=True)
    
    if matches is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Venues by Number of Matches")
            top_venues = matches['venue'].value_counts().head(10).reset_index()
            top_venues.columns = ['Venue', 'Matches']
            
            fig = px.bar(top_venues, x='Matches', y='Venue', orientation='h',
                        color='Matches', color_continuous_scale='Blues')
            fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("City-wise Match Distribution")
            city_matches = matches['city'].value_counts().head(10).reset_index()
            city_matches.columns = ['City', 'Matches']
            
            fig = px.pie(city_matches, values='Matches', names='City', hole=0.3)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# TRENDS & INSIGHTS PAGE
# ============================================

elif page == "📈 Trends & Insights":
    st.markdown('<p class="main-header">📈 Trends & Insights</p>', unsafe_allow_html=True)
    
    if matches is not None and deliveries is not None:
        # Total runs per season (Fixed: now deliveries has season column from merge)
        st.subheader("🏏 Total Runs Scored Per Season")
        runs_per_season = deliveries.groupby('season')['total_runs'].sum().reset_index()
        runs_per_season.columns = ['Season', 'Total Runs']
        
        fig = px.area(runs_per_season, x='Season', y='Total Runs',
                     labels={'Season': 'Season', 'Total Runs': 'Total Runs Scored'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Result Type Distribution")
            result_type = matches['result'].value_counts().reset_index()
            result_type.columns = ['Result Type', 'Count']
            
            fig = px.pie(result_type, values='Count', names='Result Type', hole=0.3)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Dismissal Types")
            dismissal_types = deliveries['dismissal_kind'].value_counts().head(8).reset_index()
            dismissal_types.columns = ['Dismissal Type', 'Count']
            
            fig = px.bar(dismissal_types, x='Count', y='Dismissal Type', orientation='h',
                        color='Count', color_continuous_scale='Reds')
            fig.update_layout(showlegend=False, height=350, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🏏 IPL Analytics Dashboard | Made with ❤️ by Jeevan</p>
        <p>Data Source: IPL 2008-2024 | Technology: Python, Streamlit, Plotly</p>
    </div>
""", unsafe_allow_html=True)