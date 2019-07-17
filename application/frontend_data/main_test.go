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

func TestTestJoke(t *testing.T) {
	emptyJoke := ""
	emptyJokeExpected := false
	assert.Equal(t, emptyJokeExpected, testJoke(emptyJoke), "Empty jokes are NOT detected")
	onlyescapedJoke := "\r\r\n\f\n\r\f"
	onlyescapedJokeExpected := false
	assert.Equal(t, onlyescapedJokeExpected, testJoke(onlyescapedJoke), "Jokes with only escaped characters are NOT detected")
}
