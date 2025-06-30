# Personal Finance Analyzer

This is a Flask-based web application project to record and visualize financial transactions.

## Features:
- Add new transactions (income/expenses).
- Delete existing transactions.
- Display a dashboard with financial data (requires running a Jupyter Notebook).
- Data storage in a CSV file.

## Technologies Used:
- Python
- Flask
- Pandas
- Panel (for the dashboard)
- Plotly (for the graphs)
- HTML/CSS
- Git & GitHub

## Setup and Local Execution:
1.  Clone the repository: `git clone https://github.com/your_username/your_repository.git`
2.  Navigate to the project folder: `cd your_repository`
3.  Create and activate a virtual environment:
    -   `python -m venv venv`
    -   Windows: `.\venv\Scripts\activate`
    -   macOS/Linux: `source venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt` (if you don't have this file, create one with `pip freeze > requirements.txt` after installing everything)
5.  Configure the Flask secret key (for security):
    -   Windows (persistent): Open "System Environment Variables" and add `FLASK_SECRET_KEY` with a long, random value.
    -   macOS/Linux (persistent): Add `export FLASK_SECRET_KEY='your_secret_key'` to your `.bashrc` or `.zshrc`.
6.  Run the Flask application: `python app.py`
7.  Open your browser at `http://127.0.0.1:5000/`

## Acknowledgements / Credits & License

This project is based on the original work by [Thu Vu](https://github.com/thu-vu92/local-llms-analyse-finance) and is licensed under the MIT License.

Substantial modifications have been made to adapt and extend the original project to new use cases.


You can find the original tutorial here:
* https://www.youtube.com/watch?v=h_GTxRFYETY
* Thu Vu

---
**Author:** [Fernando Becerra Vázquez]