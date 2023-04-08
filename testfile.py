from flask import Flask, render_template, redirect, request, session, make_response, jsonify
from flask_session import Session
from testfile_db import *
# from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
application = app

# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'
# SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "test_api"
#     }
# )
# app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route("/")
def main():
    """
    If the user is not logged in, redirect them to the login page. 
    If they are logged in, get all the grants and render the userdetails.html template.
    :return: The data is being returned as a list of dictionaries.
    """
    if not session.get("name"):
        return redirect("/login")
    data = getall_grants()
    return render_template('userdetails.html', name=session.get("name"), role=session.get("role"), data=data)


@app.route("/team")
def team():
    """
    If the user is not logged in, redirect them to the login page. Otherwise, render the
    Teamdetails.html template
    :return: the rendered template.
    """
    if not session.get("name"):
        return redirect("/login")
    return render_template('Teamdetails.html', name=session.get("name"), role=session.get("role"))

@app.route("/requirement")
def requirement():
    """
    If the user is not logged in, redirect them to the login page. Otherwise, render the
    Teamdetails.html template
    :return: the rendered template.
    """
    if not session.get("name"):
        return redirect("/login")
    return render_template('index.html', name=session.get("name"), role=session.get("role"))

@app.route("/customer")
def customer():
    """
    If the user is not logged in, redirect them to the login page. Otherwise, render the
    CustomerDetails.html page
    :return: The customer() function is returning the CustomerDetails.html page.
    """
    if not session.get("name"):
        return redirect("/login")
    return render_template('CustomerDetails.html', name=session.get("name"), role=session.get("role"))


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    If the request method is POST, then get the username from the form, 
    print the result of the search function, 
    if the search function returns true, then set the session name to the username, 
    set the session role to the result of the getrole function, 
    and redirect to the home page, 
    otherwise redirect to the login page. 
    Finally, render the login page.
    :return: the rendered template.
    """
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")
        search(username,password)
        if search(username):
            session["name"] = username
            session["role"] = getrole(username)
            return redirect("/")
        else:
            return redirect("/login")
    return render_template('login.html')

@app.route("/application/<grant_name>/<ammount>", methods=["POST", "GET"])
def get_grant(grant_name,ammount):
    """
    If the request method is POST, then get the username from the form, 
    print the result of the search function, 
    if the search function returns true, then set the session name to the username, 
    set the session role to the result of the getrole function, 
    and redirect to the home page, 
    otherwise redirect to the login page. 
    Finally, render the login page.
    :return: the rendered template.
    """
    if not session.get("name"):
        return redirect("/login")
    try:
        if search_grant_ammount(grant_name,ammount):
            add_app(session["name"],grant_name,ammount)
            return redirect("/")
    except:
        return redirect("/")
    
@app.route("/register/<email>/<password>", methods=["POST", "GET"])
def register(email,password):
    """
    If the request method is POST, then get the username from the form, 
    print the result of the search function, 
    if the search function returns true, then set the session name to the username, 
    set the session role to the result of the getrole function, 
    and redirect to the home page, 
    otherwise redirect to the login page. 
    Finally, render the login page.
    :return: the rendered template.
    """
    try:
        register_user(email,password)
        return redirect("/")
    except:
        return redirect("/login")
    



#admin routes
@app.route("/admin/main",methods=["GET"])
def admin_main():
    """
    It gets all the grants from the database and renders the userdetails.html template with the data.
    :return: The data is being returned as a list of dictionaries.
    """
    data = getall_grants()
    if not session.get("name"):
        return redirect("/login")
    if not session.get("role") == "admin":
        return redirect("/")
    return render_template('userdetails.html', name=session.get("name"), role="admin", data=data)

@app.route("/admin/user/add/<name>/<password>", methods=["POST"])
def admin_user_add(name,password):
    """
    If the user is logged in and is an admin, add a new user
    
    :param name: The name of the user
    :param password: The password for the user
    :return: the redirect function.
    """
    if not session.get("name"):
        return redirect("/login")
    if not session.get("role") == "admin":
        return redirect("/")
    register_user(name,password)
    return redirect("/")

@app.route("/admin/user/remove/<name>", methods=["POST"])
def admin_user_remove(name):
    """
    If the user is logged in and is an admin, remove the user from the database
    
    :param name: The name of the user to remove
    :return: the redirect function.
    """
    if not session.get("name"):
        return redirect("/login")
    if not session.get("role") == "admin":
        return redirect("/")
    remove_user(name)
    return redirect("/")

@app.route("/admin/grant/add/<name>/<amount>/<site>", methods=["POST"])
def admin_grant_add(name,amount,site):
    """
    It checks if the user is logged in and if they are an admin, then it adds a grant to the database
    
    :param name: The name of the grant
    :param amount: The amount of money the grant is worth
    :param site: the site the grant is for
    :return: the redirect function.
    """
    if not session.get("name"):
        return redirect("/login")
    if not session.get("role") == "admin":
        return redirect("/")
    add_grant(name,amount,site)
    return redirect("/")

@app.route("/admin/grant/remove/<name>", methods=["POST"])
def admin_grant_remove(name):
    """
    It removes a grant from the database
    
    :param name: The name of the user to be removed
    :return: the redirect function.
    """
    if not session.get("name"):
        return redirect("/login")
    if not session.get("role") == "admin":
        return redirect("/")
    remove_grant(name)
    return redirect("/")

@app.route("/datapull", methods=["GET"])
def datapull():
    """
    If the user is not logged in, return a 500 error. If the user is logged in, return a 200 response
    with the data.
    :return: A list of dictionaries.
    """
    if not session.get("name"):
        data = {"message":"bad request"}
        return make_response(jsonify(data), 500)
    data = getall_grants()
    return make_response(jsonify(data), 200)


if __name__ == "__main__":
    app.run(debug=True)
