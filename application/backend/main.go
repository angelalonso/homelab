package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

type Dependency struct {
	Name   string `json:"name"`
	Status string `json:"status"`
}

type Check struct {
	Status       string       `json:"status"`
	Hostname     string       `json:"hostname"`
	Dependencies []Dependency `json:"dependencies"`
}

func Router() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("/", createMain).Methods("GET")
	router.HandleFunc("/check", createCheck).Methods("GET")
	return router
}

func createMain(w http.ResponseWriter, req *http.Request) {
	joke := `What do you call a white girl that can run faster than her brothers?
The redneck virgin.`
	w.WriteHeader(200)
	w.Write([]byte(joke))
}

func createCheck(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte(createCheckContent()))
}

func createCheckContent() string {
	hostname, err := os.Hostname()
	if err != nil {
		hostname = "unknown"
	}
	result := Check{
		Status:   "ok",
		Hostname: hostname,
	}

	jsonresult, err := json.MarshalIndent(&result, "", "\t")
	if err != nil {
		return "Error generating check result"
	}
	return string(jsonresult)
	/*
		hostname, err := os.Hostname()
		if err != nil {
			hostname = "unknown"
		}
		return "ok, " + hostname
	*/
}

func main() {
	PORT := "4490"
	fmt.Println("Serving on port " + PORT + "...")
	log.Fatal(http.ListenAndServe(":"+PORT, Router()))
}
