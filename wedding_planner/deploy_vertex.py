from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="nirmal-maven", location="us-central1")

# Create an endpoint
endpoint = aiplatform.Endpoint.create(
    display_name="wedding-planner-embeddings",
    project="nirmal-maven",
    location="us-central1"
)

# Deploy the prebuilt textembedding-gecko model
model_name = "publishers/google/models/text-embedding-005"  # Prebuilt model path
deployed_model = aiplatform.Model(model_name)
endpoint.deploy(
    model=deployed_model,
    traffic_percentage=100,
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=1
)

print(f"Endpoint created and model deployed: {endpoint.resource_name}")