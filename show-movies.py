from flask import Flask
from flask import render_template

import random
import numpy as np
import pandas as pd

import config

def get_movies(id=-1):

    """
    Get a list of movies

    Parameters:
    - id (int): The movie id for which to retrieve recommendations. Default is 0 for a random selection

    Returns:
    Tuple:
    - If id == 0:
        - list: A list of lists representing a random selection of movies
        - str: An empty string (no specific movie name)
    - Else:
        - list: A list of lists representing recommended movies
        - str: The name of the movie with the specified id
    """

    # Load movies into new dataframe
    df = pd.read_csv(config.MOVIES_PATH)

    # Add integer index column with asecending values from zero 
    df = df.reset_index(drop=False)

    if id == -1:
    
        # Return list of random selection of movies
        return (random.sample(df.values.tolist(), 30), "no movie selected")

    else:

        # Load similarities into a new dataframe 
        similarities = pd.read_csv(config.SIMILARITIES_PATH)

        # Extract a string of similarity values for row id
        similarities_for_id = similarities.loc[id, "similarities"]

        # Split the string into list of strings
        similarity_values_as_strings = similarities_for_id.split()

        # Convert into list of integers
        similarity_values_as_integers = list(map(int, similarity_values_as_strings))

        # Get movies from rows that match list of integers
        selected_rows_from_df = df.loc[similarity_values_as_integers]

        # Convert df to list
        result_list_of_lists = selected_rows_from_df.values.tolist()

        # Return list of similar movies
        return (result_list_of_lists, df.loc[id][1])

app = Flask(__name__)

@app.route("/")
def home():
    # Show random selection of movies
    movies, _ = get_movies()
    return render_template("movies.html", movies=movies, h2="Choose a movie to get recommendations")

@app.route('/movie/<int:id>')
def get_movie_recommendations(id):
    # Show similar movies
    movies, movie_name = get_movies(id)
    return render_template("movies.html", movies=movies, h2=f"If you liked '{movie_name}', you might like these")

if __name__ == "__main__":
    app.run()