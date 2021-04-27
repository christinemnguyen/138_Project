from flask_mysql_connector import MySQL
from pyconnector import *
def dbreinit(logger,MySql,bool): #pass in mysql = MySQL(app) from init.py
    if bool==0:
        logger.debug("Database reinitialization deferred")
        return 0
    
    ddrop="drop database if exists `+games`;"
    cdb="create database `+games`;"
    udb="use `+games`;"

    companytable=   "CREATE TABLE Company (CompanyName VARCHAR(25),PRIMARY KEY (CompanyName),unique (CompanyName));"
    platformtable=  "CREATE TABLE Platform (platform_name varchar(25),PRIMARY KEY (platform_name));"
    gametable=      "CREATE TABLE Game(game_id varchar(25) not null,g_company varchar(25) not null,game_n varchar(25) not null,genre varchar(10),rating decimal(3,2),release_Date	date,price decimal(4,2),primary key (game_id,g_company),foreign key (g_company) references Company(CompanyName));"
    releasedontable="CREATE TABLE Released_on (game_id VARCHAR(25) not null,platform_name VARCHAR(25) not null,primary key (game_id,platform_name),foreign key (game_id) references Game(game_id) ON UPDATE CASCADE ON DELETE CASCADE,foreign key (platform_name) references Platform(platform_name) ON UPDATE CASCADE ON DELETE CASCADE);"
    userstable=     "CREATE TABLE Users (unique_id integer not null primary key,unique (unique_id));"
    guestable=      "CREATE TABLE Guests (unique_id integer(16) not null,primary key (unique_id),foreign key (unique_id) references Users(unique_id)on update cascade on delete cascade);"
    memberstable=   "create table Members (unique_id integer(16)not null,mem_username varchar(16)not null,mem_email VARCHAR(50),mem_password varchar(128) default null, primary key (unique_id, mem_username),foreign key (unique_id) references Users(unique_id)on update cascade on delete cascade,unique (mem_username));"
    requestgame=    "CREATE TABLE request_game (mem_username varchar(16) not null,game_id varchar(25),req_text varchar(50),foreign key (mem_username) references Members(mem_username) ON UPDATE CASCADE ON DELETE CASCADE,foreign key (game_id) references Game(game_id) ON UPDATE CASCADE ON DELETE CASCADE);"
    commenttable=   "CREATE TABLE comment_on (mem_username varchar(16)not null,game_id varchar(25)not null,c_date date,c_time time,comment_text varchar(250),primary key (mem_username, game_id),foreign key (mem_username) references Members(mem_username) on delete CASCADE,foreign key (game_id) references Game(game_id) on delete CASCADE);"
    reviewtable=    "CREATE TABLE review_on (mem_username varchar(16)not null,game_id varchar(10)not null,rv_date date,rv_time timestamp,review_text varchar(250),primary key (mem_username, game_id), foreign key (mem_username) references Members(mem_username) on delete CASCADE,foreign key (game_id) references Game(game_id) on delete CASCADE);"
    reporttable=    "CREATE TABLE report_on (mem_username varchar(16)not null,game_id varchar(10)not null,rp_date date,rp_time timestamp,report_text varchar(250),primary key (mem_username, game_id), foreign key (mem_username) references Members(mem_username) on delete CASCADE,foreign key (game_id) references Game(game_id) on delete CASCADE);"
    bookmarktable=  "CREATE TABLE bookmarked (mem_username varchar(16) not null,game_id varchar(10) not null,primary key (mem_username, game_id), foreign key (mem_username) references Members(mem_username) on delete CASCADE,foreign key (game_id) references Game(game_id) on delete CASCADE);"
    admintable=     "CREATE TABLE Administrator (unique_id integer(16) not null,admin_username varchar(16) not null,admin_email varchar(50),admin_password varchar(128) default null,primary key (unique_id, admin_username),foreign key (unique_id) references Users(unique_id)on update cascade on delete cascade,unique (admin_username));"
    profiletable=   "CREATE TABLE Profile (user_id integer(16) not null,name varchar(16),primary key (user_id));"
    interactable=   "CREATE TABLE interact_with (mem_username varchar(16),user_id integer(16),primary key (mem_username, user_id),foreign key (mem_username) references Members(mem_username) ON DELETE CASCADE,foreign key (user_id) references Profile(user_id) ON DELETE CASCADE);"
    managetable=    "CREATE TABLE manage (admin_username varchar(16) not null,user_id integer(16) not null,primary key (admin_username, user_id),foreign key (admin_username) references Administrator(admin_username) ON DELETE CASCADE,foreign key (user_id) references Profile(user_id) ON DELETE CASCADE);"

    execute_query(MySql.connection,ddrop)
    execute_query(MySql.connection,cdb)
    execute_query(MySql.connection,udb)

    execute_query(MySql.connection,companytable)
    execute_query(MySql.connection,platformtable)
    execute_query(MySql.connection,gametable)
    execute_query(MySql.connection,releasedontable)
    execute_query(MySql.connection,userstable)
    execute_query(MySql.connection,guestable)
    execute_query(MySql.connection,memberstable)
    execute_query(MySql.connection,requestgame)
    execute_query(MySql.connection,commenttable)
    execute_query(MySql.connection,reviewtable)
    execute_query(MySql.connection,reporttable)
    execute_query(MySql.connection,bookmarktable)
    execute_query(MySql.connection,admintable)
    execute_query(MySql.connection,profiletable)
    execute_query(MySql.connection,interactable)
    execute_query(MySql.connection,managetable)
    logger.debug("Database Reinitialized")
    return