

# 📊 Book Analytics Dashboard

An interactive **Streamlit dashboard** for analyzing book data, built as part of my **Data Science Internship (Task 5: End-to-End Data Pipeline for Book Analytics)** at [SkilledScore.com](https://skilledscore.com).

This project connects to a SQLite database and provides insights into book ratings, votes, revenue, and publication trends using **SQL queries, Pandas, and Plotly visualizations**.

---

## 🚀 Features

- **Summary Metrics**
  - Total number of books
  - Average rating
  - Total votes
  - Total revenue (in millions)

- **Interactive Visualizations**
  1. ⭐ **Average Rating by Genre**  
     Bar chart showing average ratings across genres.
  2. 🏆 **Top-Rated Books by Year**  
     Scatter plot highlighting the highest-rated book per year.
  3. 💰 **Revenue vs Votes**  
     Bubble chart comparing book revenue and votes.
  4. 📈 **Book Count by Genre Over Time**  
     Line chart showing how book counts evolve by genre across years.

- **Sidebar Filters**
  - Filter by **genre**
  - Select a **publication year range**

---

## 🛠️ Tech Stack

- **Frontend & Dashboard**: [Streamlit](https://streamlit.io/)  
- **Database**: SQLite  
- **Data Handling**: Pandas  
- **Visualizations**: Plotly Express  

---

## 📂 Project Structure

```
├── database.db          # SQLite database with books, genres, and stats
├── app.py               # Main Streamlit application
├── README.md            # Project documentation
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/book-analytics-dashboard.git
   cd book-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:
   ```
   streamlit
   pandas
   plotly
   sqlite3   # comes with Python standard library
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**  
   Navigate to `http://localhost:8501`

---

## 📊 Database Schema

The SQLite database (`database.db`) contains the following tables:

- **books**: `id`, `title`, `publication_year`, `genre_id`
- **genres**: `id`, `name`
- **book_stats**: `id`, `book_id`, `rating`, `votes`, `revenue_millions`

---

## 🎯 Learning Outcomes

- Building an **end-to-end data pipeline** for analytics
- Writing optimized **SQL queries** for insights
- Creating **interactive dashboards** with Streamlit
- Using **Plotly** for advanced visualizations
- Connecting **Python apps with databases**

---

## 📌 Future Improvements

- Add **user-uploaded datasets** for custom analysis  
- Implement **machine learning models** for rating prediction  
- Deploy on **cloud platforms** (e.g., Railway, Streamlit Cloud, Heroku)  

---

## 🙌 Acknowledgements

This project was developed as part of my **Data Science Internship at SkilledScore.com**.  
Special thanks to mentors and peers for guidance and feedback.

---
