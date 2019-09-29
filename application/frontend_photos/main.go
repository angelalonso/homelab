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
	if err := tmpl.Execute(w, &wd); err != nil {
		log.Println(err.Error())
		http.Error(w, http.StatusText(500), 500)
	}
}

func main() {
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))
	http.HandleFunc("/", homeHandler)
	port := ":9000"
	log.Println("Listening on port ", port)
	http.ListenAndServe(port, nil)
}
