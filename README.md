# Nature Articles Scraper

## Description

This Python project scrapes articles from the [Nature](https://www.nature.com/nature/articles?sort=PubDate&year=2020) website, based on user input for the number of pages and the type of articles to filter. The program dynamically navigates multiple pages of articles, filters them based on the specified type, and saves the filtered articles as `.txt` files into corresponding directories named by page number.

Each article is saved with a cleaned-up title as its filename, and the article content is extracted and stored in the file.

## Features

- Scrapes multiple pages of articles from the Nature website.
- Filters articles based on user-specified type (e.g., News, Nature Briefing, etc.).
- Saves the articles to separate text files, named after the article titles.
- Organizes articles into directories corresponding to the page number.
- Handles cases where no articles match the given type on a page by still crea