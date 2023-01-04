package engine

import (
	"log"

	"github.com/elastic/go-elasticsearch/v8"
)

var ES *elasticsearch.Client

func New() *elasticsearch.Client {
	if ES == nil {
		es, err := elasticsearch.NewDefaultClient()
		if err != nil {
			log.Fatal(err)
		}

		ES = es
	}

	return ES
}
