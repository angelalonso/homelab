package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
	"github.com/romana/rlog"
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
	w.WriteHeader(200)
	w.Write([]byte(getJoke()))
}

func createCheck(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte(createCheckContent()))
}

func createCheckContent() string {
	hostname, err := os.Hostname()
	if err != nil {
		rlog.Warn("Hostname not defined")
		hostname = "unknown"
	}
	result := Check{
		Status:   "ok",
		Hostname: hostname,
	}

	jsonresult, err := json.MarshalIndent(&result, "", "\t")
	if err != nil {
		rlog.Error("Marshalling the JSON result did not work")
		return "Error generating check result"
	}
	return string(jsonresult)
}

func main() {
	PORT := "4490"
	rlog.Debug("Serving on port " + PORT + "...")
	log.Fatal(http.ListenAndServe(":"+PORT, Router()))
}
