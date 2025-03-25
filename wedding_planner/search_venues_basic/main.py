from google.cloud import bigquery
import functions_framework

@functions_framework.http
def search_venues_basic(request):
    # Get user inputs from the request (sent by Bubble)
    request_json = request.get_json(silent=True)
    if not request_json:
        return {"error": "No input provided"}, 400

    venue_style = request_json.get("venue_style")
    location = request_json.get("location")
    guest_capacity = request_json.get("guest_capacity")

    # Build BigQuery client
    client = bigquery.Client()

    # Query BigQuery for exact matches, handling REPEATED venue_style
    query = """
        SELECT venue_name, location, guest_capacity, about
        FROM `nirmal-maven.llm_app.wedding_venues`,
        UNNEST(venue_style) AS vs
        WHERE (@venue_style IS NULL OR vs = @venue_style)
        AND (@location IS NULL OR location = @location)
        AND (@guest_capacity IS NULL OR guest_capacity = @guest_capacity)
    """

    # Define query parameters
    query_params = []
    if venue_style:
        query_params.append(bigquery.ScalarQueryParameter("venue_style", "STRING", venue_style))
    if location:
        query_params.append(bigquery.ScalarQueryParameter("location", "STRING", location))
    if guest_capacity:
        query_params.append(bigquery.ScalarQueryParameter("guest_capacity", "STRING", guest_capacity))

    # Run query
    job_config = bigquery.QueryJobConfig(query_parameters=query_params)
    results = client.query(query, job_config=job_config).to_dataframe()

    # Convert results to a list of dictionaries
    venues = results.to_dict(orient="records")
    return {"venues": venues}
