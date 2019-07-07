package main

import (
	"database/sql"
	"fmt"
	"math/rand"
	"strconv"
	"strings"
	"time"
)

const (
	dbhost   = "localhost"
	dbport   = 5432
	user     = "miniuser"
	password = "minipass"
	dbname   = "minidb"
)

func getJoke() string {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
		"password=%s dbname=%s sslmode=disable",
		dbhost, dbport, user, password, dbname)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		//panic(err)
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
	maxRand, _ := strconv.Atoi(getSelectCount(db))
	r := rand.New(source).Intn(maxRand)
	row := db.QueryRow(sqlStatement, r+1)
	var joke string
	switch err := row.Scan(&joke); err {
	case sql.ErrNoRows:
		fmt.Println("No rows were returned!")
	case nil:
		return joke
	default:
		//panic(err)
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
		fmt.Println("No rows were returned!")
	case nil:
		return count
	default:
		//panic(err)
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
