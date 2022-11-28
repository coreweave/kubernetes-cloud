package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"regexp"
	"sync"

	"github.com/gocolly/colly"
)

const (
	smashWordsURL    string = "www.smashwords.com"
	localCacheDir    string = "./smashwords_cache"
	westernRomanceID int    = 1245
	maxPageId        int    = 140
	bookListSize     int    = 20 // Number of books on each smashwords list page
)

func createBookFileName(title string) string {
	// Remove all non-alphanumeric characters from the title
	re := regexp.MustCompile(`[^\w]`)
	fileName := re.ReplaceAllString(title, "")

	return fileName
}

func downloadBook(title string, bookLink string, dataDir string) {
	fileName := createBookFileName(title)
	if fileName == "" {
		log.Printf("Skipping %s since the title is all symbols (probably not English)", title)
		return
	}

	filePath := fmt.Sprintf("%s/%s", dataDir, fileName)
	fullUrl := fmt.Sprintf("https://%s%s", smashWordsURL, bookLink)

	if _, err := os.Stat(dataDir); os.IsNotExist(err) {
		os.MkdirAll(dataDir, 0700)
	}
	file, err := os.Create(filePath)
	if err != nil {
		log.Fatal(err)
	}
	client := http.Client{
		CheckRedirect: func(r *http.Request, via []*http.Request) error {
			r.URL.Opaque = r.URL.Path
			return nil
		},
	}
	resp, err := client.Get(fullUrl)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	defer file.Close()

	log.Printf("Downloaded %s to %s\n", title, filePath)
}

func scrapeBookList(pageId int, dataDir string) {
	// Create a collector for the page that lists all books
	listCollector := colly.NewCollector(
		colly.AllowedDomains(smashWordsURL),
		colly.CacheDir(localCacheDir),
	)

	// Create another collector to scrape the book pages
	bookCollector := listCollector.Clone()

	// Before making a request print "Visiting ..."
	listCollector.OnRequest(func(r *colly.Request) {
		log.Println("Getting book links from", r.URL.String())
	})

	// Send all the individual book links through the book collector
	listCollector.OnHTML("a[class=library-title]", func(e *colly.HTMLElement) {
		link := e.Attr("href")
		bookCollector.Visit(link)
	})

	// Get the text file link and download when available
	bookCollector.OnHTML("div[id=pageContentFull]", func(e *colly.HTMLElement) {
		title := e.ChildText("h1")
		e.ForEach("a[title='Plain text; contains no formatting']", func(_ int, e *colly.HTMLElement) {
			book_link := e.Attr("href")
			downloadBook(title, book_link, dataDir)
		})
	})

	westernRomanceURL := fmt.Sprintf("https://%s/books/category/%d/downloads/0/free/any/%d", smashWordsURL, westernRomanceID, pageId)
	listCollector.Visit(westernRomanceURL)
}

func getDataDir() string {
	dataDirPtr := flag.String("data_dir", "./data", "directory that the book files will download to")
	flag.Parse()

	return *dataDirPtr
}

func main() {
	dataDir := getDataDir()

	wg := new(sync.WaitGroup)

	// Each list page only shows `bookListSize` books so scrape each one in parallel
	for i := 0; i <= maxPageId; i = i + bookListSize {
		wg.Add(1)
		go func(pageId int) {
			defer wg.Done()
			scrapeBookList(pageId, dataDir)
		}(i)
	}

	wg.Wait()
}
