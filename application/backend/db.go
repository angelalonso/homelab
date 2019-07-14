package main

import (
	"database/sql"
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/romana/rlog"
)

var (
	dbhost   = os.Getenv("DB_HOST")
	dbport   = os.Getenv("DB_PORT")
	user     = getVarFromFile(os.Getenv("DB_USER_FILE"))
	password = getVarFromFile(os.Getenv("DB_PASS_FILE"))
	dbname   = getVarFromFile(os.Getenv("DB_NAME_FILE"))
)

func getVarFromFile(filename string) string {
	content, err := ioutil.ReadFile(filename) // just pass the file name
	if err != nil {
		rlog.Debug("Error getting value from file " + filename + ": " + err.Error())
		return ""
	}
	return string(content)
}

func getJoke() string {
	rlog.Debug("Vars: " + dbhost + " - " + dbport + " - " + user + " - " + password + " - " + dbname)
	psqlInfo := fmt.Sprintf("host=%s port=%s user=%s "+
		"password=%s dbname=%s sslmode=disable",
		dbhost, dbport, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		rlog.Error("Error opening connection to Postgresql: " + err.Error())
		return "No joke received"
	}
	defer db.Close()

	joke := format4HTML(getRandomJoke(db))
	return joke
}

func getRandomJoke(db *sql.DB) string {
	sqlStatement := `SELECT 
	data -> 'joke' AS joke
	FROM jokes 
	WHERE id = $1;`

	source := rand.NewSource(time.Now().UnixNano())
	maxRand, errMaxRand := strconv.Atoi(getSelectCount(db))
	if errMaxRand != nil {
		rlog.Error("Error producing a random Number: " + errMaxRand.Error())
	}
	r := rand.New(source).Intn(maxRand)
	row := db.QueryRow(sqlStatement, r+1)
	var joke string
	switch err := row.Scan(&joke); err {
	case sql.ErrNoRows:
		rlog.Warn("No rows were returned!")
	case nil:
		rlog.Debug("Returning a proper joke: " + joke)
		return joke
	default:
		rlog.Error("Error getting jokes from the SELECT")
		return "No joke received"
	}
	return ""
}

func getSelectCount(db *sql.DB) string {
	sqlStatement := `SELECT COUNT (*) 
	FROM jokes;`

	row := db.QueryRow(sqlStatement)
	var count string
	switch err := row.Scan(&count); err {
	case sql.ErrNoRows:
		rlog.Debug("No rows were returned!")
	case nil:
		return count
	default:
		rlog.Error("Error getting NUMBER OF jokes from the SELECT COUNT")
		//TODO: can we NOT set a default of 1 here?
		return "1"
	}
	return "1"
}

func format4HTML(joke string) string {
	result := strings.Replace(
		strings.Replace(
			strings.Replace(joke, "\\n", "<br><br>", -1),
			"`", "'", -1),
		`"`, ``, -1)
	return result
}
