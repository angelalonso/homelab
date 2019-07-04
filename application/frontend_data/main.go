package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

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
	router.HandleFunc("/", CreateMain).Methods("GET")
	router.HandleFunc("/check", CreateCheck).Methods("GET")
	return router
}

func CreateMain(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte("ok"))
}

func CreateCheck(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte(CreateCheckContent()))
}

func CreateCheckContent() string {
	backend_url := os.Getenv("BACKEND_HOST") + ":" + os.Getenv("BACKEND_PORT")
	hostname, err := os.Hostname()
	if err != nil {
		hostname = "unknown"
	}
	result := Check{
		Status:   "ok",
		Hostname: hostname,
		Dependencies: []Dependency{
			Dependency{
				Name:   backend_url,
				Status: TestConnection(backend_url),
			},
		},
	}

	jsonresult, err := json.MarshalIndent(&result, "", "\t")
	if err != nil {
		return "Error generating check result"
	}
	return string(jsonresult)
}

func TestConnection(url string) (response string) {
	fullurl := "http://" + url

	resp, err := http.Get(fullurl)
	if err != nil {
		response = err.Error()
	} else {
		response = strconv.Itoa(resp.StatusCode) + " " + string(http.StatusText(resp.StatusCode))
		//response = strconv.Itoa(resp.StatusCode)
	}

	return response
}

func main() {
	PORT := "4481"
	fmt.Println("Serving on port " + PORT + "...")
	log.Fatal(http.ListenAndServe(":"+PORT, Router()))
}
