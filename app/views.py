# from app package(folder) import app objecty created in "__init__.py"
from app import app
from app.db import *
from flask import render_template, request, redirect, url_for, session, flash
import re
import bcrypt


#this view.py include public view functions and customer view functions

def get_session_user():
    username = session.get("USERNAME", "")
    return username

def is_customer(username):
    customer_details = get_customer_by_username(username)
    if customer_details is not None:
        return True    

def user_has_customer_permission(username):
    return is_customer(username)





app.config["SECRET_KEY"] = "ZO_ryq1DYvupTvnfIzGgBA"


@app.route("/")
def home():
    return render_template("public/home.html")



@app.route('/register', methods=['GET', 'POST'])
def register():

    req = request.form

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in req and 'password' in req and 'email' in req:
        # get all info from register form
        # cust_id null - auto fill
        first_name = req.get("first_name").capitalize()
        last_name = req.get("last_name").capitalize()
        username = req.get('username')
        email = req.get('email')
        password = req.get('password')

        # format address info to populate database Customer table Address collumn
        address = req.get("address")
        city = req.get("city")
        postcode = req.get("postcode")

        texts_in_address = [address, city, postcode]
        valid_text_in_address = [text for text in texts_in_address if text]

        if len(valid_text_in_address) == 0:
            formatted_address = None
        elif len(valid_text_in_address) == 1 and valid_text_in_address[0] == "Choose...":
            formatted_address = None
        else:
            formatted_address = ", ".join(valid_text_in_address)

        # format phone_number
        nzcode = req.get('nzcode')
        prefix = req.get('prefix')
        digits_1 = req.get('digits_1')
        digits_2 = req.get('digits_2')
        formatted_phone_number = nzcode + " " + prefix + " " + digits_1 + " " + digits_2



        # Check if account exists using MySQL
        cust_account = get_customer_by_username(username)

        # If account exists show error and validation checks
        if cust_account:
            flash('Account already exists!', "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!', "danger")
        elif not username or not password or not email:
            flash('Please fill out the form!', "warning")
        # password validation
        elif not len(password) >= 8:
            flash("Password must be at least 8 characters in length", "danger")
            return redirect(request.url)

        else:
            # Account doesnt exists and the form data is valid, hass pass
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # insert new customer info to database
            create_a_new_customer(first_name, last_name, username,
                                  formatted_address, email, formatted_phone_number, hashed)
            flash('You have successfully registered!', 'success')
            return redirect(url_for('sign_in'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!', 'warning')
        return redirect(request.url)

    return render_template('public/register.html')



@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():

    req = request.form

    if request.method == "POST":
        # get info from request form
        username_provided = req.get("username")
        password_provided = req.get("password")

        # Check if account exists in the database, fetch one record and return result
        cust_account = get_customer_by_username(username_provided)

        if cust_account is None:
            flash("Username not found",'danger')
            return redirect(request.url)
        else:
            hashed_pass_from_db = cust_account[7]

            if bcrypt.checkpw(password_provided.encode('utf-8'), hashed_pass_from_db.encode('utf-8')):
                session["USERNAME"] = cust_account[3]
                #print("User added to session")
                return redirect(url_for("dashboard", username=session["USERNAME"]))
            else:
                flash("Password incorrect","warning")
                return redirect(request.url)

    return render_template("public/sign_in.html")



@app.route('/sign-out')
def sign_out():
    session.pop('USERNAME', None)
    return redirect(url_for('home'))



@app.route("/dashboard/<username>")
def dashboard(username):
    if not user_has_customer_permission(get_session_user()):
        flash("You don't have permission to view this page", "warning")
        return redirect("home")
    else:
        cust_account = get_customer_by_username(get_session_user())
        first_name = cust_account[1]
        last_name = cust_account[2]
        user = first_name + " " + last_name
        return render_template("customer/dashboard.html",cust_account=cust_account, user=user, username=username)


@app.route("/customer-edit-profile", methods=["GET","POST"])
def customer_edit_profile():
    if user_has_customer_permission(get_session_user()):
        if request.method == 'GET':
            customer_username = request.args.get("customer_username")
            customer_details = get_customer_by_username(customer_username)
            return render_template("customer/customer_edit_profile.html", customer_details=customer_details)

        elif request.method == 'POST':
            req =request.form
            customer_username = req.get("username")

            # format address info to populate database Customer table Address collumn
            address = req.get("address")
            city = req.get("city")
            postcode = req.get("postcode")

            texts_in_address = [address, city, postcode]
            valid_text_in_address = [text for text in texts_in_address if text]

            if len(valid_text_in_address) == 0:
                formatted_address = None
            else:
                formatted_address = ", ".join(valid_text_in_address)

            # format phone_number
            nzcode = req.get('nzcode')
            prefix = req.get('prefix')
            digits_1 = req.get('digits_1')
            digits_2 = req.get('digits_2')
            formatted_phone_number = nzcode + " " + prefix + " " + digits_1 + " " + digits_2

            customer_edit_profile_in_db(formatted_address, formatted_phone_number, customer_username)
            flash("You have successfully updated your profile", "success")
            return redirect(url_for("dashboard", username=session["USERNAME"]))
            
    return redirect(url_for("home"))


@app.route("/customer-reset-password", methods=["GET","POST"])
def customer_reset_profile():
    if user_has_customer_permission(get_session_user()) and request.method == 'GET':
        customer_username = request.args.get("customer_username")
        customer_details = get_customer_by_username(customer_username)
        return render_template("customer/customer_reset_password.html", username = customer_username, details=customer_details)

    elif user_has_customer_permission(get_session_user()) and request.method == 'POST':
        req = request.form
        customer_username = req.get("username")           
        new_pass = req.get("new_pass")
        comfirm_pass = req.get("comfirm_pass")

        #check input correct
        if new_pass != comfirm_pass:
            flash("Passwords do not match. Please try again", "warning")
            return redirect(request.url)
        else: 
            #check password valid
            if not len(new_pass) >= 8:
                flash("Password must be at least 8 characters in length", "danger")
                return redirect(request.url)            
            else:
                # Account doesnt exists and the form data is valid, hass pass
                hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())

                #check if new pass is different from the old_pass
                customer_details = get_customer_by_username(customer_username)
                if customer_details is None:
                    flash("Customer user not found", "warning")
                    return redirect(url_for("dashboard", username=session["USERNAME"]))
                else:
                    old_pass = customer_details[7]
                    if hashed == old_pass:
                        flash("New password should be different from the old password", "warning")
                    else:
                        cust_reset_pass(hashed, customer_username)
                        flash("You've successfully changed your password", "success")
                        return redirect(url_for("dashboard", username=session["USERNAME"]))
                

@app.route("/available-cars")
def available_cars():
    if not user_has_customer_permission(get_session_user()):
        flash("You don't have the permission to view this page", "warning")
        return redirect(request.url)
    else:
        # check which cars are available by regi_num
        cars = get_all_cars()
        registration_nums_list = []
        available_cars_registration_num = []

        for car in cars:
            registration_nums_list.append(car[1])
        # print(registration_nums_list)

        for num in registration_nums_list:
            if car_is_available(num):
                available_cars_registration_num.append(num)
        # print(available_cars_registration_num)

        return render_template("customer/available_cars.html", cars=cars,
                                available_cars_registration_num=available_cars_registration_num)



@app.route("/customer-view-car-profile/<registration_num>", methods=["GET", "POST"])
def customer_view_car_profile(registration_num):

    if request.method == 'GET':
        if not user_has_customer_permission(get_session_user()): 
            flash("You don't have permission to view this page", "warning")
            return redirect(url_for('home'))
        else:
            registration_num = request.args.get(registration_num)
            if registration_num is not None:
                if request.method == 'POST':
                    car = get_car_by_registration_num(registration_num)
                    return render_template("customer/customer_view_car_profile.html", registration_num=registration_num)
            
            else:
                flash("Please provide registration number", "warning")
                return redirect(request.url)
        

