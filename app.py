import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


# database utility functions

def run_query(query,conn):
    return pd.read_sql(query,conn)

# SQL Queries

QUERIES = {
    "avg_rating_by_genre": """
        SELECT g.name AS genre,
               ROUND(AVG(bs.rating), 2) AS avg_rating
        FROM genres g
        JOIN books b ON g.id = b.genre_id
        JOIN book_stats bs ON b.id = bs.book_id
        GROUP BY g.name
        ORDER BY avg_rating DESC;
    """,

    "top_rated_books_by_year": """
    SELECT b.publication_year,
           b.title,
           bs.rating AS top_rating
    FROM books b
    JOIN book_stats bs ON b.id = bs.book_id
    WHERE bs.rating = (
        SELECT MAX(bs2.rating)
        FROM book_stats bs2
        JOIN books b2 ON b2.id = bs2.book_id
        WHERE b2.publication_year = b.publication_year
    )
    ORDER BY b.publication_year;
""",

    "revenue_vs_votes": """
        SELECT b.title,
               bs.votes,
               bs.revenue_millions
        FROM books b
        JOIN book_stats bs ON b.id = bs.book_id;
    """,

    "book_count_by_genre_year": """
        SELECT b.publication_year,
               g.name AS genre,
               COUNT(*) AS book_count
        FROM books b
        JOIN genres g ON g.id = b.genre_id
        GROUP BY b.publication_year, g.name
        ORDER BY b.publication_year, g.name;
    """
}

# Streamlit app

st.set_page_config(page_title="Book Analytics Dashboard",layout="wide")

st.title("📊 Book Analytics Dashboard")
st.markdown("This dashboard is a part of my Data Science Internship **Task 5 : End-to-End Data Pipeline for Book Analytics** at SkilledScore.com")

# connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
# Total Books
total_books = cursor.execute("SELECT COUNT(*) FROM books").fetchone()[0]

# Average Rating
avg_rating = cursor.execute("SELECT AVG(rating) FROM book_stats").fetchone()[0]

# Total Votes
total_votes = cursor.execute("SELECT SUM(votes) FROM book_stats").fetchone()[0]

# Total Revenue
total_revenue = cursor.execute("SELECT SUM(revenue_millions) FROM book_stats").fetchone()[0]
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Books", f"{total_books:,}")

with col2:
    st.metric("Average Rating", f"{avg_rating:.2f}")

with col3:
    st.metric("Total Votes", f"{total_votes:,}")

with col4:
    st.metric("Total Revenue (M)", f"${total_revenue:,.2f}")
# sidebar filters 
st.sidebar.header("Filters")
selected_genre = st.sidebar.multiselect(
    "Select Genre (for some plots )",
    [row[0] for row in conn.execute("SELECT name from genres").fetchall()]
)

selected_year = st.sidebar.slider("Select Publication Year",1950,2023,(2000,2023))

# 1.Average Rating per Genre 

st.subheader("⭐Average Book Rating by Genre")
df_avg_rating = run_query(QUERIES["avg_rating_by_genre"],conn)

if selected_genre:
    df_avg_rating = df_avg_rating[df_avg_rating['genre'].isin(selected_genre)]

fig1 = px.bar(df_avg_rating, x='genre',y='avg_rating',
              labels={"avg_rating":"Average Rating",
                      "genre":"Genre"},
              color = "avg_rating",color_continuous_scale="viridis"
)
st.plotly_chart(fig1,use_container_width=True)

# -------------------------
# 2. Top-Rated Books by Year
# -------------------------
st.subheader("🏆 Top-Rated Books by Year")
df_top_books = run_query(QUERIES["top_rated_books_by_year"], conn)
df_top_books = df_top_books[(df_top_books["publication_year"] >= selected_year[0]) &
                            (df_top_books["publication_year"] <= selected_year[1])]

fig2 = px.scatter(df_top_books, x="publication_year", y="top_rating",
                  text="title", size="top_rating",
                  title="Top-Rated Books by Year",
                  labels={"publication_year": "Year", "top_rating": "Rating"})
fig2.update_traces(textposition="top center")
st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# 3. Revenue vs Votes
# -------------------------
st.subheader("💰 Revenue vs. Votes")
df_revenue_votes = run_query(QUERIES["revenue_vs_votes"], conn)

fig3 = px.scatter(df_revenue_votes, x="votes", y="revenue_millions",
                  hover_data=["title"],
                  title="Revenue vs Votes",
                  labels={"votes": "Votes", "revenue_millions": "Revenue (Millions)"},
                  size="revenue_millions", opacity=0.7)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# 4. Book Count by Genre Over the Years
# -------------------------
st.subheader("📈 Book Count by Genre Over the Years")
df_book_count = run_query(QUERIES["book_count_by_genre_year"], conn)
df_book_count = df_book_count[(df_book_count["publication_year"] >= selected_year[0]) &
                              (df_book_count["publication_year"] <= selected_year[1])]

fig4 = px.line(df_book_count, x="publication_year", y="book_count",
               color="genre",
               title="Book Count by Genre Over Time",
               labels={"publication_year": "Year", "book_count": "Number of Books"})
st.plotly_chart(fig4, use_container_width=True)

# Close DB Connection
conn.close()

