from django.shortcuts import render, HttpResponse
import pyrebase
from django.contrib import auth
from django.utils import timezone

config = {
    'apiKey': "AIzaSyClzrs_FaBCrdjNlhJAHFmj-BP1wpzvSTc",
    'authDomain': "cpanel-10b49.firebaseapp.com",
    'databaseURL': "https://cpanel-10b49.firebaseio.com",
    'projectId': "cpanel-10b49",
    'storageBucket': "cpanel-10b49.appspot.com",
    'messagingSenderId': "789638283473"
}
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()
glb = ""


def signIn(request):

    return render(request, "signIn.html")

def postsign(request):
    global glb
    email = request.POST.get('email')
    glb = email
    target=open("text.txt",'w')
    target.write(email)
    target.close()
    passw = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid Credential"
        return render(request, "signIn.html", {'mess': message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "welcome.html", {'e': email})


def logout(request):
    auth.logout(request);
    return render(request, "signIn.html")

def signUp(request):
    return render(request, "signup.html")

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    user = authe.create_user_with_email_and_password(email, passw)
    return render(request, "signIn.html")


def send(request):
        global glb 
        d = {}
        count = 0
        chat = request.POST.get('chat')
        date=str(timezone.now())
        data = {"chat": chat,"date":date,"glb":glb}
        database.child("users").child("post").push(data)
        all_users = database.child("users").child("post").get()
        for user in all_users.each():
            temp = user.val()
           # for k, v in temp.items():
               # print(v)
            d[count] = temp
            count = count+1
        return render(request, "welcome.html", {"d": d, "e":glb})




