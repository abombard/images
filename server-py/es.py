import requests

def create_index(model, dims):
    body = {
      "mappings": {
        "properties": {
          "vector": {
            "type": "dense_vector",
            "dims": dims,
            "index": True,
            "similarity": "cosine"
          },
          "link": {
            "type": "text"
          }
        }
      }
    }

    res = requests.put(f'http://localhost:9200/{model}', json=body)
    print(res.json())

def delete_index(model):
    res = requests.delete(f'http://localhost:9200/{model}')
    print(res.json())

def search_knn(model, emb, max_results=10):
    body = {
        'knn': {
            'field': 'vector',
            'k': max_results,
            'num_candidates': 500,
            'query_vector': emb,
        },
        '_source': ['id', 'link'],
    }

    res = requests.post(f'http://localhost:9200/{model}/_knn_search', json=body)

    resp = res.json()

    items = []
    for hit in resp['hits']['hits']:
        items.append(hit['_source']['link'])

    return items

