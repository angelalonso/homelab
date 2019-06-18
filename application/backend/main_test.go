package main

import (
	"io/ioutil"
	"net/http"
	"net/http/httptest"
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
}
