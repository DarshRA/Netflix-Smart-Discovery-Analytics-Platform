import pandas as pd

netflix = pd.read_csv("data/netflix_titles.csv")

print(netflix.head())

print(netflix.shape)
print(netflix.columns)
print("\nMissing Values:")
print(netflix.isnull().sum())
netflix["director"] = netflix["director"].fillna("Unknown")
netflix["cast"] = netflix["cast"].fillna("Unknown")
netflix["country"] = netflix["country"].fillna("Unknown")

print("\nMissing Values:")
print(netflix.isnull().sum())

print("\nMovies vs TV Shows:")
print(netflix["type"].value_counts())

print("\nTop 10 Countries:")
print(netflix["country"].value_counts().head(5))
print("\nContent Ratings:")
print(netflix["rating"].value_counts())

# Fix rows where duration values accidentally appear in the rating column
bad_rating_rows = netflix["rating"].str.contains("min", na=False)

netflix.loc[bad_rating_rows, "duration"] = netflix.loc[bad_rating_rows, "rating"]
netflix.loc[bad_rating_rows, "rating"] = "Unknown"

print("\nBad rating rows fixed:")
print(bad_rating_rows.sum())

print("\nCleaned Content Ratings:")
print(netflix["rating"].value_counts()) 

print("\nSample Genres:")
print(netflix["listed_in"].head(10))

# Split genres into separate rows
genre_data = netflix.copy()

genre_data["listed_in"] = genre_data["listed_in"].str.split(", ")

genre_data = genre_data.explode("listed_in")

print("\nTop Individual Genres:")
print(genre_data["listed_in"].value_counts().head(15))
