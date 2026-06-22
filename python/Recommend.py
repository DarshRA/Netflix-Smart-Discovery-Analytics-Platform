import pandas as pd

# Load dataset
netflix = pd.read_csv("data/netflix_titles.csv")

# Basic cleaning
netflix["country"] = netflix["country"].fillna("Unknown")
netflix["director"] = netflix["director"].fillna("Unknown")
netflix["cast"] = netflix["cast"].fillna("Unknown")

# Fix duration/rating issue
bad_rating = netflix["rating"].astype(str).str.contains("min", na=False)
netflix.loc[bad_rating, "duration"] = netflix.loc[bad_rating, "rating"]
netflix.loc[bad_rating, "rating"] = "Unknown"

print("="*50)
print("🍿 NETFLIX SMART DISCOVERY 🍿")
print("="*50)

genre = input("\nEnter a genre: ")

matches = netflix[
    netflix["listed_in"].str.contains(
        genre,
        case=False,
        na=False
    )
]

if len(matches) == 0:
    print("\nNo matches found.")
else:

    if len(matches) > 5:
        matches = matches.sample(5)

    print("\nYour Recommendations:\n")

    for _, row in matches.iterrows():

        print("="*50)
        print("🎬 Title:", row["title"])
        print("📺 Type:", row["type"])
        print("🌎 Country:", row["country"])
        print("🔞 Rating:", row["rating"])
        print("📅 Year:", row["release_year"])
        print("⏱ Duration:", row["duration"])
        print("🎭 Genres:", row["listed_in"])

print("\nEnjoy! 🍿")