from flask import Flask, render_template, request, redirect
import pymysql
import csv

# from render import render
app = Flask(__name__)

# @app.route('/entry', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST', 'DELETE'])  # its like app.get('/')
def message():
    return render_template('index.html')

@app.route('/home_name')
def my_name():
    name="richard"
    return ("Hello "+name+", Hope you're doing good")

@app.route('/name/<name>')
def my_nameurl(name):
    return ("Hello "+name+", Hope you're doing good")


@app.route('/submit',methods=['POST'])
def my_dbconn():
    id = request.form['id']
    name = request.form['name']
    php = int(request.form['php'])
    js = int(request.form['js'])
    java = int(request.form['java'])
    total = php + js +java
    average = total/3


    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="ngo_mis"
    )
    print( "DB connected Successfull .........")
    cur = conn.cursor()

    cur.execute("INSERT INTO student ( name, php, js, java, total, average) VALUES (%s, %s, %s, %s,%s, %s)", ( name, php, js, java, total, average))
    conn.commit()

# Exporting Report
    with open('report.csv', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([id, name, php, js, java, total, average]) 
    
    # return ("Data was Success Full Added !!!!")

    # return ('<script>alert("Inserted Succesfull !!!")</script>')
    return redirect('/report')
    


@app.route('/report')
def getAll():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="ngo_mis"
    )
    print( "DB connected Successfull .........")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    allstudent = rows
    return render_template('report.html', allstudent=allstudent)
    # return render_template('index.html')
    cur.close()


if(__name__=="__main__"):
    app.run(debug=True,port=5500)

