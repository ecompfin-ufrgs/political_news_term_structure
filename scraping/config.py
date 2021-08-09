
import database


class Config:
    
    LOG_FILENAME = "cofig"
    
    def __init__(self):
        self.database = database.Database(self.LOG_FILENAME)
        
    def run(self):
        self.database.execute(self.database.USE_DB)
        self.database.commit()
        self.database.execute(self.database.CREATE_WEBSITE)
        self.database.execute(self.database.CREATE_ARTICLES)
        self.database.commit()
        
        
    def create_website(self):
        self.database.execute(self.database.CREATE_WEBSITE)
    def create_minas(self):
       name = ("Estado de Minas")
       self.database.execute(self.database.INSERT_WEBSITE, name)
        



if __name__ == "__main__":
    c = Config()
    c.run()