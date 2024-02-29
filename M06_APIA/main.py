import fastapi

import sqlalchemy.orm as orm
import services, schemas

app = fastapi.FastAPI()

services.create_database()

#TODO: Complete the API function to create a new user.
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: orm.Session=fastapi.Depends(services.get_db)):
    ...


#TODO: Complete the API function to retrieve user information based on a skip and limit parameter.
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: orm.Session = fastapi.Depends(services.get_db)):
    ...


#TODO: Complete the API function to retrieve user information based on a specific user_id.
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    ...


#TODO: Complete the API function to create an article for a user.
@app.post("/users/{user_id}/posts/", response_model=schemas.Article)
def create_article_for_user(user_id: int, article: schemas.ArticleCreate, 
                            db: orm.Session = fastapi.Depends(services.get_db)):
    ...


#TODO: Complete the API function to retrieve article information based on a skip and limit parameter.
@app.get("/posts/", response_model=list[schemas.Article])
def read_articles(skip: int = 0, limit: int = 10, db: orm.Session = fastapi.Depends(services.get_db)):
    ...


#TODO: Complete the API function to retrieve article information based on a specific article_id.
@app.get("/posts/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    ...


#TODO: Complete the API function to delete an article based on a specific article_id.
@app.delete("/posts/{article_id}")
def delete_article(article_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    ...


#TODO: Complete the API function to change the information of a given article based on a specific article_id.
@app.put("/posts/{article_id}")
def update_article(article_id: int, article: schemas.ArticleCreate, 
                   db: orm.Session = fastapi.Depends(services.get_db)):
    ...

