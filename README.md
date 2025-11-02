# 🏏 IPL Analytics Dashboard

An interactive and visually rich **Streamlit web application** that provides detailed insights and analysis of the **Indian Premier League (IPL)** from **2008 to 2024**.  
Built with **Python, Streamlit, and Plotly**, this dashboard allows users to explore team performances, player stats, venue trends, and much more — all in one place.

---

## 📚 Features

### 🏠 Home Page
- Overview of IPL with key statistics: total matches, teams, venues, and seasons.
- Year-wise matches visualization.
- Top 5 winning teams.
- Toss impact on match outcomes.

### 📊 Team Analysis
- Team-wise performance overview (wins, losses, win rate).
- Season-wise win trends.
- Top venues for each team.

### ⭐ Player Stats
- Top run scorers and wicket takers in IPL history.
- Player of the Match award leaderboard.
- Interactive sliders to control the number of players displayed.

### 🏟️ Venue Analysis
- Top venues by number of matches.
- City-wise match distribution pie chart.

### 📈 Trends & Insights
- Total runs scored per season.
- Distribution of match result types.
- Most common dismissal types.

---

## ⚙️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Frontend** | Streamlit |
| **Data Visualization** | Plotly Express, Plotly Graph Objects |
| **Backend / Logic** | Python (Pandas, NumPy) |
| **Data Source** | IPL datasets (matches.csv, deliveries.csv) |
| **Images / UI** | Custom CSS + Streamlit UI |

---

## 📂 Project Structure

├── app.py # Main Streamlit application
├── matches.csv # IPL match-level dataset
├── deliveries.csv # Ball-by-ball delivery dataset
├── ipl_analysis.ipynb # Jupyter notebook for EDA and preprocessing
└── README.md # Project documentation

yaml
Copy code

---

## 🚀 How to Run the App Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/ipl-analytics-dashboard.git
cd ipl-analytics-dashboard
2️⃣ Install Dependencies
Make sure you have Python 3.9+ installed, then run:

bash
Copy code
pip install -r requirements.txt
Example requirements.txt:

nginx
Copy code
streamlit
pandas
numpy
plotly
pillow
3️⃣ Run the App
bash
Copy code
streamlit run app.py
4️⃣ Open in Browser
Once the app starts, open the provided local URL (e.g., http://localhost:8501) in your browser.

🧠 Insights Highlight
Teams with the highest win rates across seasons.

Evolution of batting trends (runs per season).

Venue dominance — which cities host most matches.

Top-performing players across the IPL timeline.

✨ UI Features
Modern gradient headers and minimalistic design.

Responsive layout with wide-screen optimization.

Smooth interactive charts (bar, pie, line, and area).

Lightweight custom CSS styling for better readability.

🧑‍💻 Author
Jeevan Kumar Panda
📧 jeevanpanda1234@gmail.com
🌐 jeevankportfolio.netlify.app
💼 GitHub Profile

🏁 License
This project is open-source and available under the MIT License.
