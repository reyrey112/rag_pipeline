from steps.pubmed_to_df import PubSearch
from dotenv import load_dotenv
from steps.df_to_delta_table import write_to_delta_table
import os
import argparse

load_dotenv()
ps = PubSearch()


def run_pipeline(
    query: str = "Lentivirus",
    max_results: int = 500,
    meta_table: str = f"{os.environ.get("DATABRICKS_CATALOG")}.bronze.pubmed_meta",
    abstract_table: str = f"{os.environ.get("DATABRICKS_CATALOG")}.bronze.abstracts",
):

    print(f"Searching Pubmed for: '{query}'")
    pmids = ps.search(query, max_results)
    print(f"Found {len(pmids)} articles")

    print("Fetching article details")
    articles = ps.fetch(pmids)

    print("Converting to Dataframe")
    df = ps.list_to_df(articles)

    print("Uploading to databricks")
    write_to_delta_table(df, meta_table, abstract_table)

    print("Pipeline Completed")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed articles and load into Databricks"
    )
    parser.add_argument("--query", default="Lentivirus", help="PubMed search query")
    parser.add_argument(
        "--max-results", type=int, default=500, help="Max number of articles to fetch"
    )
    parser.add_argument(
        "--meta_table",
        default=f"{os.environ.get("DATABRICKS_CATALOG")}.bronze.pubmed_meta",
        help="Target metadata table",
    )
    parser.add_argument(
        "--abstract_table",
        default=f"{os.environ.get("DATABRICKS_CATALOG")}.bronze.abstracts",
    )
    args = parser.parse_args()

    run_pipeline(
        query=args.query,
        max_results=args.max_results,
        meta_table=args.meta_table,
        abstract_table=args.abstract_table,
    )


if __name__ == "__main__":
    main()
