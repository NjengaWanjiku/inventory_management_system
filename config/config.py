class Config():
    DEBUG = True
    SECRET_KEY = 'gyjioollplokkijihuhyggtdrdddthjjooihuyggftfde'

class  Development():
    # database://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kiprugut@127.0.0.1:5432/postgres'

class Production():
    pass
