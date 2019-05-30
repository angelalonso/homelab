package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func Router() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("/", getAnswer).Methods("GET")
	return router
}

func getAnswer(w http.ResponseWriter, req *http.Request) {
	joke := `What do you call a white girl that can run faster than her brothers?
The redneck virgin.`
	w.WriteHeader(200)
	w.Write([]byte(joke))
}

func main() {
	PORT := "4490"
	fmt.Println("Serving on port " + PORT + "...")
	log.Fatal(http.ListenAndServe(":"+PORT, Router()))
}
