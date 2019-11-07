class Config(object):
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DEFAULT_DB = 'ruralpower'

    JWT_SECRET = 'IVxZQ8t6vM9NmbHw7xbtEvCYDWYpW3xR1Aw/1l3LeX7gCGS/2zMa6qXIZC273Q=='
    JWT_HEADER = 'JWTAUTH'
    JWT_EXPIRED = 15 * 60
