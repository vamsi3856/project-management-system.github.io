from django.shortcuts import render,redirect
from django.http import HttpResponse
import psycopg2

uname=''
password=''
cnfpassword=''
email=''
usname=''
title=''
demo_link=''
code_link=''
tags=''
college=''
skill1=''
skill2=''
skill3=''
description=''
linkedin=''
session={}

conn = psycopg2.connect(
    host="localhost",
    database="project_management",
    user="postgres",
    password="vamsi"
)
# Create your views here.
def index(request):
    cur=conn.cursor()
    cur.execute("SELECT * from uploads")
    t=tuple(cur.fetchall())
    if t!=():
        l=[]
        data=[]
        for i in t:
            for j in i:
                l.append(j)
            data.append(l)
            l=[]
        print("index data")
        print(data)
        session['data']=data
        return render(request,"index.html",{'data':data})
    else:
        return render(request,"index.html")

def registerUser(request):
    return render(request,"register.html")

def signup(request):
    global uname,password,cnfpassword,email
    if request.method=="POST":
        cursor = conn.cursor()
        d = request.POST
        print("vamsi")
        for key, value in d.items():
            if key == "uname":
                uname = value
            if key == "password":
                password = value
            if key == "cnfpassword":
                cnfpassword = value
            if key == "email":
                email = value
            if key == "college":
                college = value
            if key == "linkedin":
                linkedin = value
            if key == "skill1":
                skill1 = value
            if key == "skill2":
                skill2 = value
            if key == "skill3":
                skill3 = value
        print([uname, password, email])
        if password == cnfpassword:
            c = "INSERT INTO users(username, password, email, college, linkedin, skill1, skill2, skill3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (uname, password, email, college, linkedin, skill1, skill2, skill3)
            cursor.execute(c, values)
            conn.commit()
            return render(request, "index.html")
        else:
            return render(request, "register.html")


def login(request):
    global uname, password 
    if not session.get('user'):
        if request.method == "POST":
            cursor = conn.cursor()
            d = request.POST.dict()
            d.pop('csrfmiddlewaretoken', None)  # exclude CSRF token
            for key, value in d.items():
                if key == "uname":
                    uname = value
                if key == "password":
                    password = value
            print(uname, password)
            c = "SELECT * FROM users WHERE username='{}' AND password='{}'".format(uname, password)
            cursor.execute(c)
            t = tuple(cursor.fetchall())
            print(t)
            if t == ():
                return render(request, "login.html")
            else:
                session['user']=uname
                # cursor.execute("SELECT * from uploads")
                
                cursor.execute("SELECT * from uploads")
                t1=tuple(cursor.fetchall())
                if t1!=():
                    l=[]
                    data=[]
                    for i in t1:
                        for j in i:
                            l.append(j)
                        data.append(l)
                        l=[]
                    print("login data")
                    print(data)
                    session['data']=data
                    return render(request,"home.html",{'data':data,'uname':uname})
                else:
                    return render(request,"index.html")

                
                # return render(request, "home.html",{"uname":uname})
        return render(request, "login.html")
    else:
        return render(request, "home.html",{"uname":session.get('user')})

def add_pro(request):
    return render(request,"add_pro.html")

def add_projects(request):
    if session.get('user'):
        try:
            global usname,title,demo_link,code_link,tags,description
            usname=session.get('user')
            if request.method=="POST":
                cursor=conn.cursor()
                d=request.POST
                print("vamsi1")
                title = d.get("pro_title")
                demo_link = d.get("pro_demo")
                code_link = d.get("pro_code")
                tags = d.getlist("my_options")
                description = d.get("description")
                tag=[]
                for i in tags:
                    tag.append(i.lower())
                tags=','.join(tag)
                # print([usname,title,demo_link,code_link,tags,description])
                c = "INSERT INTO uploads(username, pro_title, demo_link, code_link, tags, description) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(usname, title.replace("'", "''"), demo_link, code_link, tags, description)   
                cursor.execute(c)
                conn.commit()
                return redirect('profile',usname)
            else:
                return HttpResponse("GET method") 
        except Exception as e:
            print(e)
            return HttpResponse("Error")
    return render(request,"login.html")

def profile(request,uname):
    if session.get('user'):
        cursor=conn.cursor()
        print(uname)
        cursor.execute("SELECT * from users where username=%s",(uname,))
        t = tuple(cursor.fetchall())
        lst=[]
        print(t)
        for i in t[0]:
            lst.append(i)
        cursor.execute("SELECT * from uploads where username=%s",(uname,))
        t1=tuple(cursor.fetchall())
        ln=len(t1)
        data=[]
        data1=[]
        print(t1)
        if t1!=():
            for k in t1:
                for j in k:
                    data1.append(j)
                data.append(data1)
                data1=[]
            print(data)
            if uname in t[0]:
                return  render(request,"profile.html",{'uname':uname,'lst':lst,'data':data,'ln':ln})
            else:
                session.pop('user',None)
                return render(request,"login.html")
        else:
            if uname in t[0]:
                return  render(request,"profile.html",{'uname':uname,'lst':lst,'ln':0})
            else:
                session.pop('user',None)
                return render(request,"login.html")
    else:
        return render(request,"login.html")

def userlist(request):
    cur=conn.cursor()
    cur.execute("select username,email from users")
    t=tuple(cur.fetchall())
    if session.get('user'):
        return render(request,"users.html",{'t':t,'uname':session.get('user')})
    else:
        return render(request,"users.html",{'t':t})

def delete(request,id,uname):
    if request.method=="POST":
        cur = conn.cursor()
        cur.execute("DELETE FROM uploads WHERE s_no = %s and username=%s", (id,uname))
        conn.commit()
        cur.close()
        # messages.success(request, "Tag deleted successfully")
        return redirect(f'/profile/{uname}')

def update_to(request,id,uname):
    if request.method=="POST":
        cur=conn.cursor()
        cur.execute("SELECT * from uploads where s_no=%s AND username=%s",(id,uname))
        t=tuple(cur.fetchall())
        l=[]
        for i in t[0]:
            l.append(i)
        return render(request,"update.html",{'id':id,'uname':uname,'l':l})

def update(request,id,uname):
    if request.method=="POST":
        cur = conn.cursor()
        d=request.POST
        title = d.get("pro_title")
        demo_link = d.get("pro_demo")
        code_link = d.get("pro_code")
        tags = d.getlist("my_options")
        description = d.get("description")
        tag=[]
        for i in tags:
            tag.append(i.lower())
        tags=','.join(tag)
        cur.execute("UPDATE uploads SET pro_title=%s,demo_link=%s,code_link=%s,tags=%s,description=%s WHERE s_no=%s and username=%s",(title,demo_link,code_link,tags,description,id,uname))
        conn.commit()
        cur.close()
        return redirect(f'/profile/{uname}')

def logout(request):
    session.pop('user',None)
    return render(request,"index.html",{'data':session.get('data')})