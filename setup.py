from setuptools import setup, find_packages

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# ----------------- Project info -----------------
REPO_NAME = "BooksRecommender"
AUTHOR_USER_NAME = "Murtaza Hussain"
SRC_REPO = "books_recommender"
LIST_OF_REQUIREMENTS = []  # e.g., ["pandas", "scikit-learn", "numpy"]
# ------------------------------------------------

setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    author_email="murtazahussain@example.com",
    description="A local package for ML-based book recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/murtiunlimited/{REPO_NAME}",
    packages=find_packages(where="."),
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)
