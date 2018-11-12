# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 19:38:22 2018

@author: saurav
"""

from flask import Flask , render_template,flash,request,redirect,url_for,session,logging

from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
app=Flask(__name__)

#configuring MySql
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_HOST']='firstsample'
app.config['MYSQL_CURSORCLASS']='DictCursor'

#initialize mysql db
mysql=MySQL(app)

Articles = Articles()
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/articles')
def articles():
    return render_template('articles.html',articles=Articles)#passing the data parameter
@app.route('/article/<string:id>/')#<>is used to pass synamic values and not just only string/number
def article(id):
    return render_template('article.html',id=id)

class RegisterForm(Form):
    name=StringField('Name',[validators.Length(min=1,max=50)])
    username=StringField('Username',[validators.Length(min=4,max=25)])
    email=StringField('Email',[validators.Length(min=6,max=50)])
    password=PasswordField('Password',[
            validators.DataRequired(),
            validators.EqualTo('confirm',message='No match')
            ])
    confirm=PasswordField('Confirm')

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm(request.form)
    if request.method=='POST' and form .validate():
        name=form.name.data
        email=form.email.data
        username=form.username.data
        password=sha256_crypt.encrypt(str(form.password.data))
        
        #cursor creation
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)",(name,email,username,password))
        
        mysql.connection.commit()
        cur.close()
        flash('Registration Successful , try to Log in Now!!!','success')
        return redirect(url_for('login'))
        
        return render_template('register.html')
    return render_template('register.html',form=form)

if __name__ == '__main__':
    app.secret_key='secret1234'
    app.run(debug=True)#This is for auto refreshing the server so that fresh contents are automatically loaded
    