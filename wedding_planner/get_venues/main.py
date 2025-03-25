from google.cloud import bigquery
import functions_framework
import pandas as pd

@functions_framework.http
def get_venues(request):
    client = bigquery.Client()
    query = """
        SELECT DISTINCT vs AS venue_style, location, guest_capacity
        FROM `nirmal-maven.llm_app.wedding_venues`,
        UNNEST(venue_style) AS vs
    """
    results = client.query(query).to_dataframe()
    # Convert to plain Python lists and remove duplicates
    venue_styles = sorted(set(str(x) for x in results["venue_style"] if pd.notna(x)))
    locations = sorted(set(str(x) for x in results["location"] if pd.notna(x)))
    capacities = sorted(set(str(x) for x in results["guest_capacity"] if pd.notna(x)))
    
    return {
        "venue_styles": venue_styles,
        "locations": locations,
        "capacities": capacities
    }