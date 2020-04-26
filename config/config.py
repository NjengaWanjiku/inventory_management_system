class Config():
    DEBUG = True
    SECRET_KEY = 'gyjioollplokkijihuhyggtdrdddthjjooihuyggftfde'

class  Development():
    # database://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kiprugut@127.0.0.1:5432/postgres'

class Production():
    pass
    SQLALCHEMY_DATABASE_URI = 'postgres://abggqjxxipfojm:5af7d9ea18038e18bcecd21bad73727573c79d67bb0c9671a768883eb789e19e@ec2-52-201-55-4.compute-1.amazonaws.com:5432/d83hg5c2ovh1dq'
    SECRET_KEY = 'gyjioollplokkijihuhyggtdrdddthjjooihuyggftfdeunnity'
