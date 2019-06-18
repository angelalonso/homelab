package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	//"net/http/httptest"
	"os"
	"strings"

	"github.com/gorilla/mux"
)

type Classifier struct {
	key   string
	value string
}

func Router() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("/", CreateMain).Methods("GET")
	router.HandleFunc("/check", CreateCheck).Methods("GET")
	router.HandleFunc("/post/", CreateResult).Methods("GET")
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
	backend_url := os.Getenv("BACKEND_HOST") + ":" + os.Getenv("BACKEND_PORT")
	w.WriteHeader(200)
	w.Write([]byte(CreateResultContent(backend_url)))
}

func GetBackendContent(backend_url string) string {
	var client http.Client
	var result string
	resp, err := client.Get("http://" + backend_url)
	if err != nil {
		if err.Error() == "Get http:: http: no Host in request URL" {
			return "No Host was provided for Backend"
		}
		return "Something is wrong at the Backend -> " + err.Error()
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		result = string(bodyBytes)
	}
	return result
}

func CreateMainContent() string {
	html_main, err_html_main := ioutil.ReadFile("static/html_main")
	if err_html_main != nil {
		fmt.Println("Error: " + err_html_main.Error())
		os.Exit(1)
	}
	return FormatContent(string(html_main))
}

func CreateCheckContent() string {
	hostname, err := os.Hostname()
	if err != nil {
		hostname = "unknown"
	}

	/*response, httperr := http.Get("http://0.0.0.0:4490/check")
	if httperr != nil {
		hostname = "unknown"
	}
	*/
	//TODO: use JSON library to build this instead
	return `{"status": "ok", "hostname": "` + hostname + `"}`
	//	return `{"status": "ok", "hostname": "` + hostname + `", "backend": "` + string(response.StatusCode) + `"}`
}

func CreateResultContent(backend_url string) string {
	var client http.Client
	var response string
	resp, err := client.Get("http://" + backend_url)
	if err != nil {
		if err.Error() == "Get http:: http: no Host in request URL" {
			return "No Host was provided for Backend"
		}
		return "Something is wrong at the Backend -> " + err.Error()
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		response = string(bodyBytes)
	}
	result := FormatContent(`<body><div id="regMsg"><h1>` + response + `</h1></div>`)
	return result
}

func parseResult(result string) []Classifier {
	var c []Classifier

	splittedResult := strings.Split(strings.Replace(result, "/post/?", "", 1), "&")
	if len(splittedResult[0]) > 0 {
		for _, each := range splittedResult {
			newClassifier := Classifier{
				key:   strings.Split(each, "=")[0],
				value: strings.Split(each, "=")[1],
			}
			c = append(c, newClassifier)
		}
	}

	return c
}

func FormatContent(mainContent string) string {
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
	content = append(content, mainContent...)
	content = append(content, js...)
	content = append(content, html_footer...)

	return string(content)
}

func main() {
	PORT := "4480"
	fmt.Println("Serving on port " + PORT + "...")
	log.Fatal(http.ListenAndServe(":"+PORT, Router()))
}
