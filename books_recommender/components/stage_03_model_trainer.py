import os
import pickle
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from books_recommender.config.configuration import AppConfiguration


class ModelTrainer:
    def __init__(self, app_config=AppConfiguration()):
        self.model_trainer_config = app_config.get_model_trainer_config()

    def train(self):
        # Loading pivot data
        book_pivot = pickle.load(open(self.model_trainer_config.transformed_data_file_dir, 'rb'))
        book_sparse = csr_matrix(book_pivot)

        # Training model
        model = NearestNeighbors(algorithm='brute')
        model.fit(book_sparse)

        # Saving model object for recommendations
        os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
        file_name = os.path.join(
            self.model_trainer_config.trained_model_dir, 
            self.model_trainer_config.trained_model_name
        )
        pickle.dump(model, open(file_name, 'wb'))

        return file_name  # returning path to the saved model

    def initiate_model_trainer(self):
        self.train()
