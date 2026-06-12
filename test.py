from dotenv import load_dotenv
from databricks_notebooks.abstracts_to_chunks import create_chunks
import os
load_dotenv()
abstract_table = f"{os.environ.get("DATABRICKS_CATALOG")}.bronze.abstracts"
chunks_table = f"{os.environ.get("DATABRICKS_CATALOG")}.silver.chunks"
create_chunks(abstract_table, chunks_table)