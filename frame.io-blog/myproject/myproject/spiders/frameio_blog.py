import scrapy
import csv


class FrameioBlogSpider(scrapy.Spider):
    name = "frameio_blog"
    allowed_domains = ["frame.io"]
    start_urls = ["https://blog.frame.io/category/post-production/"]

    def __init__(self, *args, **kwargs):
        super(FrameioBlogSpider, self).__init__(*args, **kwargs)
        # Initialize CSV file
        self.csv_file = open('frame-blog-articles.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Title', 'Author', 'Date', 'URL'])  # Write header

    def parse(self, response):
        for article in response.css("div#primary article"):
            title_without_strip = article.css("h3.entry-title a::text").get()
            title = title_without_strip.strip() #Stripping parenthesis and commas from title
            author = article.css("li.entry-meta-author a::text").get()
            date = article.css("li.entry-meta-date time::text").get()
            url = article.css("h3.entry-title a::attr(href)").get()

            self.csv_writer.writerow([title, author, date, url])

        next_page = response.css('a.next::attr(href)').get()
        print("Next page URL:", next_page)  # Debugging print statement
        if next_page is not None:
            yield response.follow(next_page, self.parse)