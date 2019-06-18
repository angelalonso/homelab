package main

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCreateMain(t *testing.T) {
	request, err := http.NewRequest("GET", "/", nil)
	assert.Equal(t, nil, err, "nil Error on getting request is expected")
	response := httptest.NewRecorder()
	Router().ServeHTTP(response, request)

	assert.Equal(t, 200, response.Code, "OK response is expected")
}

func TestCreateCheck(t *testing.T) {
	request, err := http.NewRequest("GET", "/check", nil)
	assert.Equal(t, nil, err, "nil Error on getting request is expected")
	response := httptest.NewRecorder()
	Router().ServeHTTP(response, request)

	assert.Equal(t, 200, response.Code, "OK response is expected")
}

func TestCreateMainContent(t *testing.T) {
	request, _ := http.NewRequest("GET", "/", nil)
	response := httptest.NewRecorder()
	Router().ServeHTTP(response, request)
	// the page Content must be readable
	pageContentInBytes, err := ioutil.ReadAll(response.Body)
	assert.Equal(t, nil, err, "nil Error on reading content buffer is expected")
	// the result of CreateMainContent must not be empty
	//assert.Equal(t, CreateMainContent(), pageContent, "OK response is expected")
	// the page content must be the same as the result of CreateMainContent
	pageContent := string(pageContentInBytes)
	assert.Equal(t, CreateMainContent(), pageContent, "OK response is expected")
	// the page must have a title
	titleStartIndex := strings.Index(pageContent, "<!DOCTYPE html>")
	assert.NotEqual(t, -1, titleStartIndex, "There should be a DOCTYPE tag")
}

func TestCreateCheckContent(t *testing.T) {
	request, _ := http.NewRequest("GET", "/check", nil)
	response := httptest.NewRecorder()
	Router().ServeHTTP(response, request)
	// the page Content must be readable
	pageContentInBytes, err := ioutil.ReadAll(response.Body)
	assert.Equal(t, nil, err, "nil Error on reading content buffer is expected")
	// the page content must include an OK
	// TODO: maybe check other information here (hostname, dependencies reachable...)
	pageContent := string(pageContentInBytes)
	assert.Contains(t, pageContent, "ok", "OK response is expected")

	assert.Equal(t, true, json.Valid(pageContentInBytes), "Not a valid JSON")
}

func TestGetBackendContent(t *testing.T) {
	assert.Equal(t, GetBackendContent(""), "No Host was provided for Backend", "Empty URL is not being handled")
	//Get http://0.0.0.0:90: dial tcp 0.0.0.0:90: connect: connection refused
	assert.Contains(t, GetBackendContent("0.0.0.0:90"), "Something is wrong at the Backend ->", "Http error response is not being handled")
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
