from flask import Flask, render_template, request, redirect, url_for#, session,logging
#from flaskext.mysql import MySQL
from pyconnector import *
from mysql.connector import Error
import random, string
import os, sys
from flask_mysql_connector import MySQL



app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE'] = '+games'
mysql = MySQL(app)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
   return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   # if request.method == "POST": ##gets info from form
   #    userDetails = request.form
   #    email= userDetails['email']
   #    password = userDetails['password']
   #    cur = mysql.connection.cursor() #open cursor
   #    cursor.execute("Insert INTO users(email, password) VALUES(%s, %s)", (username, email)) #YOU HAVE TO SELECT, AND CHECK IF USER EXISTS IN DB
   #    cur.close()
   # else:
      return render_template('login.html')



@app.route('/signup', methods=['GET','POST'])
def signup():
   if request.method=='POST':
      mem_username=request.form.get('username')
      mem_email= request.form.get('email')
      mem_password= request.form.get('password')
      cur= mysql.connection.cursor()
      unique_id=random.randint(1,100000)
      print(mem_username)
      print(mem_email)
      print(mem_password)
      user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
      member_query= "insert into `Members` (`unique_id`, `mem_username`, `mem_email`, `mem_password`) values ({},'{}','{}', sha1('{}'));".format(unique_id,mem_username,mem_email,mem_password)
      try:
         cur.execute(user_query)
         cur.execute(member_query)
         return render_template('signup.html')
      except:
         return -1
   return render_template('signup.html')

@app.route('/requestgame', methods=['GET', 'POST'])
def requestgame():
   return render_template('requestgame.html')


@app.route('/example', methods=['GET', 'POST'])
def example():
   result = (request.form['result'])
   cursor = connection.cursor()
   cursor.execute("get database testing result", result)
   return render_template('example.html', result = result)


@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   return render_template('game_page.html')

@app.route('/game_list', methods=['GET', 'POST'])
def game_list():
   return render_template('game_list.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
   return render_template('profile.html')



if __name__ == '__main__':
   app.run(debug=True)