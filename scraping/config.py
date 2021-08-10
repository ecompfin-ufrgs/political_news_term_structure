
import database


class Config:
    
    LOG_FILENAME = "cofig"
    
    def __init__(self):
        self.database = database.Database(self.LOG_FILENAME)
        
    def run(self):
        self.database.execute(self.database.USE_DB)
        self.database.commit()
        self.database.execute(self.database.DROP_ARTICLE)
        self.database.execute(self.database.DROP_WEBSITE)
        self.database.commit()
        self.database.execute(self.database.CREATE_WEBSITE)
        self.database.execute(self.database.CREATE_ARTICLE)
        self.database.commit()
        self.create_newspapers()
        
        
    def create_newspapers(self):
       self.database.execute(self.database.INSERT_WEBSITE, ("Estado de Minas","minas"))
       self.database.commit()
        



if __name__ == "__main__":
    c = Config()
    c.run()