from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import mysql.connector as sql

fn = ''
ln = ''
g = ''
a = ''
ad = ''
ph = ''
em = ''
pwd = ''


# Create your views here.
def signaction(request):
    global fn, ln, g, em, pwd
    if request.method == "POST":
        m = sql.connect(host="127.0.0.1", user="root", passwd="", database='webdata')
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == "first_name":
                fn = value
            if key == "last_name":
                ln = value
            if key == "gender":
                g = value
            if key == "age":
                a = value
            if key == "address":
                ad = value
            if key == "phone_no":
                ph == value
            if key == "email":
                em = value
            if key == "password":
                pwd = value

        c = "insert into users Values('{}','{}','{}','{}','{}','{}','{}','{}')".format(fn, ln, g, a, ad, ph, em, pwd)
        cursor.execute(c)
        m.commit()

    return render(request, 'signup_page.html')