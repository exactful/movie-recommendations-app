import os
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import config

 # Create an empty dataframe df with three columns
df = pd.DataFrame(columns=["title", "image", "plot"]) 

# Load source data into df
for dirname, _, filenames in os.walk(config.SOURCE_DATA_PATH):
    for filename in filenames:
        if filename.endswith(".csv"):
            df_new = pd.read_csv(os.path.join(dirname, filename))
            df = pd.concat([df, df_new], ignore_index=True)        
            print(f"Loaded {filename}")

print("Loaded source data in df")

# Truncate the plots to first 100 words; adjust to improve consine similarity effectiveness
df["plot"] = df["plot"].apply(lambda x: " ".join(x.split()[:100]))
print("Truncated plots")

# Create a TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words="english")
print("Created TF-IDF vectorizer")

# Fit and transform the plot column to TF-IDF vectors
tfidf_matrix = tfidf.fit_transform(df["title"] + " " + df["plot"])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print("Created cosine similarity matrix")

# Create an empty dataframe with an index based on the length of cosine_sim
similarities = pd.DataFrame(index=range(len(cosine_sim)))

# Calculate and store the top 30 most similar movie indices for each row in the similarities df
# ::-1 reverses the list, :30 returns first 30 items
similarities["similarities"] = similarities.index.map(lambda row_index: np.argsort(cosine_sim[row_index])[::-1][:30])

# Convert the arrays to strings
similarities["similarities"] = similarities["similarities"].apply(lambda x: " ".join(map(str, x)))

# Save to CSV
df.to_csv(config.MOVIES_PATH, index=False)
similarities.to_csv(config.SIMILARITIES_PATH, index=False)
print("Saved data files for website")