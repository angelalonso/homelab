package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func Router() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("/", CreateEndpoint).Methods("GET")
	return router
}

func CreateEndpoint(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte("Item Created"))
}

func main() {
	log.Fatal(http.ListenAndServe(":8080", Router()))
}
