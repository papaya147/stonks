package main

import (
	"log/slog"
	"os"

	"github.com/papaya147/stonks/news_scraper"
)

func saveArticles() news_scraper.Articles {
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))
	s := news_scraper.NewMoneyControlScraper(logger)

	articles := s.Scrape(1, 30)

	err := articles.Save("money-control-articles")
	if err != nil {
		panic(err)
	}

	return articles
}

func formatArticles(articles news_scraper.Articles) {
	articles.FormatContent()

	err := articles.Save("money-control-articles-formatted")
	if err != nil {
		panic(err)
	}
}

func main() {
	articles := saveArticles()
	formatArticles(articles)
}