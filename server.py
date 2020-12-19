from flask import Flask,render_template,request,redirect,url_for,flash,abort,session
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from user import get_user_2, get_user
from wtforms import Form, BooleanField, StringField, validators,PasswordField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from passlib.hash import pbkdf2_sha256 as hasher
import forms
import webbrowser
import UrlSearch

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisisSecret'
app.config.from_object("settings")

@app.route("/")
def home_page():
     logout_user()
     return redirect(url_for("dashboard_page"))

@app.route("/dashboard",methods=['GET', 'POST'])
def dashboard_page():
    if request.method == 'POST':
        url = request.form["url"]
        
        return graph_page(url)
    return render_template("dashboard.html")

@app.route("/graph")
def graph_page(url):
    

    myob = UrlSearch.UrlSearch(url)
    myob.get_all_citas()
    lengt=len(myob.list_of_citas)
    i=0
    while i < lengt:
        j=0
        while j <lengt:
            if myob.all_citas[i]["title"]==myob.all_citas[j]["title"] or myob.all_citas[i]["link"]==myob.all_citas[j]["link"]:
                if i!=j and i<j:
                    myob.all_citas[i]["citation_text"]=myob.all_citas[i]["citation_text"]+"<br><br>"+(myob.all_citas[j]["citation_text"])
                    del myob.all_citas[j]
                    lengt=lengt-1
                    j=j-1
            j=j+1
        i=i+1
    cursor=[]
    for i in range(lengt):
        cursor.append(myob.all_citas[i])
    if len(cursor) == 0:
        flash('Please check your URL!')
        redirect(url_for('dashboard_page'))
    return render_template("graph.html",cursor=cursor)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

@app.route("/login",methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        obje = forms.ShowMe()
        cursor=obje.Check_existing_user(username)
        if len(cursor) != 1:
            flash("Warning!")
            #flash(len(cursor))
            #flash(cursor[0][1]])
            flash('Username or password is wrong')
            return redirect(url_for("login_page"))
        else:
            if not hasher.verify(password, cursor[0][1]):
                flash("Warning!")
                flash('Username or password is wrong!')
                return redirect(url_for("login_page"))
            else:
                #flash("Success!")
                #flash("You have already logged in successfully!")
                user = get_user_2(cursor[0][0], cursor[0][1])
                login_user(user, remember=True)
                next_page = request.args.get("next", url_for("my_profile_page"))
                return redirect(next_page)

@app.route("/")
def logout_page():
    print("1")
    logout_user()
    flash("Info!")
    flash("You have logged out.")
    return redirect(url_for("home_page"))
lm.init_app(app)
lm.login_view = "login_page"

@app.route("/sign_up",methods=['GET','POST'])
def sign_up_page():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        name= request.form["name"]
        surname= request.form["surname"]
        gender= request.form["gender"]
        username = request.form["username"]
        password = request.form["password"]
        obje = forms.ShowMe()
        cursor=obje.Check_username(username)
        #print(cursor)
        if cursor == False:
            flash("Warning!")
            flash("Please select a different username!")
            return redirect(url_for("sign_up_page"))
        else:
            obje.User_Add(name,surname,gender,username,hasher.hash(password))
        flash("Info!")
        flash("You have crated your account, please login!")
        return redirect(url_for("my_profile_page"))

@app.route('/profile')
@login_required
def my_profile_page():
    obje = forms.ShowMe()
    cursor=obje.get_gender(current_user.username)
    return render_template('myprofile.html', username=current_user.username, cursor=cursor[0][0])

@app.route('/profile/about',methods=['GET','POST'])
@login_required
def about_page(user_key):
    obje = forms.ShowMe()
    if request.method == 'POST':
        processAdd = request.form.get('buttonName')
        processUpdate = request.form.get('buttonName')
        processDelete = request.form.get('buttonName')
        if processAdd == "add":
            return redirect(url_for("about_adding_page"))
        elif processUpdate == "update":
            return redirect(url_for('about_update_page'))
        elif processDelete == "delete":
            obje.About_delete(current_user.username)
            cursor = obje.About_key(current_user.username)
            return render_template('about.html',cursor=cursor, username=current_user.username, currentuser=current_user.username)
    cursor=obje.About_key(user_key)
    return render_template('about.html', cursor=cursor, username=user_key, currentuser=current_user.username)
app.add_url_rule("/profile/about/<user_key>", view_func=about_page,methods=['GET','POST'])

@app.route('/profile/about/add',methods=['GET','POST'])
@login_required
def about_adding_page():
    obje = forms.ShowMe()
    if request.method == 'GET':
        return render_template('add_about.html')
    elif request.method == 'POST':
        username = current_user.username
        info = request.form["about"]
        cursor=obje.Check_about(username)
        if cursor == False:
            flash("Warning!")
            flash("Already added about!")
            cursor = obje.About_key(current_user.username)
            return redirect(url_for('about_page', user_key=current_user.username ))
        else:
            obje.About_add(username,info)
            #flash("You have updated about!")
            cursor = obje.About_key(current_user.username)
            return redirect(url_for('about_page', user_key=current_user.username ))
    return render_template('add_about.html')
app.add_url_rule("/profile/about/<user_key>", view_func=about_page,methods=['GET','POST'])

@app.route('/profile/about/update',methods=['GET','POST'])
@login_required
def about_update_page():
    obje = forms.ShowMe()
    if request.method == 'GET':
        cursor = obje.About_key(current_user.username)
        return render_template('update_about.html',cursor=cursor, username=current_user.username, currentuser=current_user.username)
    elif request.method == 'POST':
        info = str(request.form["about"])
        obje.About_update(current_user.username,info)
        #flash("You have updated about!")
        cursor = obje.About_key(current_user.username)
        return redirect(url_for('about_page', user_key=current_user.username ))
    cursor=obje.About_key(current_user.username)
    return render_template('update_about.html', cursor=cursor, username=current_user.username, currentuser=current_user.username)
app.add_url_rule("/profile/about/<user_key>", view_func=about_page,methods=['GET','POST'])


@app.route('/profile/see_all_users',methods=['GET','POST'])
@login_required
def see_all_users_page():
    obje = forms.ShowMe()
    if request.method == 'POST':
        processFollow = request.form.get('follow')
        processUnFollow = request.form.get('unfollow')
        if processFollow:
            source = current_user.username
            target = request.form["follow"]
            obje.Follow_add(source,target)
            flash("You have followed ",target)
            return redirect(url_for('see_all_users_page'))
        elif processUnFollow:
            source = current_user.username
            target = request.form["unfollow"]
            obje.Follow_delete(source,target)
            flash("You have unfollowed ",target)
            return redirect(url_for('see_all_users_page'))
    cursor=obje.All_Users(current_user.username)
    return render_template('users.html', cursor=cursor, username=current_user.username)
    
@app.route('/profile/followed_users',methods=['GET','POST'])
@login_required
def followed_users_page(user_key):
    obje = forms.ShowMe()
    if request.method == 'POST':
        processUnFollow = request.form.get('unfollow')
        if processUnFollow:
            source = current_user.username
            target = request.form["unfollow"]
            obje.Follow_delete(source,target)
            flash("You have unfollowed ",target)
            cursor = obje.Followed_users(user_key)
            return render_template('followed_users.html',cursor=cursor, username=user_key, currentuser=current_user.username)
    cursor = obje.Followed_users(user_key)
    return render_template('followed_users.html',cursor=cursor, username=user_key, currentuser=current_user.username)
app.add_url_rule("/profile/followed_users/<user_key>", view_func=followed_users_page, methods=['GET','POST'])

@app.route('/profile/bookmarks',methods=['GET','POST'])
@login_required
def bookmarks_page(user_key):
    obje = forms.ShowMe()
    if request.method == "POST":
        process = request.form.get('buttonName')
        if (process == "add"):
            return redirect(url_for("bookmark_adding_page"))
        elif(process == "delete"):
            form_bookmark_keys = request.form.getlist("bookmark_keys")
            for form_bookmark_key in form_bookmark_keys:
                obje.Bookmark_delete(int(form_bookmark_key))
            cursor = obje.Bookmarks(current_user.username)
            return render_template('bookmarks.html',cursor=cursor, username=current_user.username, currentuser=current_user.username)
    cursor = obje.Bookmarks(user_key)
    return render_template('bookmarks.html',cursor=cursor, username=user_key, currentuser=current_user.username)
app.add_url_rule("/profile/bookmarks/<user_key>", view_func=bookmarks_page)

@app.route('/profile/bookmarks/add',methods=['GET','POST'])
@login_required
def bookmark_adding_page():
    if request.method == 'GET':
        return render_template('add_bookmark.html')
    elif request.method == 'POST':
        url = str(request.form["url"])
        obje = forms.ShowMe()
        obje.Bookmark_add(current_user.username,url)
        flash("You have added.")
        return redirect(url_for('bookmarks_page', user_key=current_user.username ))
    return render_template('add_bookmark.html')
app.add_url_rule("/profile/bookmarks/<user_key>", view_func=bookmarks_page,methods=['GET','POST'])

@app.route('/profile/delete_account',methods=['GET','POST'])
@login_required
def delete_my_account_page(user_key):
    if user_key == current_user.username:
        if request.method == 'POST':
            password = request.form["password"]
            obje = forms.ShowMe()
            cursor=obje.Check_existing_user(current_user.username)
            if not hasher.verify(password, cursor[0][1]):
                flash("Warning!")
                flash("Password is wrong!")
                return redirect(url_for("delete_my_account_page",user_key=current_user.username))
            else:
                obje.Delete_account(current_user.username)
                return redirect(url_for('home_page'))
        return render_template('delete_my_account.html',username=user_key)
    return redirect(url_for("dashboard_page"))
app.add_url_rule("/profile/delete_account/<user_key>", view_func=delete_my_account_page,methods=['GET','POST'])

@app.route('/profile')
@login_required
def user_key(user_key):
    if current_user.username == user_key:
        return redirect(url_for('my_profile_page'))
    obje = forms.ShowMe()
    cursor=obje.get_gender(user_key)
    return render_template("other_profiles.html",username=user_key,cursor=cursor[0][0])
app.add_url_rule("/profile/<user_key>", view_func=user_key)

if __name__ == "__main__":
    app.run(debug=True)
