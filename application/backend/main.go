package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

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
	return "ok, " + hostname
}

func main() {
	PORT := "4490"
	fmt.Println("Serving on port " + PORT + "...")
	log.Fatal(http.ListenAndServe(":"+PORT, Router()))
}
