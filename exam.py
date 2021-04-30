from flask import Flask,render_template,request,session,flash,redirect,url_for,send_from_directory,flash
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import random, copy
import smtplib
import requests
import string
import random
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:saksham@localhost/us'
db=SQLAlchemy(app)



class Data1(db.Model):
    __tablename__="answer"
    qid=db.Column(db.Integer,primary_key=True)
    ans1=db.Column(db.String(500))
    ans2=db.Column(db.String(500))
    ans3=db.Column(db.String(500))
    ans4=db.Column(db.String(500))
    correct=db.Column(db.String(500))
    rel1 = db.relationship('Data', backref='answer', lazy='dynamic')

    def __init__(self, subject, q1,q2,q3,q4,q5,id=None):
        if id:
            self.id = id
        self.subject = subject
        self.q1=q1
        self.q2=q2



class Data(db.Model):
    __tablename__="subject"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    standard=db.Column(db.String(120))
    subject=db.Column(db.String(120))
    question=db.Column(db.String(500))
    qid=db.Column(db.Integer,db.ForeignKey('answer.qid'))

    def __init__(self,standard, subject,q1,id=None):
        """Constructor"""
        if id:
            self.id = id   # Otherwise, default to auto-increment
        self.standard = standard
        self.subject = subject
        self.question=q1


class Quiz(db.Model):
    __tablename__="quiz"
    quizname=db.Column(db.String(120),primary_key=True)
    question=db.Column(db.String(120))
    option1=db.Column(db.String(120))
    option2=db.Column(db.String(120))
    option3=db.Column(db.String(120))
    option4=db.Column(db.String(120))
    correct=db.Column(db.String(120))

    def __init__(self,quizname,question,op1,op2,op3,op4,correct):
        self.quizname=quizname
        self.question=question
        self.option1=op1
        self.option2=op2
        self.option3=op3
        self.option4=op4
        self.correct=correct


#InSert into many to many db
statement = student_identifier.insert().values(class_id=cl1.id, user_id=sti1.id)
db.session.execute(statement)
db.session.commit()