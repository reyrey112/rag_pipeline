from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
for job in w.jobs.list():
    print(job.job_id, job.settings.name)