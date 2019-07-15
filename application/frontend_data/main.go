package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
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

type Post struct {
	ID    string `json:"id"`
	Title string `json:"title"`
	Body  string `json:"body"`
}

var posts []Post

func Router() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("/", CreateMain).Methods("GET")
	router.HandleFunc("/check", CreateCheck).Methods("GET")
	router.Path("/post/").Methods("GET").HandlerFunc(CreateResult)
	return router
}

func CreateMain(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte(CreateMainContent()))
}

func CreateCheck(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte(CreateCheckContent()))
}

func CreateResult(w http.ResponseWriter, req *http.Request) {
	joke, _ := req.URL.Query()["joke"]
	fmt.Println(joke)
	w.WriteHeader(200)
	w.Write([]byte(strings.Join(joke, " ")))
}

func CreateMainContent() string {
	html_main, err_html_main := ioutil.ReadFile("static/html_main")
	if err_html_main != nil {
		rlog.Error("Error reading html_main: " + err_html_main.Error())
		os.Exit(1)
	}
	return FormatContent(string(html_main))
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

func FormatContent(mainContent string) string {
	content := []byte{}
	html_header, err := ioutil.ReadFile("static/html_header")
	if err != nil {
		rlog.Error("Error reading html_header: " + err.Error())
		os.Exit(1)
	}
	css, err_css := ioutil.ReadFile("static/css")
	if err_css != nil {
		rlog.Error("Error reading css: " + err_css.Error())
		os.Exit(1)
	}
	js, err_js := ioutil.ReadFile("static/js")
	if err_js != nil {
		rlog.Error("Error reading js: " + err_js.Error())
		os.Exit(1)
	}
	html_footer, err_html_footer := ioutil.ReadFile("static/html_footer")
	if err_html_footer != nil {
		rlog.Error("Error reading html_footer: " + err_html_footer.Error())
		os.Exit(1)
	}

	content = append(content, html_header...)
	content = append(content, css...)
	content = append(content, mainContent...)
	content = append(content, js...)
	content = append(content, html_footer...)

	return string(content)
}

func main() {
	PORT := "4481"
	fmt.Println("Serving on port " + PORT + "...")
	log.Fatal(http.ListenAndServe(":"+PORT, Router()))
}
