# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2

class AdscraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveToPostgreSQLPipeline:

    def __init__(self):
        self.conn = psycopg2.connect(
            #host="localhost",
            host="postgres",
            database="ads",
            user="postgres",
            password="postgres"
        )
        #self.conn.set_client_encoding("WIN1250")

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create apartments table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS apartments (
            id SERIAL PRIMARY KEY,
            title TEXT,
            image_url VARCHAR(255)
        );
        """)


    def process_item(self, item, spider):
        try:
            ## Define insert statement
            self.cur.execute("""
            INSERT INTO apartments(
                title,
                image_url
            ) VALUES (
                %s,
                %s     
            )
            """, (
                item["title"],
                item["image_url"]
            ))

            ## Execute insert of data into database
            self.conn.commit()
            return item
        except Exception as e:
            print(f'Error je:{e}')
            print('Anything else that you feel is useful')
            self.conn.rollback()
    

    def close_spider(self, spider):

        ## Close cursor & connection to database
        self.cur.close()
        self.conn.close()