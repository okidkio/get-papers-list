# 🧬 PubMed Pharma Paper Extractor

A Python CLI tool that fetches research papers from PubMed based on a user query, identifies papers with **at least one non-academic author affiliated with a pharmaceutical or biotech company**, and saves the filtered results in a CSV file.

> ✅ **Built for Aganitha's Python Take Home Exercise – 2025**

---

## 📌 Features

- 🔍 Uses the **NCBI E-utilities API** (PubMed) to fetch papers.
- 🧪 Filters papers where at least one author is **non-academic** and affiliated with **pharma/biotech** companies.
- 📥 Saves the final results into a clean `.csv` file.
- 🧪 Comes with a basic **test case** using `pytest`.
- 📦 Project organized using **Poetry** structure for maintainability.

---

## 🗂️ Folder Structure

get-papers-list/
├── src/
│ └── get_papers/
│ ├── init.py
│ ├── main.py ← CLI entry point
│ └── pubmed.py ← Core logic to fetch and filter papers
├── tests/
│ └── test_main.py ← Test for functionality
├── requirements.txt ← Python dependencies
├── README.md ← Project documentation


---

## 🚀 How to Set Up & Run the Project (Step-by-Step)

> ⚠️ Prerequisites: Python 3.9+ installed on your system

### 1. 🧱 Clone the Repository

```bash
git clone https://github.com/your-username/get-papers-list.git
cd get-papers-list

# Create a virtual environment
python -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

