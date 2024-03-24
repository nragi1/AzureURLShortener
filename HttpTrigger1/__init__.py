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
    logging.info('List function processed a request.')
    items = list(container.query_items(query='SELECT * FROM c', enable_cross_partition_query=True))
    base_url = "http://localhost:7071/api"
    urls_list = [
        {
            "Shortened URL": f"{base_url}/{item.get('id')}",
            "Long URL": item.get("received_url"),
            "Description": item.get("received_description", "No description found")
        }
        for item in items
        
    ]
    
    return func.HttpResponse(json.dumps(urls_list), status_code=200, headers={"Content-Type": "application/json"})
