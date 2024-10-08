import os
import string
import requests
from bs4 import BeautifulSoup


def write_files(articles, page_num):
    # Create a directory for the current page
    dir_name = f"Page_{page_num}"
    os.makedirs(dir_name, exist_ok=True)

    for article in articles:
        # Prepare the filename by replacing spaces with underscores and stripping punctuation
        filename = article['title'].replace(" ", "_").strip(string.punctuation) + '.txt'
        file_path = os.path.join(dir_name, filename)

        # Save the article content to a file
        with open(file_path, "w") as f:
            f.write(article['body'])


def parse_page(uri):
    response = requests.get(uri)
    if response.status_code == 200:
        response_soup = BeautifulSoup(response.content, features="html.parser")
        return response_soup
    else:
        raise Exception(f"The URL returned {response.status_code}")


def parse_articles(links):
    articles = []
    for link in links:
        rs = parse_page(link)
        title = rs.head.title.string
        body = rs.find("p", {"class": "article__teaser"})

        # Ensure the article body exists
        if body:
            articles.append({"title": title, "body": body.text.strip()})
    return articles


def parse_article_links(article_list):
    links = []
    for article in article_list:
        link_tags = article.find_all(attrs={"data-track-action": "view article", "data-track-label": "link"})
        for tag in link_tags:
            href = "https://www.nature.com" + tag.attrs["href"]
            links.append(href)
    return links


def get_filtered_articles(rs, article_type):
    articles = rs.find_all("article")
    filtered_articles = []

    for article in articles:
        spans = article.find_all("span", attrs={"data-test": "article.type"})
        for span in spans:
            if span.text.strip() == article_type:  # Filter by the user-provided article type
                filtered_articles.append(article)

    return filtered_articles


def main():
    # Get user input for the number of pages and article type
    num_pages = int(input("Enter the number of pages to scrape: "))
    article_type = input("Enter the article type to filter: ").strip()

    # Loop through the specified number of pages
    for page_num in range(1, num_pages + 1):
        try:
            # Update the URL to fetch articles from the current page
            url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page_num}"
            rs = parse_page(url)

            # Filter articles by type and get links
            filtered_articles = get_filtered_articles(rs, article_type)
            if filtered_articles:
                links = parse_article_links(filtered_articles)
                articles = parse_articles(links)
                write_files(articles, page_num)
            else:
                # Create an empty folder if no articles of the specified type are found
                os.makedirs(f"Page_{page_num}", exist_ok=True)

        except Exception as e:
            print(f"Error processing page {page_num}: {e}")

    print("Saved all articles.")


if __name__ == "__main__":
    main()
