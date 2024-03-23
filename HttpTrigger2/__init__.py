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
    logging.info('Python HTTP trigger function processed a request.')
    short_code = req.route_params.get('short_code')
    logging.info(f"Short code from route: {short_code}")
    if not short_code:
        return func.HttpResponse("Please pass a short code on the URL", status_code=400)
    
    data_response = container.read_item(item=short_code, partition_key=short_code)
    original_url = data_response.get('received_url')
    
    if not original_url:
        return func.HttpResponse("Short URL not found", status_code=404)
    
    return func.HttpResponse(status_code=302, headers={"Location": original_url})
