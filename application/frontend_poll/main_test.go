package main

import (
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCreateEndpoint(t *testing.T) {
	request, err := http.NewRequest("GET", "/", nil)
	assert.Equal(t, nil, err, "nil Error on getting request is expected")
	response := httptest.NewRecorder()
	Router().ServeHTTP(response, request)

	assert.Equal(t, 200, response.Code, "OK response is expected")
}

func TestCreateContent(t *testing.T) {
	request, _ := http.NewRequest("GET", "/", nil)
	response := httptest.NewRecorder()
	Router().ServeHTTP(response, request)
	// the page Content must be readable
	pageContentInBytes, err := ioutil.ReadAll(response.Body)
	assert.Equal(t, nil, err, "nil Error on reading content buffer is expected")
	// the result of CreateContent must not be empty
	//assert.Equal(t, CreateContent(), pageContent, "OK response is expected")
	// the page content must be the same as the result of CreateContent
	pageContent := string(pageContentInBytes)
	assert.Equal(t, CreateContent(), pageContent, "OK response is expected")
	// the page must have a title
	titleStartIndex := strings.Index(pageContent, "<!DOCTYPE html>")
	assert.NotEqual(t, -1, titleStartIndex, "There should be a DOCTYPE tag")
}

func TestGetBackend(t *testing.T) {
	assert.Equal(t, GetBackend(""), "No Host was provided for Backend", "Empty URL is not being handled")
	//Get http://0.0.0.0:90: dial tcp 0.0.0.0:90: connect: connection refused
	assert.Contains(t, GetBackend("0.0.0.0:90"), "Something is wrong at the Backend ->", "Http error response is not being handled")
}

func TestParseResultEmpty(t *testing.T) {
	var expectedEmpty []Classifier
	classifiersEmpty := parseResult("")
	assert.Equal(t, classifiersEmpty, expectedEmpty, "The classifiers should contain something else")
	expected := []Classifier{
		Classifier{key: "radio_age", value: "21"},
		Classifier{key: "radio_sex", value: "other"},
	}
	classifiersFilled := parseResult("/post/?radio_age=21&radio_sex=other")
	assert.Equal(t, expected, classifiersFilled, "The classifiers should contain something else")
}
