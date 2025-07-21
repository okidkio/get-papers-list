# 🧬 **PubMed Pharma Paper Extractor**

A Python CLI tool that fetches research papers from PubMed based on a user query, identifies papers with at least one non-academic author affiliated with a pharmaceutical or biotech company, and saves the filtered results into a CSV file.

✅ Built for Aganitha's Python Take Home Exercise – 2025

---

## 📌 **Features**

- 🔍 Uses the [NCBI E-utilities API (PubMed)](https://www.ncbi.nlm.nih.gov/books/NBK25501/) to fetch relevant research papers.
- 🧪 Filters papers to identify at least one **non-academic author** affiliated with a **pharmaceutical or biotech company**.
- 📥 Saves filtered results into a clean `.csv` file.
- 🧪 Includes basic test case using `pytest`.
- 📦 Organized with Poetry for clean dependency and project management.

---

## 🗂️ **Project Structure**

get-papers-list/

├── src/get_papers/

│   ├── main.py        # CLI entry

│   └── pubmed.py      # Fetch + filter logic

├── tests/

│   └── test_main.py   # Test case

├── requirements.txt

├── pyproject.toml

└── README.md


---

## 🚀 **How to Set Up & Run the Project**

⚠️ **Prerequisite:** Python 3.9+ and Poetry installed

1. Clone the Repository
   
"git clone https://github.com/okidkio/get-papers-list.git
cd get-papers-list"

3. Set Up Environment Using Poetry (Recommended)

"poetry install"

5. Run the CLI Tool

"poetry run get-papers-list --query "covid vaccine" --output results.csv --max_results 15"

Optional: Run with Virtual Environment

If you prefer not to use Poetry:

"python -m venv venv

source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt

python src/get_papers/main.py --query "covid vaccine" --output results.csv --max_results 15"

⚙️ **Command-Line Options**

| Option         | Description                                       |
|----------------|---------------------------------------------------|
| `--query`      | Search query for PubMed (e.g., `"lung cancer"`)   |
| `--output`     | Path to save the filtered results as a CSV file   |
| `--max_results`| *(Optional)* Limit the number of papers to retrieve |


🔧 **Tools & Libraries Used**

-Python 3.9+

-Poetry – for dependency and project management

-Requests – API integration

-Pandas – CSV handling

-TQDM – Progress display

-Pytest – Unit testing

-OpenAI GPT – for identifying author affiliations (if integrated)

🧪 **Run Tests**

poetry run pytest

👤 Author

Shiwani Wasnik

https://github.com/okidkio

Email: wasnikshiwani6@gmail.com
