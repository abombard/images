#!/bin/bash

usage() {
	cat <<EOF
usage: $0 -i [elastic index] [ARGUMENT]
-h                          help
-v                          verbose
-m <model> [mpnet|clip]     model to use (its the name of the es index aswell)
-c                          create index named after model (-m argument)
-d                          delete index named after model (-m argument)
-s                          execute the model and generate files in ./tmp/
-f                          push all the files in tmp/ to ES
-e <json text>              index document
EOF
}

INDEXNAME="text"

create_index() {
  if [[ $INDEXNAME == mpnet ]]; then
   curl -H 'Content-Type: application/json' -X PUT http://localhost:9200/$INDEXNAME -d '{
    "mappings": {
      "properties": {
        "vector": {
          "type": "dense_vector",
          "dims": 768,
          "index": true,
          "similarity": "cosine"
        },
        "link": {
          "type": "text"
        },
        "headline": {
          "type": "text"
        },
        "category": {
          "type": "text"
        },
        "short_description": {
          "type": "text"
        },
        "authors": {
          "type": "text"
        },
        "date": {
          "type":"date",
          "format":"YYYY-MM-DD"
        }
      }
    }
  }
}'
  elif [[ $INDEXNAME == clip ]]; then
   curl -H 'Content-Type: application/json' -X PUT http://localhost:9200/$INDEXNAME -d '{
    "mappings": {
      "properties": {
        "vector": {
          "type": "dense_vector",
          "dims": 256,
          "index": true,
          "similarity": "cosine"
        },
        "link": {
          "type": "text"
        }
      }
    }
  }
}'
  fi
}

delete_index() {
   curl -H 'Content-Type: application/json' -X DELETE http://localhost:9200/$INDEXNAME
}

push_document() {
  curl -H 'Content-Type: application/json' -X POST http://localhost:9200/$INDEXNAME/_doc/"$1" -d"$2"
}

execute_model() {
  mkdir -p tmp
  if [[ $INDEXNAME == mpnet ]]; then
    mkdir -p tmp/mpnet
    python execute_mpnet.py -f $1
  elif [[ $INDEXNAME == clip ]]; then
    mkdir -p tmp/clip
    echo >&2 "execute the following:"
    echo >&2 "  python execute_clip.py natural_images/fruit/*"
  fi
}

push_document_json() {
  D="./tmp"

  typeset -i X=0
  for F in $D/*; do
    (( X += 10 ))
    jq -c '.[]' $F | while read LINE; do
      (( X++ ))
      curl -X PUT "http://localhost:9200/$INDEXNAME/_doc/$X" -H 'Content-Type: application/json' -d "${LINE}"
    done
  done
}

while getopts "hm:cde:fs:" arg; do
  case $arg in
	h)
	  usage
	  exit 0
	  ;;
  m)
    INDEXNAME=$OPTARG
    ;;
	c)
    create_index
    ;;
  d)
    delete_index
	  ;;
  s)
    execute_model $OPTARG
    ;;
  e)
    push_document $OPTARG
    ;;
  f) 
    push_document_json
  esac
done
