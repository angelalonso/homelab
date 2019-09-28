package main

import (
	"html/template"
	"log"
	"net/http"
	"time"
)

type WebData struct {
	Title string
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	tmpl, _ := template.ParseFiles("templates/layout.html", "templates/home.html")
	now := time.Now()
	wd := WebData{
		Title: now.String(),
	}
	tmpl.Execute(w, &wd)
}

func pageHandler(w http.ResponseWriter, r *http.Request) {
	tmpl, _ := template.ParseFiles("templates/layout.html", "templates/page.html")
	wd := WebData{
		Title: "Page",
	}
	tmpl.Execute(w, &wd)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", homeHandler)
	mux.HandleFunc("/page", pageHandler)
	port := ":9000"
	log.Println("Listening on port ", port)
	http.ListenAndServe(port, mux)
}
