import requests
import pandas as pd
import json

def setHost():
    SOLR_HOST = "localhost"
    SOLR_PORT = "8983"

    solr_url = f'http://{SOLR_HOST}:{SOLR_PORT}/solr/'
    solr_collections_api = f'{solr_url}admin/collections'

    return solr_url, solr_collections_api

def create_collection(collection_name):

    #Wipe previous collection
    wipe_collection_params = [
      ('action', "delete"),
      ('name', collection_name)
    ]

    print(f"Wiping '{collection_name}' collection")
    response = requests.post(solr_collections_api, data=wipe_collection_params).json()

  #Create collection
    create_collection_params = [
      ('action', "CREATE"),
      ('name', collection_name),
      ('numShards', 1),
      ('replicationFactor', 1) ]

    print(create_collection_params)

    print(f"Creating '{collection_name}' collection")
    response = requests.post(solr_collections_api, data=create_collection_params).json()
    print(response)

def addData(solr_url, collection):
    #load data from csvimport pysolr
    fName = "../tc/complaints.csv"
    data = pd.read_csv(fName)
    # take a subset of 225K complaints. Anything more than this fails due to solr/memory limitation.
    data = data.iloc[0:225000]
    data.to_json("data.json", orient='records', lines=True)
    complaints_json = []
    for line in open('data.json', 'r'):
        complaints_json.append(json.loads(line))
    print(f"\nAdding Documents to '{collection}' collection")
    response = requests.post(f"{solr_url}{collection}/update?commit=true", json=complaints_json).json()
    print("Status: " "Success" if response["responseHeader"]["status"] == 0 else "Failure")

if __name__ == "__main__":
    collectionName = "complaints"
    solr_url, solr_collections_api = setHost()
    #create collection
    create_collection(collectionName)
    #add data to collection
    addData(solr_url, collectionName)




