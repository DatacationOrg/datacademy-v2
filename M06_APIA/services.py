import sqlalchemy.orm as orm
import database, models, schemas

import datetime as dt

#TODO: Complete the create_database() function.
def create_database():
    ...

#TODO: Complete the get_db() function.
def get_db():
    ...

#TODO: Complete the get_user_by_email() function.
def get_user_by_email(db: orm.Session, email: str):
    ...

#TODO: Complete the create_user() function.
def create_user(db: orm.Session, user: schemas.UserCreate):
    ...


#TODO: Complete the get_users() function to retrieve all users with a given "user_id".
def get_users(db: orm.Session, skip: int = 0, limit: int = 10):
    ...


#TODO: Complete the get_user() function to retrieve only the first user with a given "user_id".
def get_user(db: orm.Session, user_id: int):
    ...


#TODO: Complete the create_user_article() function.
def create_user_article(db: orm.Session, article: schemas.ArticleCreate, user_id: int):
    ...


#TODO: Complete the get_articles() function to retrieve a set amount of articles.
def get_articles(db: orm.Session, skip: int = 0, limit: int = 10):
    ...


#TODO: Complete the get_article() function to retrieve only the first article with a given "article_id".
def get_article(db: orm.Session, article_id: int):
    ...


#TODO: Complete the delete_article() function to delete the article(s) with a given "article_id".
def delete_article(db: orm.Session, article_id: int):
    ...


#TODO: Complete the update_article() function to change the information of a certain article using its "article_id".
def update_article(db: orm.Session, article: schemas.ArticleCreate, article_id: int):
    ...

