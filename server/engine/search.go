package engine

import (
	"bytes"
	"encoding/json"
	"fmt"

	"github.com/gin-gonic/gin"
)

type SearchRequest struct {
	Text  string `json:"text"`
	Image string `json:"image"`
}

type SearchResponse struct {
	Items []string `json:"items"`
}

func Search(c *gin.Context, req SearchRequest) (*SearchResponse, error) {
	es := New()

	var buf bytes.Buffer

	query := map[string]interface{}{
		"knn": map[string]interface{}{
			"field":          "vector",
			"k":              10,
			"num_candidates": 100,
			"query_vector":   []float32{},
		},
		"_source": []string{"id", "link"},
	}

	if err := json.NewEncoder(&buf).Encode(query); err != nil {
		return nil, fmt.Errorf("failed to encode query: %w", err)
	}

	res, err := es.Search(
		es.Search.WithContext(c),
		es.Search.WithIndex("clip"),
		es.Search.WithBody(&buf),
		es.Search.WithTrackTotalHits(true),
		es.Search.WithPretty(),
	)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	if res.IsError() {
		var e map[string]interface{}

		_ = json.NewDecoder(res.Body).Decode(&e)
		return nil, fmt.Errorf("ES error during search: %v", e)
	}

	var r struct {
		Hits struct {
			Hits []struct {
				Link string `json:"link"`
			} `json:"hits"`
		} `json:"hits"`
	}
	if err := json.NewDecoder(res.Body).Decode(&r); err != nil {
		return nil, fmt.Errorf("failed to decode body response from ES: %w", err)
	}

	items := []string{}
	for _, hit := range r.Hits.Hits {
		items = append(items, hit.Link)
	}

	return &SearchResponse{Items: items}, nil
}
