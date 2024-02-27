import sqlalchemy as sql
import sqlalchemy.orm as orm

from database import Base

import datetime as dt

class User(Base):
    #TODO: Set the table name to "users".
    ...

    #TODO: Define the columns of the "users" table.
    ...

    #TODO: Set the orm.relationship() for the "users" table.
    ...


class Article(Base):
    #TODO: Set the table name to "articles".
    ...

    #TODO: Define the columns of the "articles" table.
    ...

    #TODO: Set the orm.relationship() for the "articles" table.
    ...

