import mysql.connector
from mysql.connector import Error
import pandas as pd
import random, string
from IPython.display import display
import logging
logger = logging.getLogger('TLog')
logger.setLevel(logging.DEBUG)
logger.debug('Logger config message')
fhandler = logging.FileHandler(filename='logfile2.log', mode='a')
fhandler.setLevel(logging.DEBUG)
hformatter=logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fhandler.setFormatter(hformatter)
logger.addHandler(fhandler)
#-----------------
#Building blocks
#-----------------
#Connect to the database, necessary object for every query
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        #connect to the database
        connection = mysql.connector.connect(
            host=host_name, #use double quotes for all fields
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        connection.autocommit=False
        #autocommit disabled so we can rollback changes
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
        logger.debug('Db connection err')
    return connection

# use triple quotes if using multiline strings (i.e queries w/linebreaks)
#Pass in connection and string query, commits or rollbacks changes depending on errors
def execute_query(connection, query):

    #instance of connection
    #cursor is an abstraction meant for
    #data set traversal.
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        print("Query successful")
        connection.commit()
        cursor.close()
        logger.debug('Commit: '+query)

    except Error as err:
        print(f"Error: '{err}'")
        #Rollback changes due to errors
        connection.rollback()
        cursor.close()
        logger.debug('Rollback: '+query)
        raise err


#Pass in a connection and a string query, returns result
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        logger.debug('Fetching: '+query)
        return result
    except Error as err:
        print(f"Error: '{err}'")
        cursor.close()
        logger.debug('Badfetch: '+query)

#for testing purposes, returns a string of size length 
def randomstring(length):
    l = string.ascii_lowercase
    return ''.join(random.choice(l)for i in range(length))


#---------------------------------
#connector funcs
#---------------------------------


# use {}, '{}' for any raw arguments and string arguments,respectively.
# then at the end of the string use .format(parameter, ...)
def addmembers(connection, unique_id, mem_username, mem_email,mem_password):
    if(unique_id==0):
        unique_id=random.randint(1,100000)
    if mem_email == "" or mem_username =="" or mem_password == "":
        raise err
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
    member_query= "insert into `Members` (`unique_id`, `mem_username`, `mem_email`, `mem_password`) values ({},'{}','{}', sha1('{}'));".format(unique_id,mem_username,mem_email,mem_password)
    try: #This will fail the whole query and prevent a member being added to an already existing unique_id. Even though execute_query has a try/except, we need another try here to make sure we stop if the 1st exec fails
        execute_query(connection,user_query)
        execute_query(connection,member_query)
    except:
        exit

def addadmins(connection, unique_id, admin_username, admin_email, admin_password):
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
    adm_query="INSERT INTO administrator (unique_id, admin_username, admin_email, admin_password) VALUES({},'{}','{}',sha1('{}'));".format(unique_id,admin_username,admin_email,admin_password)
    try:
        execute_query(connection,user_query)
        execute_query(connection,adm_query)
    except:
        exit

def addguest(connection,unique_id):
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
    try:
        execute_query(connection,unique_id)
    except:
        exit


#add add game, comment, add review, company, console etc.
#LOOK AT THE WEBSITE
#Anything that a person clicks on the website, think what should be returned to webpage. Write functions that the front end can use to format and display it.

def returncolumns(connection,query):#basically read_query but returns a 2darray/column
    qresult=read_query(connection,query)
    resultlist1 = []
    for result in qresult:
        result = list(result)
        resultlist1.append(result)
    return resultlist1

def displaytable(columns,twoDarray): #columns = ["unique_id", "mem_username", "mem_password"]
    df = pd.DataFrame(twoDarray, columns=columns)
    display(df)



def sortbygenre(connection,genre):
    gamegenre = "SELECT * FROM Game ORDER BY '{}';".format(genre)
    return returncolumns(connection,gamegenre)


    
def sortbypopularity(connection):
    gamequery="select * from Game order by rating desc;" #uncertain, game not implemented yet so...
    return returncolumns(connection,gamequery)
    

def sortbyalphabetical(connection):
	gamealpha = "SELECT game_n FROM Game ORDER BY game_n ASC;"
	return returncolumns(connection,gamealpha)
	
	
def sordbyalphabeticaldesc(connection):
	gamealphadesc = "SELECT game_n FROM game ORDER BY game_n DESC;"
	return returncolumns(connection,gamealphadesc)

def platform(connection,released_on):
    chooseplatform = "SELECT DISTINCT platform_name FROM released_on WHERE platform_name = '{}';".format(platform_name)
    return returncolumns(connection,chooseplatform)

def sortbyplatform(connection,platform):
    chooseplatform = "SELECT * FROM Game join Released_on WHERE Game.game_id = Released_on.game_id and platform_name= '{}';".format(platform)
    #or this
    chooseplatform2 ="SELECT g.game_id,g.game_n,g.genre,g.rating,g.release_date,g.price FROM Game as g join Released_on as r WHERE g.game_id = r.game_id and r.platform_name='{}';".format(platform)
    return returncolumns(connection,chooseplatform)


def addcomment(connection, mem_username,game_id,text):
    insertq="insert into comment_on (mem_username, game_id,c_date,c_time,comment_text) values ('{}', {},NOW(),NOW(), '{}');".format(mem_username,game_id,text)
    execute_query(connection, insertq)

def addreview(connection, mem_username,game_id,text):
    insertq="insert into comment_on (mem_username, game_id,c_date,c_time,comment_text) values ('{}', {},NOW(),NOW(), '{}');".format(mem_username,game_id,text)
    execute_query(connection, insertq)
	
def addgame(connection,game_id,g_company,game_n,genre,rating,price):

    insertq = "INSERT INTO Game (game_id,g_company,game_n,genre,rating,release_Date,price) values ({},'{}','{}','{}',{},NOW(),{});".format(game_id,g_company,game_n,genre,rating,price)
    execute_query(connection, insertq)

def gamecomments(connection, game_id):
    game_comments = "select mem_username, c_date, c_time, comment_text from comment_on join Game on comment_on.game_id = Game.game_id where game_id={} order by c_time desc".format(game_id)
    return returncolumns(connection,game_comments)

def addbookmark(connection, mem_username, game_id):
        insertq="insert into bookmarked (mem_username, game_id) values ('{}', '{}');".format(mem_username, game_id)
        execute_query(connection, insertq)

