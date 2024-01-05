import sqlite3
import pandas as pd
import os

class uploadData:
    def __init__(self, dic_dfs:dict, db_name:str='database.db'):
        self.db_name = db_name
        self.db_file_path = f"./{self.db_name}"
        
        self.tables = ['auctions', 'lots', 'bids']
        self.dfs = dic_dfs

        self.create_connection()
        self.push_data()
        self.close_connection()

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_file_path)
        self.cur = self.conn.cursor()
    
    def push_data(self):
        for table in self.dfs:
            df = self.dfs[table]
            #df.columns = self.get_column_names_from_db_table(table_name=table)

            # The replace parameter drops the table before inserting new values.
            df.to_sql(name=table, con=self.conn, 
                    if_exists='replace', index=False,
                    chunksize=100000)

            print(f'--- Finished upload {table} data. ---')

    def close_connection(self):
        self.conn.close()             

    def get_column_names_from_db_table(self, table_name:str) -> list:
        """
        Scrape the column names from a database table to a list
        :param table_name: table name to get the column names from
        :return: a list with table column names
        """

        get_column_name_query = 'PRAGMA table_info(' + table_name + ');'
        self.cur.execute(get_column_name_query)
        table_column_names = self.cur.fetchall()

        column_names = list()

        for name in table_column_names:
            column_names.append(name[1])

        return column_names