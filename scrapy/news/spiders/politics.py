import scrapy
import sqlite3

class MySpider(scrapy.Spider):
    name       = "g1"

    DROP_TABLE = """
        DROP TABLE IF EXISTS g1;
        """

    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS g1 (
        id    INT AUTO INCREMENT PRIMARY KEY,
        date  DATETIME,
        title VARCHAR(255),
        link  VARCHAR(255)
        );
        """
    
    INSERT_DATA = """
        INSERT INTO g1 (date, title, link)
        VALUES (?, ?, ?);
        """

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://g1.globo.com/politica/"]
        self.n          = 1
        self.conn       = sqlite3.connect("news.db")
        print("SQLite connection open.")
        self.conn.execute(self.DROP_TABLE)
        self.conn.execute(self.CREATE_TABLE)

    def __del__(self):
        self.conn.close()
        print("SQLite connection closed.")
        
    def parse(self, response):
        print(self.n)
        for page in response.xpath("//*[@class='feed-post-body']//a/@href").getall():
            yield response.follow(page, self.parse_article)
        self.n += 1
        if self.n <= 2000:
            next_page = (f"https://g1.globo.com/politica/index/feed/pagina-{self.n}.ghtml")
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        date = response.xpath("//time[@itemprop='datePublished']/text()").get()
        if date:
            day_time = date.split()
            day      = day_time[0]
            time     = day_time[1]
            YMD      = day.split("/")
            HMS      = time.split('h')
            new_date = f"{YMD[2]}-{YMD[1]}-{YMD[0]} {HMS[0]}:{HMS[1]}:00"

            title = response.xpath("//h1[@class='content-head__title']/text()").get()
            link  = response.url
            values = (new_date, title, link)
            self.conn.execute(self.INSERT_DATA, values)
            self.conn.commit()
