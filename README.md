# AI-Powered Course Recommendation System

This project is a content-based course recommendation system that suggests courses to users based on their interests. The recommendation engine is built using TF-IDF and cosine similarity. The project is served via a Flask API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.10 or higher
*   pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the Flask API server, run the following command from the root directory of the project:

```bash
python src/app.py
```

The server will start on `http://127.0.0.1:5000`.

You can get course recommendations by sending a GET request to the `/recommend` endpoint with a `title` query parameter.

**Example using cURL:**

```bash
curl "http://127.0.0.1:5000/recommend?title=Intro to Python"
```

**Example Response:**

```json
{
  "recommendations": [
    "Data Science with Python",
    "AI Projects Made Easy",
    "Machine Learning",
    "Data Engineering with Python",
    "The Data Science Course 2021"
  ]
}
```

## Running the Tests

To run the unit tests, execute the following command from the root directory:

```bash
python -m unittest tests/test_app.py
```

This will run all the tests in the `tests/test_app.py` file and report the results.

## Google Colab

This project can also be run in a Google Colab notebook.

1.  **Open the notebook in Google Colab:**
    *   Navigate to [Google Colab](https://colab.research.google.com/).
    *   Click on `File > Open notebook`.
    *   Select the `GitHub` tab.
    *   Enter the URL of this repository and select the `notebooks/google_colab_recommendation_system.ipynb` file.

2.  **Run the notebook:**
    *   Once the notebook is open, you can run each cell sequentially by pressing `Shift + Enter`.
    *   The notebook will install the necessary dependencies, load the data, build the recommendation model, and provide examples of how to get course recommendations.
