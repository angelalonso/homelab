package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

func Router() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("/", CreateEndpoint).Methods("GET")
	router.HandleFunc("/post/", GetResult).Methods("GET")
	return router
}

func GetResult(w http.ResponseWriter, req *http.Request) {
	fmt.Println(req.URL)

}

func CreateEndpoint(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte(CreateContent()))
}

func CreateContent() string {
	content := []byte{}
	html_header, err := ioutil.ReadFile("static/html_header")
	if err != nil {
		fmt.Println("Error: " + err.Error())
		os.Exit(1)
	}
	css, err_css := ioutil.ReadFile("static/css")
	if err_css != nil {
		fmt.Println("Error: " + err_css.Error())
		os.Exit(1)
	}
	html_main, err_html_main := ioutil.ReadFile("static/html_main")
	if err_html_main != nil {
		fmt.Println("Error: " + err_html_main.Error())
		os.Exit(1)
	}
	js, err_js := ioutil.ReadFile("static/js")
	if err_js != nil {
		fmt.Println("Error: " + err_js.Error())
		os.Exit(1)
	}
	html_footer, err_html_footer := ioutil.ReadFile("static/html_footer")
	if err_html_footer != nil {
		fmt.Println("Error: " + err_html_footer.Error())
		os.Exit(1)
	}

	content = append(content, html_header...)
	content = append(content, css...)
	content = append(content, html_main...)
	content = append(content, js...)
	content = append(content, html_footer...)

	return string(content)

}

func main() {
	PORT := "4480"
	fmt.Println("Serving on port " + PORT + "...")
	log.Fatal(http.ListenAndServe(":"+PORT, Router()))
}
