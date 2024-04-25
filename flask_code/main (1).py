import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

authors_df = 'dummy_author_data.csv'
papers_df = 'dummy_paper_data.csv'
orgs_df = 'dummy_org_data.csv'

global_paper_data = pd.read_csv(papers_df)
global_author_data = pd.read_csv(authors_df)
global_org_data = pd.read_csv(orgs_df)

@app.route("/", methods=("GET", "POST"))
def index():
    # Default value
    search_type = 'author'  
    result_data = None

    if request.method == "POST":
        # This will be either 'author', 'paper', or 'org'
        search_type = request.form['searchType']  
        query = request.form.get("query")
        result_data = search(query, search_type)
    
    return render_template("index.html", result=result_data, searchType=search_type)


def search(query, search_type):
    if search_type == 'paper':
        result = global_paper_data.groupby('title').agg({
            'abstract': 'first', 
            'year': 'first',
            'author': ', '.join,
            'org': lambda x: list(x),
            'n_citation': 'first'
        }).reset_index()
        return result[["title", "abstract", "year", "author", "org", "n_citation"]]

    elif search_type == 'author':
        result = global_author_data[['author', 'org', 'n_citation', 'google_link']]
        return result

    elif search_type == 'org':
        result = global_org_data[['org', 'n_citation']]

        return result

if __name__ == '__main__':
    app.run()
