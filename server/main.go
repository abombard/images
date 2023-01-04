package main

import (
	"net/http"

	"github.com/abombard/images/engine"
	"github.com/gin-gonic/gin"
)

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}

func main() {
	router := gin.Default()

	router.Use(CORSMiddleware())

	router.POST("/search", func(c *gin.Context) {
		var searchRequest engine.SearchRequest

		if err := c.BindJSON(&searchRequest); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"message": err.Error(),
			})

			return
		}

		response, err := engine.Search(c, searchRequest)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"message": err.Error(),
			})

			return
		}

		c.JSON(http.StatusOK, gin.H{
			"message":  "coucou",
			"response": response,
		})
	})

	router.Run()
}
