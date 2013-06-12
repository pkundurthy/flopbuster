

import MySQLdb

def_dBhost = 'localhost'
def_dBuser = 'root'
def_dBpass = ''
def_dBname = 'flopbuster'
def_path_to_socket = '/var/mysql/mysql.sock'


def dbConnect(dBhost=def_dBhost,dBuser=def_dBuser,\
              dBpass=def_dBpass,dBname=def_dBname,\
              path_to_socket=def_path_to_socket):
    """ standard MySQLdb connector to 'flopbuster' database """
    
    db = MySQLdb.connect(host=dBhost, user=dBuser,\
                         passwd=dBpass,db=dBname,unix_socket=path_to_socket)
    cursor = db.cursor()
    return cursor

def getTitles_BoxOffice():
    """
        get list of all movie titles from boxoffice table
    """

    cursor = dbConnect()
    foo  = 'select title from boxoffice;'
    cursor.execute(foo)
    results = cursor.fetchall()

    return [x[0] for x in results]

# def getInstance_BoxOfficeMovie(MovieName, countEntry=False):
#     """
#         find all data on a given movie title from BoxOffice table.
#         countEntry=True will return the number of rows for a given
#         match to MovieName string.
#     """

#     foo  = 'select title from boxoffice;' % (MovieName)
#     cursor.execute(foo)

#     print foo
