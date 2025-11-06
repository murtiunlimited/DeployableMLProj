import os
import ast
import pandas as pd
import pickle
from books_recommender.config.configuration import AppConfiguration


class DataValidation:
    def __init__(self, app_config=AppConfiguration()):
        self.data_validation_config = app_config.get_data_validation_config()

    def preprocess_data(self):
        ratings = pd.read_csv(
            self.data_validation_config.ratings_csv_file,
            sep=";",
            on_bad_lines="skip",
            encoding="latin-1"
        )

        books = pd.read_csv(
            self.data_validation_config.books_csv_file,
            sep=";",
            on_bad_lines="skip",
            encoding="latin-1"
        )

        # Keep only important columns for books
        books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]

        # Rename book columns
        books.rename(columns={
            "Book-Title": "title",
            "Book-Author": "author",
            "Year-Of-Publication": "year",
            "Publisher": "publisher",
            "Image-URL-L": "image_url"
        }, inplace=True)

        # Rename ratings columns
        ratings.rename(columns={
            "User-ID": "user_id",
            "Book-Rating": "rating"
        }, inplace=True)

        # Keep only users who rated more than 200 books
        active_users = ratings['user_id'].value_counts() > 200
        active_user_ids = active_users[active_users].index
        ratings = ratings[ratings['user_id'].isin(active_user_ids)]

        # Merge ratings with books
        ratings_with_books = ratings.merge(books, on='ISBN')
        number_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
        number_rating.rename(columns={'rating': 'num_of_rating'}, inplace=True)
        final_rating = ratings_with_books.merge(number_rating, on='title')

        # Keep books with at least 50 ratings
        final_rating = final_rating[final_rating['num_of_rating'] >= 50]

        # Drop duplicate user-book pairs
        final_rating.drop_duplicates(['user_id', 'title'], inplace=True)

        # Save cleaned data
        os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
        final_rating.to_csv(
            os.path.join(self.data_validation_config.clean_data_dir, 'clean_data.csv'),
            index=False
        )

        # Save serialized object
        os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
        pickle.dump(
            final_rating,
            open(os.path.join(self.data_validation_config.serialized_objects_dir, "final_rating.pkl"), 'wb')
        )

    def initiate_data_validation(self):
        self.preprocess_data()
