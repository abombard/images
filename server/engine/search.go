package engine

type SearchRequest struct {
	Text  string `json:"text"`
	Image string `json:"image"`
}

type SearchResponse struct {
	Items []string `json:"items"`
}

func Search(req SearchRequest) (SearchResponse, error) {
	return SearchResponse{
		Items: []string{"banane", "coco", "ananas"},
	}, nil
}
