package main

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

/*
 */
func TestMain(t *testing.T) {
	// Show buttons to add new joke, edit a joke, or delete a joke
	// t.Fatal("not implemented")
}

func TestCreateCheck(t *testing.T) {
	request, err := http.NewRequest("GET", "/check", nil)
	assert.Equal(t, nil, err, "nil Error on getting request is expected")
	response := httptest.NewRecorder()
	Router().ServeHTTP(response, request)

	assert.Equal(t, 200, response.Code, "OK response is expected")
}
