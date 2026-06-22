import streamlit as st
import pandas as pd

st.set_page_config(page_title="Netflix Smart Discovery", page_icon="🍿", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_titles.csv")

    df["country"] = df["country"].fillna("Unknown")
    df["director"] = df["director"].fillna("Unknown")
    df["cast"] = df["cast"].fillna("Unknown")
    df["rating"] = df["rating"].fillna("Unknown")
    df["duration"] = df["duration"].fillna("Unknown")

    bad_rating = df["rating"].astype(str).str.contains("min", na=False)
    df.loc[bad_rating, "duration"] = df.loc[bad_rating, "rating"]
    df.loc[bad_rating, "rating"] = "Unknown"

    return df

netflix = load_data()

st.title("🍿 Netflix Smart Discovery")
st.write("Find Netflix recommendations based on your preferences.")

tab1, tab2 = st.tabs(["🎬 Recommendations", "📊 Analytics"])

with tab1:
    st.header("Find Something to Watch")

    all_genres = sorted(
        set(
            genre.strip()
            for genres in netflix["listed_in"].dropna()
            for genre in genres.split(",")
        )
    )

    genre = st.selectbox("Choose a genre", all_genres)
    content_type = st.selectbox("Choose type", ["Any", "Movie", "TV Show"])

    countries = sorted(netflix["country"].dropna().unique())
    country = st.selectbox("Choose country", ["Any"] + countries)

    num_recs = st.slider("Number of recommendations", 1, 10, 5)

    if st.button("Recommend"):
        matches = netflix[
            netflix["listed_in"].str.contains(genre, case=False, na=False)
        ]

        if content_type != "Any":
            matches = matches[matches["type"] == content_type]

        if country != "Any":
            matches = matches[
                matches["country"].str.contains(country, case=False, na=False)
            ]

        if len(matches) == 0:
            st.warning("No matches found. Try different filters.")
        else:
            results = matches.sample(min(num_recs, len(matches)))

            for _, row in results.iterrows():
                st.subheader(row["title"])
                st.write(f"**Type:** {row['type']}")
                st.write(f"**Country:** {row['country']}")
                st.write(f"**Rating:** {row['rating']}")
                st.write(f"**Release Year:** {row['release_year']}")
                st.write(f"**Duration:** {row['duration']}")
                st.write(f"**Genres:** {row['listed_in']}")
                st.write(f"**Description:** {row['description']}")
                st.divider()

with tab2:
    st.header("Netflix Content Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Titles", len(netflix))
    col2.metric("Movies", len(netflix[netflix["type"] == "Movie"]))
    col3.metric("TV Shows", len(netflix[netflix["type"] == "TV Show"]))

    st.subheader("Movies vs TV Shows")
    st.bar_chart(netflix["type"].value_counts())

    st.subheader("Top 10 Ratings")
    st.bar_chart(netflix["rating"].value_counts().head(10))

    st.subheader("Top 10 Countries")
    st.bar_chart(netflix["country"].value_counts().head(10))

    st.subheader("Top 10 Genres")
    genre_data = netflix.copy()
    genre_data["listed_in"] = genre_data["listed_in"].str.split(", ")
    genre_data = genre_data.explode("listed_in")
    st.bar_chart(genre_data["listed_in"].value_counts().head(10))

    st.markdown("---")
st.markdown(
    "Built with Python, Pandas, Streamlit, and Netflix Dataset"
)