export AIRFLOW_HOME=~/rag_pipeline/airflow
echo 'export AIRFLOW_HOME=~/rag_pipeline/airflow' >> ~/.bashrc
source ~/.bashrc
airflow db migrate

if [ -f ~/rag_pipeline/.env ]; then
    # Automatically export all variables defined from this point forward
    set -o allexport
    source ~/rag_pipeline/.env
    # Turn off automatic exporting
    set +o allexport
else
    echo ".env file not found"
    exit 1
fi

export DATABRICKS_HOST="$DATABRICKS_HOST"
export DATABRICKS_HTTP_PATH="$DATABRICKS_HTTP_PATH"
export DATABRICKS_TOKEN="$DATABRICKS_TOKEN"

airflow connections add 'databricks_default' \
    --conn-type 'databricks' \
    --conn-host "$DATABRICKS_HOST" \
    --conn-password "$DATABRICKS_TOKEN"

airflow standalone