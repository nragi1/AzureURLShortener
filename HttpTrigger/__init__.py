import logging
import azure.functions as func
import json
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os

endpoint = os.environ['COSMOS_ENDPOINT']
credential = os.environ['COSMOS_KEY']
client = CosmosClient(endpoint, credential=credential)
database_name = 'url-shortener'
database = client.get_database_client(database_name)
container_name = 'urls'
container = database.get_container_client(container_name)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    url = req_body.get('url')
    short_code = req_body.get('short_code').lower()
    description = req_body.get('description', "")

    try:
        data = {
            "id": short_code,
            "received_url": url,
            "received_short_code": short_code,
            "received_description": description
        }
        container.upsert_item(data)
    except exceptions.CosmosHttpResponseError as e:
        logging.error(e, exc_info=True)
        return func.HttpResponse(f"Error creating short URL: {str(e)}", status_code=500)
    
    base_url = "http://localhost:7071/api"
    short_url = f"{base_url}/{short_code}"
    response_data = {"short_url": short_url}
    
    return func.HttpResponse(json.dumps(response_data), status_code=200, headers={"Content-Type": "application/json"})