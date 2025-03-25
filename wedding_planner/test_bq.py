from google.cloud import bigquery

client = bigquery.Client()
query = "SELECT venue_name, location FROM `nirmal-maven.llm_app.wedding_venues` LIMIT 5"
results = client.query(query).to_dataframe()
print(results)