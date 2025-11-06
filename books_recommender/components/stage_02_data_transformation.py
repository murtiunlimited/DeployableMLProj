import os
import pickle
import pandas as pd
from books_recommender.config.configuration import AppConfiguration


class DataTransformation:
    def __init__(self, app_config=AppConfiguration()):
        self.data_transformation_config = app_config.get_data_transformation_config()
        self.data_validation_config = app_config.get_data_validation_config()

    def get_data_transformer(self):
        df = pd.read_csv(self.data_transformation_config.clean_data_file_path)

        # Create pivot table
        book_pivot = df.pivot_table(columns='user_id', index='title', values='rating')
        book_pivot.fillna(0, inplace=True)

        # Save pivot table
        os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
        with open(os.path.join(self.data_transformation_config.transformed_data_dir, "transformed_data.pkl"), 'wb') as f:
            pickle.dump(book_pivot, f)

        # Save book names
        book_names = book_pivot.index
        os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
        with open(os.path.join(self.data_validation_config.serialized_objects_dir, "book_names.pkl"), 'wb') as f:
            pickle.dump(book_names, f)

        # Save book pivot for web app
        os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
        with open(os.path.join(self.data_validation_config.serialized_objects_dir, "book_pivot.pkl"), 'wb') as f:
            pickle.dump(book_pivot, f)

    def initiate_data_transformation(self):
        self.get_data_transformer()
