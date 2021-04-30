from email.message import EmailMessage
from re import error, sub
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
app.secret_key='United'
UPLOAD_FOLD =r'static\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLD
app.config["CLIENT_PDF"] = os.path.abspath(r'United_school-master\client\pdf')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
#app.config['SQLALCHEMY_DATABASE_URI']=r'postgres://bycqscsiivmkgf:b83e85ff50441729c05e6e6d11cb201c750f7dceed23ce635dac33379337dc99@ec2-18-204-74-74.compute-1.amazonaws.com:5432/de2qm4ed7agbri?sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI']=r'postgresql://postgres:saksham@localhost/us'
db=SQLAlchemy(app)
db1=SQLAlchemy(app)


sqrel = db.Table('sqrel',db.Model.metadata,
    db.Column('sid', db.String, db.ForeignKey('student.eno')),
    db.Column('qid', db.Integer, db.ForeignKey('quiz.id')))


class Data(db.Model):
    __tablename__="student"
    eno=db.Column(db.String(120),primary_key=True, unique=True)
    passw=db.Column(db.String(120))
    Name=db.Column(db.String(120))
    classs=db.Column(db.String(120))
    ContactNo=db.Column(db.String(120))
    Address=db.Column(db.String(120))
    Emailid=db.Column(db.String(120))
    result=db.Column(db.String(120))
    fees=db.Column(db.String(120))
    gives = db.relationship('Data3', secondary='sqrel', lazy='dynamic', backref=db.backref('takenby', lazy='dynamic'))

    def __init__(self, eno, passw,Name,classs,Contactno,Add,ema,res,fees):
        self.eno=eno
        self.passw=passw
        self.Name=Name
        self.classs=classs
        self.ContactNo=Contactno  
        self.Address=Add
        self.Emailid=ema
        self.result=res
        self.fees =fees

class announcement(db.Model):
    __tablename__="announcements"
    ids=db.Column(db.String(120),primary_key=True, unique=True)
    ann=db.Column(db.String(120))

    def __init__(self, ids,ann):
        self.ids=ids
        self.ann=ann

class carou(db.Model):
    __tablename__="cimg"
    ids=db.Column(db.String(120),primary_key=True, unique=True)
    path=db.Column(db.String(120))

    def __init__(self, ids,path):
        self.ids=ids
        self.path=path

class Notice(db.Model):
    __tablename__="journal"
    title=db.Column(db.String(120),primary_key=True)
    content=db.Column(db.String(120))
    filename=db.Column(db.String(120))

    def __init__(self,title,content,filename):
        self.title=title
        self.content=content
        self.filename=filename
class Books(db.Model):
    __tablename__="books"
    bno=db1.Column(db.Integer,primary_key=True, unique=True)
    Name=db.Column(db.String(120))
    edition=db.Column(db.String(120))
    Author=db.Column(db.String(120))
    Availability=db.Column(db.String(120))
    ISBN=db.Column(db.String(120))
    description=db.Column(db.String(120))
    path=db.Column(db.String(120))
    
    def __init__(self, bno, Name,edition,Author,Availability,ISBN,description,path):
        self.bno=bno
        self.Name=Name
        self.edition=edition
        self.Author=Author  
        self.Availability=Availability
        self.ISBN=ISBN
        self.description=description
        self.path=path


class Data1(db1.Model):
    __tablename__="teachers"
    tno=db1.Column(db1.String(120),primary_key=True, unique=True)
    passw=db1.Column(db1.String(120))
    Name=db.Column(db1.String(120))
    classs=db.Column(db1.String(120))
    ContactNo=db.Column(db1.String(120))
    Address=db.Column(db1.String(120))
    Emailid=db.Column(db1.String(120))

    def __init__(self, tno, passw,Name,classs,Contactno,Add,ema):
        self.tno=tno
        self.passw=passw
        self.Name=Name
        self.classs=classs
        self.ContactNo=Contactno  
        self.Address=Add
        self.Emailid=ema

class Data3(db.Model):
    __tablename__="quiz"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quizname=db.Column(db.String(120))
    rel1 = db.relationship('Data4', backref='quiz', lazy='dynamic')
    

    def __init__(self,qname,id=None):
        if id:
            self.id = id   # Otherwise, default to auto-increment
        self.quizname = qname

class Data4(db.Model):
    __tablename__="questions"
    qestid=db.Column(db.Integer,primary_key=True)
    questdescr=db.Column(db.String(500))
    ans1=db.Column(db.String(500))
    ans2=db.Column(db.String(500))
    ans3=db.Column(db.String(500))
    ans4=db.Column(db.String(500))
    correct=db.Column(db.String(500))
    qid=db.Column(db.Integer,db.ForeignKey('quiz.id'))

    def __init__(self, questdescr, a1,a2,a3,a4,correct,quzid,id=None):
        if id:
            self.id = id
        self.questdescr=questdescr
        self.a1=a1
        self.ans2=a2
        self.ans3=a3
        self.ans4=a4
        self.correct=correct
        self.qid=quzid

class Result(db.Model):
    __tablename__="result"
    rollno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject=db.Column(db.String(100),primary_key=True)
    marks=db.Column(db.Integer)

    def __init__(self,mark,roll,sub):
        self.rollno=roll
        self.marks=mark
        self.subject=sub

class Assignment(db.Model):
    __tablename__="assignmentQuestion"
    qid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject=db.Column(db.String(100))
    assignment=db.Column(db.String(100))
    qdesc=db.Column(db.String(1000))

    def __init__(self,ass,sub,qdesc,qid=None):
        if qid:    
            self.qid=qid
        self.assignment=ass
        self.subject=sub
        self.qdesc=qdesc

class AssignmentAns(db.Model):
    __tablename__="assignmentAnswer"
    qid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eno=db.Column(db.String(100),primary_key=True)
    assno=db.Column(db.String(100),primary_key=True)
    subno=db.Column(db.String(100),primary_key=True)
    answer=db.Column(db.String(1000))
    submitted=db.Column(db.Integer)

    def __init__(self,ass,sub,eno,qid,assno,subno):    
        self.qid=qid
        self.answer=ass
        self.submitted=sub
        self.eno=eno
        self.assno=assno
        self.subno=subno

        
@app.route("/",methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        data=request.form["Message"]
        name=request.form["name"]
        em=request.form["email"]
        phno=request.form["phno"]
        send_email(em,name,data,phno)
        flash("MESSAGE sUBMITTED TO THE ADMIN WAIT FOR REPLY ON PHONE!!!")
        return redirect("/")
    else:
        subjectExam=db.session.query(Data3).all()
        x=db.session.query(announcement.ann).all()
        caru=db.session.query(carou).order_by(carou.ids).all()
        return render_template("index.html",x=x,a=caru,sub=subjectExam)

@app.route("/student",methods=['GET', 'POST'])
def student():
    if request.method=='POST':
        session['username'] = request.form['eno']
        eno=session['username']
        pwd=request.form["pwd"]
        if db.session.query(Data).filter_by(eno=eno,passw=pwd).count()>=1:
            name=str(db.session.query(Data.Name).filter_by(eno=eno).first())[2:-3]
            classs=str(db.session.query(Data.classs).filter_by(eno=eno).first())[2:-3]
            c=str(db.session.query(Data.ContactNo).filter_by(eno=eno).first())[2:-3]
            a=str(db.session.query(Data.Address).filter_by(eno=eno).first())[2:-3]
            e=str(db.session.query(Data.Emailid).filter_by(eno=eno).first())[2:-3]
            r=str(db.session.query(Data.result).filter_by(eno=eno).first())[2:-3]
            fees=db.session.query(Data.fees).filter_by(eno=eno).scalar()
            result=db.session.query(Result).filter_by(rollno=eno).all()
            total_fees=90000
            remain=total_fees-int(fees)
            return render_template("student.html",name=name,classs=classs,con=c,add=a,email=e,res=r,tot=total_fees,fees=fees,remain=remain,result=result)
        else:
            subjectExam=db.session.query(Data3).all()
            x=db.session.query(announcement.ann).all()
            caru=db.session.query(carou).order_by(carou.ids).all()
            return render_template("index.html",x=x,data="User Not Found/Password Incorrect",a=caru,sub=subjectExam)


@app.route("/teacher",methods=['GET', 'POST'])
def teacher():
    if request.method=='POST':
        tno=request.form["tno"]
        tpwd=request.form["tpwd"]
        if tno=='9000' and tpwd=='admin':
            anno=db.session.query(announcement).all()
            car=db.session.query(carou).order_by(carou.ids).all()
            return render_template("admin.html",an=anno,a=car)
        elif db1.session.query(Data1).filter_by(tno=tno,passw=tpwd).count()>=1:
            name=str(db1.session.query(Data1.Name).filter_by(tno=tno).first())[2:-3]
            classs=str(db1.session.query(Data1.classs).filter_by(tno=tno).first())[2:-3]
            c=str(db1.session.query(Data1.ContactNo).filter_by(tno=tno).first())[2:-3]
            a=str(db1.session.query(Data1.Address).filter_by(tno=tno).first())[2:-3]
            e=str(db1.session.query(Data1.Emailid).filter_by(tno=tno).first())[2:-3]
            return render_template("teacher.html",name=name,classs=classs,con=c,add=a,email=e)
        else:
            x=db.session.query(announcement.ann).all()
            return render_template("index.html",x=x,data1="User Not Found/Password Incorrect")


@app.route("/quizquestion",methods=["POST"])
def quizquestion():
    return 'a'


@app.route('/Exam',methods=['POST','GET'])
def Exam():
    if request.method=='POST':
        eno=request.form["roll"]
        pwd=request.form["pass"]
        subid=request.form["subject"]
        questions=db.session.query(Data4).filter_by(qid=subid).all()
        random.shuffle(questions)
        flash('Quiz has been Started')
        if db.session.query(Data).filter_by(eno=eno,passw=pwd).count()>=1:
            session['username'] = eno
            session['sub']=subid
            return render_template('Exam.html', q = questions, o = questions,roll=eno,sub=subid)
        else:
            flash("User Not found")
            return redirect("/")
    else:
        return "Please Login"


@app.route("/Result", methods=['POST'])
def result():
    value=session['username']
    subid=session['sub']
    correct = 0
    questions=db.session.query(Data4).filter_by(qid=subid).all()
    for i in range(len(questions)):
        try:
            if questions[i].correct==request.form[str(questions[i].qestid)]:
                correct+=1
            else:
                correct-=1
        except:
            i+=1
    result=Result(roll=value,sub=subid,mark=correct)
    db.session.add(result)
    db.session.commit()   
    flash("Response Have Been Submitted!!!You can view it in your Result Section ")
    return redirect(url_for('index'))


@app.route("/library",methods=['GET', 'POST'])
def library():
    return render_template("library.html")


@app.route("/booklist/<string:ids>",methods=['GET'])
def booklist(ids):
    if ids=='books':
        return render_template("booklist.html")
    else:
        return render_template("ind")


@app.route("/test",methods=['GET', 'POST'])
def test():
    option = request.form['a']
    print(option)
    return render_template('teacher.html')
    


@app.route("/retustudent",methods=['GET', 'POST'])
def retustudent():
    eno=session['username']
    name=str(db.session.query(Data.Name).filter_by(eno=eno).first())[2:-3]
    classs=str(db.session.query(Data.classs).filter_by(eno=eno).first())[2:-3]
    c=str(db.session.query(Data.ContactNo).filter_by(eno=eno).first())[2:-3]
    a=str(db.session.query(Data.Address).filter_by(eno=eno).first())[2:-3]
    e=str(db.session.query(Data.Emailid).filter_by(eno=eno).first())[2:-3]
    r=str(db.session.query(Data.result).filter_by(eno=eno).first())[2:-3]
    fees=db.session.query(Data.fees).filter_by(eno=eno).scalar()
    total_fees=90000
    remain=total_fees-int(fees)
    return render_template("student.html",name=name,classs=classs,con=c,add=a,email=e,result=r,tot=total_fees,fees=fees,remain=remain)

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        title=request.form["title"]
        content=request.form["content"]
        f = request.files['filename']
        filep=secure_filename(f.filename)
        f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
        store=Notice(title,content,filep)
        db.session.add(store)
        db.session.commit()
        flash('file uploaded successfully')
        return redirect(url_for('retustudent'))

@app.route("/download/<path:filename>", methods = ['GET'])
def download(filename):
    try:
        p=os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory=p ,filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/journal",methods=['GET', 'POST'])
def journal():
    return render_template('editor.html')


@app.route("/shownotice",methods=['GET', 'POST'])
def shownotice():
    ids=db.session.query(Notice).all()
    head=['Title','Content','Download File']
    return render_template('journal.html',columns=head,ids=ids)
    

@app.route('/carouselImages/<string:i>',methods=['POST'])
def carouselImages(i):
    print(request.method)
    print(i)
    if request.method=='POST':
        if i=='1':
            f = request.files['filename0']
            filep=secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
            p=os.path.join(app.config['UPLOAD_FOLDER'],filep)
            db.session.query(carou).filter_by(ids=i).update({carou.path:p},synchronize_session=False)
            db.session.commit()
            return 'a'
        elif i=='2':
            f = request.files['filenamex']
            filep=secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
            p=os.path.join(app.config['UPLOAD_FOLDER'],filep)
            db.session.query(carou).filter_by(ids=i).update({carou.path:p},synchronize_session=False)
            db.session.commit()
            return 'a'
        elif i=='3':
            f = request.files['filename2']
            filep=secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
            p=os.path.join(app.config['UPLOAD_FOLDER'],filep)
            db.session.query(carou).filter_by(ids=i).update({carou.path:p},synchronize_session=False)
            db.session.commit()
            return 'a'
        elif i=='4':
            f = request.files['filename3']
            filep=secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
            p=os.path.join(app.config['UPLOAD_FOLDER'],filep)
            db.session.query(carou).filter_by(ids=i).update({carou.path:p},synchronize_session=False)
            db.session.commit()
            return 'a'
        elif i=='5':
            f = request.files['filename4']
            filep=secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
            p=os.path.join(app.config['UPLOAD_FOLDER'],filep)
            db.session.query(carou).filter_by(ids=i).update({carou.path:p},synchronize_session=False)
            db.session.commit()
            return 'a'
        elif i=='6':
            f = request.files['filename5']
            filep=secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
            p=os.path.join(app.config['UPLOAD_FOLDER'],filep)
            db.session.query(carou).filter_by(ids=i).update({carou.path:p},synchronize_session=False)
            db.session.commit()
            return 'a'
        elif i=='7':
            f = request.files['filename6']
            filep=secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
            p=os.path.join(app.config['UPLOAD_FOLDER'],filep)
            db.session.query(carou).filter_by(ids=i).update({carou.path:p},synchronize_session=False)
            db.session.commit()
            return 'a'
        else :
            f = request.files['filename7']
            filep=secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filep))
            p=os.path.join(app.config['UPLOAD_FOLDER'],filep)
            db.session.query(carou).filter_by(ids=i).update({carou.path:p},synchronize_session=False)
            db.session.commit()
            return 'a'

@app.route("/editann/<string:i>",methods=['GET', 'POST'])
def editann(i):
    if i=="newann":
        ai=request.form['aid']
        des=request.form['desc']
        newa=announcement(ai,des)
        db.session.add(newa)
        db.session.commit()
        return 'Hello'
    announcement.query.filter_by(ids=i).delete()
    db.session.commit()
    return 'Success'
    
@app.route("/student_Update",methods=['GET', 'POST'])
def student_Update():
    if request.method=='POST':
        eno=request.form['enrollmentnum']
        print(eno)
        info=db.session.query(Data).filter_by(eno=eno).first()
        return render_template('stud_update.html',info=info)

@app.route("/update_request",methods=['GET', 'POST'])
def update_request():
    if request.method=='POST':
        eno=request.form['enum']
        add=request.form["address"]
        name=request.form["name"]
        em=request.form["email"]
        phno=request.form["number"]
        db.session.query(Data).filter_by(eno=eno).update({Data.Address:add,Data.Name:name,Data.Emailid:em,Data.ContactNo:phno},synchronize_session=False)
        db.session.commit()
        anno=db.session.query(announcement).all()
        car=db.session.query(carou).order_by(carou.ids).all()
        return render_template("admin.html",an=anno,a=car)

@app.route("/assquestUpload",methods=['GET', 'POST'])
def assquestUpload():
    if request.method=='POST':
        subject=request.form['asssub']
        assino=request.form["assignment"]
        questions=request.form.getlist("field_name[]")
        print(questions)
        object=[]
        for i in questions:
            object.append(Assignment(sub=subject,ass=assino,qdesc=i))
        db.session.add_all(object)
        db.session.commit()
        return "DOne"

@app.route("/asiFetch",methods=['GET', 'POST'])
def asiFetch():
    eno=session['username']
    subject=request.args.get('subject')
    assino=request.args.get("Assignment")
    info=db.session.query(Data).filter_by(eno=eno).first()
    ans={}
    quest=db.session.query(Assignment).filter_by(subject=subject,assignment=assino).all()
    for i in quest:
        ans[i.qid]=db.session.query(AssignmentAns.answer).filter_by(eno=eno,subno=subject,assno=assino,qid=i.qid,submitted=0).all()
    print(ans)
    return render_template("AssignmentQuestions.html",eno=eno,question=quest,sub=subject,assi=assino,ans=ans)

@app.route("/saveasdraft",methods=['GET', 'POST'])
def saveasdraft():
    if request.method=='POST':
        qid=request.form.get('qid')
        eno=request.form.get("eno")
        ans=request.form.get("answer")
        sub=request.form.get("sub")
        assi=request.form.get("assi")
        b=bool(db.session.query(AssignmentAns).filter_by(eno=eno,qid=qid,subno=sub,assno=assi).first())
        if b==False:
            ans=AssignmentAns(qid=qid,eno=eno,ass=ans,sub=0,subno=sub,assno=assi)
            db.session.add(ans)
        else:
            db.session.query(AssignmentAns).filter_by(eno=eno,qid=qid,subno=sub,assno=assi).update({AssignmentAns.answer:ans},synchronize_session=False)

        db.session.commit()
        return 'Hello'

@app.route("/submitAssigAns",methods=['GET', 'POST'])
def submitAssigAns():
    if request.method=='POST':
        qid=request.form.get('qid')
        eno=request.form.get("eno")
        ans=request.form.get("answer")
        sub=request.form.get("sub")
        assi=request.form.get("assi")
        b=bool(db.session.query(AssignmentAns).filter_by(eno=eno,qid=qid,subno=sub,assno=assi).first())
        if b==False:
            ans=AssignmentAns(qid=qid,eno=eno,ass=ans,sub=1,subno=sub,assno=assi)
            db.session.add(ans)
        else:
            db.session.query(AssignmentAns).filter_by(eno=eno,qid=qid,subno=sub,assno=assi).update({AssignmentAns.answer:ans,AssignmentAns.submitted:1},synchronize_session=False)
        db.session.commit()
        return 'Hello'





def send_email(email,name,data,phno):
    from_email="unitedschool1@outlook.com"
    from_password="Unitedschool"

    to_email="shakti.agarg@gmail.com"
    subject="New Message"
    message="You have new message from  Name<strong> %s</strong> <br>Message: <strong> %s</strong><br>Phone Number:<strong> %s</strong><br>Email: <strong> %s</strong>:"%(name,data,phno,email)
    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email


    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.login(from_email,from_password)
    print ('server working fine')
    message=msg.as_string()
    server.sendmail(from_email,to_email,message)
    print('email sent')
    server.quit()
   


if __name__=="__main__":
    app.run(debug=True)