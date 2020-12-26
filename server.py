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
import Keysearch
import random
import os
import requests
import shutil
from pathlib import Path
import time
from ctypes import wintypes, WINFUNCTYPE
import signal
import ctypes
import mmap
import sys

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

url_global = ' '
keyword_global = ' '

@app.route("/dashboard",methods=['GET', 'POST'])
def dashboard_page():
    global url_global
    global keyword_global
    recommended_array = [
    "https://www.researchgate.net/publication/229643636_Intellectual_capital_The_new_wealth_of_organizations",
    "https://www.researchgate.net/publication/309739646_Improving_Human-Robot_Interaction_Based_on_Joint_Attention",
    "https://www.researchgate.net/publication/6312176_Sequential_processing_of_interaural_timing_differences_for_sound_source_segregation_and_spatial_localization_Evidence_from_event-related_cortical_potentials",
    "https://www.researchgate.net/publication/330402717_Omni-script_Device_Independent_User_Interface_Development_for_Omni-channel_FinTech_Applications",
    "https://www.researchgate.net/publication/254222714_Document_Categorization_with_Modified_Statistical_Language_Models_for_Agglutinative_Languages",
    "https://www.researchgate.net/publication/262805964_HYBRIST_Mobility_Model-_A_Novel_Hybrid_Mobility_Model_for_VANET_Simulations",
    "https://www.researchgate.net/publication/337435554_Using_Statistical_Measures_and_Machine_Learning_for_Graph_Reduction_to_Solve_Maximum_Weight_Clique_Problems",
    "https://www.researchgate.net/publication/326319011_Intellectual_capital_knowledge_management_and_social_capital_within_the_ICT_sector_in_Jordan",
    "https://www.researchgate.net/publication/6502464_Development_of_AMSTAR_a_measurement_tool_to_assess_the_methodological_quality_of_systematic_reviews",
    "https://www.researchgate.net/publication/312941965_A_Survey_of_Inter-Vehicle_Communication",
    "https://www.researchgate.net/publication/319327465_LocalCoin_An_Ad-hoc_Payment_Scheme_for_Areas_with_High_Connectivity",
    "https://www.researchgate.net/publication/326606151_Privacy_Preserving_and_Cost_Optimal_Mobile_Crowdsensing_Using_Smart_Contracts_on_Blockchain",
    "https://www.researchgate.net/publication/7525373_Contribution_of_harmonicity_and_location_to_auditory_object_formation_in_free_field_Evidence_from_event-related_brain_potentials" ]
    random.shuffle(recommended_array)
    recommended = recommended_array[0]
    if request.method == 'POST':
        processURL = request.form.get('url')
        processRecommended = request.form.get('recommended')
        processKeyword = request.form.get('keyword')
        if processURL:
            url = request.form["url"]
            url_global = url
            try:
                myob = UrlSearch.UrlSearch(url)
                myob.fill_blanks()
            except:
                flash('Warning!')
                flash('Please check your URL!')
                return render_template("dashboard.html",cursor="URL")
            return redirect(url_for('graph_page'))
        elif processRecommended:
            url_global = recommended
            return redirect(url_for('graph_page'))
        elif processKeyword:
            keyword = request.form["keyword"]
            keyword_global = keyword
            myob2 = Keysearch.KeySearch(keyword_global)
            myob2.fill_results()
            if len(myob2.search_results) == 0:
                flash('Warning!')
                flash('Please check your KeyWord!')
                return render_template("dashboard.html",cursor="KEYWORD")
            return redirect(url_for('results_page'))
    return render_template("dashboard.html")

@app.route("/results",methods=['GET', 'POST'])
def results_page():
    global url_global
    keyword = keyword_global
    myob2 = Keysearch.KeySearch(keyword)
    myob2.fill_results()
    results = myob2.search_results
    if request.method == "POST":
        processURL = request.form.get('graph')
        if processURL:
            url_global = processURL
            return redirect(url_for('graph_page'))
    return render_template("results.html",cursor=results)

@app.route("/graph",methods=['GET', 'POST'])
def graph_page():
    url = url_global
    obje = forms.ShowMe()
    try:
        myob = UrlSearch.UrlSearch(url)
        myob.fill_blanks()
    except:
        flash('Warning!')
        flash('Please check your URL!')
        return redirect(url_for('dashboard_page'))

    myob = UrlSearch.UrlSearch(url)
    myob.fill_blanks()

    #cursor=[]  #citations
    #for i in range(len(myob.all_citas)):
    #    cursor.append(myob.all_citas[i])
    if not os.path.exists('./static/pdf'):
        os.makedirs('./static/pdf')
    try:
        r = requests.get(myob.your_article['download_link'])
        try:
            os.remove('./static/pdf/your_paper.pdf') 
        except:
            print('x')
        with open('./static/pdf/your_paper.pdf', 'wb') as f:
            f.write(r.content)
    except:
        try:
            os.remove('./static/pdf/your_paper.pdf') 
        except:
            print('x')
    ######################################################################
    processDownloadCit = request.form.get('download_cit')
    if processDownloadCit:
        if not os.path.exists('./static/pdf'):
                os.makedirs('./static/pdf')
        try:
            '''try:
                cit = UrlSearch.UrlSearch(processDownloadCit)
                cit.fill_blanks()
            except:
                flash('Warning!')
                flash('Please check your URL!')
                return redirect(url_for('dashboard_page'))'''

            cit = UrlSearch.UrlSearch(processDownloadCit)
            cit.fill_blanks()
            r2 = requests.get(cit.your_article['download_link'])
            try:
                os.remove('./static/pdf/cit_paper.pdf') 
            except:
                print('x')
            with open('./static/pdf/cit_paper.pdf', 'wb') as f:
                f.write(r2.content)
        except:
            try:
                os.remove('./static/pdf/cit_paper.pdf') 
            except:
                print('x')
    ######################################################################
    processDownloadRef = request.form.get('download_ref')
    if processDownloadRef:
        if not os.path.exists('./static/pdf'):
                os.makedirs('./static/pdf')
        try:
            '''try:
                ref = UrlSearch.UrlSearch(processDownloadCit)
                ref.fill_blanks()
            except:
                flash('Warning!')
                flash('Please check your URL!')
                return redirect(url_for('dashboard_page'))'''

            ref = UrlSearch.UrlSearch(processDownloadRef)
            ref.fill_blanks()
            r3 = requests.get(ref.your_article['download_link'])
            try:
                os.remove('./static/pdf/ref_paper.pdf') 
            except:
                print('x')
            with open('./static/pdf/ref_paper.pdf', 'wb') as f:
                f.write(r3.content)
        except:
            try:
                os.remove('./static/pdf/ref_paper.pdf') 
            except:
                print('x')
    ######################################################################    
    if current_user.is_authenticated:
        processAdd = request.form.get('add')
        processDelete = request.form.get('delete')
        if processAdd:
            url_add = str(request.form["add"])
            url_add = url_add.split("SPLITSPLIT")
            obje.Bookmark_add(current_user.username, url_add[0],url_add[1])
            return redirect(url_for('graph_page'))
        elif processDelete:
            url_delete = str(request.form["delete"])
            obje.Bookmark_delete_graph(current_user.username,url_delete)
            return redirect(url_for('graph_page'))
        cursorBookmarks = obje.Bookmarks(current_user.username)
        return render_template("graph.html",cursor=myob.all_citas, your_paper=myob.your_article, references=myob.all_references, cursorBookmarks=cursorBookmarks, your_paper_link=url,processDownloadCit=processDownloadCit,processDownloadRef=processDownloadRef)
    return render_template("graph.html",cursor=myob.all_citas, your_paper=myob.your_article, references=myob.all_references, your_paper_link=url,processDownloadCit=processDownloadCit,processDownloadRef=processDownloadRef)       
app.add_url_rule("/graph/<url>", view_func=graph_page,methods=['GET','POST']) 

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
        city = request.form["city"]
        email = request.form["email"]
        uni = request.form["uni"]
        tel = request.form["tel"]
        cursor=obje.Check_about(username)
        if cursor == False:
            flash("Warning!")
            flash("Already added about!")
            cursor = obje.About_key(current_user.username)
            return redirect(url_for('about_page', user_key=current_user.username ))
        else:
            obje.About_add(username,info,city,email,uni,tel)
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
        city = request.form["city"]
        email = request.form["email"]
        uni = request.form["uni"]
        tel = request.form["tel"]
        obje.About_update(current_user.username,info,city, email, uni, tel)
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
    global url_global
    obje = forms.ShowMe()
    if request.method == "POST":
        process = request.form.get('buttonName')
        processURL = request.form.get('graph')
        if (process == "add"):
            return redirect(url_for("bookmark_adding_page"))
        elif processURL:
            url_global = processURL
            return redirect(url_for('graph_page'))
        elif(process == "delete"):
            form_bookmark_keys = request.form.getlist("bookmark_keys")
            for form_bookmark_key in form_bookmark_keys:
                obje.Bookmark_delete(int(form_bookmark_key))
            cursor = obje.Bookmarks(current_user.username)
            return render_template('bookmarks.html',cursor=cursor, username=current_user.username, currentuser=current_user.username)
    cursor = obje.Bookmarks(user_key)
    return render_template('bookmarks.html',cursor=cursor, username=user_key, currentuser=current_user.username, url_global=url_global)
app.add_url_rule("/profile/bookmarks/<user_key>", view_func=bookmarks_page)

@app.route('/profile/bookmarks/add',methods=['GET','POST'])
@login_required
def bookmark_adding_page():
    if request.method == 'GET':
        return render_template('add_bookmark.html')
    elif request.method == 'POST':
        url = str(request.form["url"])
        title = str(request.form["title"])
        obje = forms.ShowMe()
        obje.Bookmark_add(current_user.username,url,title)
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


HandlerRoutine = WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)

def _ctrl_handler(sig):
    """Handle a sig event and return 0 to terminate the process"""
    if sig == signal.CTRL_C_EVENT:
        dir_path = Path('./static/pdf')
        shutil.rmtree(dir_path)
    elif sig == signal.CTRL_BREAK_EVENT:
        dir_path = Path('./static/pdf')
        shutil.rmtree(dir_path)
    else:
        print("UNKNOWN EVENT")
    return 0

ctrl_handler = HandlerRoutine(_ctrl_handler)


SetConsoleCtrlHandler = ctypes.windll.kernel32.SetConsoleCtrlHandler
SetConsoleCtrlHandler.argtypes = (HandlerRoutine, wintypes.BOOL)
SetConsoleCtrlHandler.restype = wintypes.BOOL


if __name__ == "__main__":
    if not SetConsoleCtrlHandler(ctrl_handler, 1):
        print("Unable to add SetConsoleCtrlHandler")
        exit(-1)
    app.run(debug=True)
