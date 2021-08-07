

class DatabaserScripts:
    INSERT_WEBSITE = "INSERT INTO websites (name, short_name, url) VALUEs (?, ?, ?);"
    INSERT_ARTICLE = "INSERT INTO articles (website_id, date, title, link) VALUES (?, ?, ?, ?);"
    INSERT_TEXTS = "INSERT INTO texts (article_id, text) VALUES (?, ?);"