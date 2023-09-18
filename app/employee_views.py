from app import app
from app.db import *
from flask import render_template, request, redirect, url_for, session, flash
import re
import bcrypt
from datetime import datetime


app.config["SECRET_KEY"] = "ZO_ryq1DYvupTvnfIzGgBA"


def get_registration_num_in_db_as_list():
    cars = get_all_cars()
    registration_num_in_db = []
    for car in cars:
        registration_num_in_db.append(car[1])
    result = registration_num_in_db
    return result


def user_has_employee_permission(): #staff+admin permission
    if session.get("USERNAME", None) is not None:
        user = session["USERNAME"]
        employee_account = get_employee_by_username(user)

        if employee_account is None:
            flash("You do not have permission to view this page", "warning")
            return False
        else:
            return True
    else:
        flash("You need to sign in as an employee", "warning")
        return False
    

def is_admin_user(username) ->bool:
    employee_account = get_employee_by_username(username)
    if employee_account is not None:
        if employee_account[8] == 1:
            return True

        
def is_staff_user(username) ->bool:
    employee_account = get_employee_by_username(username)
    if employee_account is not None:
        if employee_account[8] == 0:
            return True

  
def user_has_admin_permission():
    if session.get("USERNAME", None) is not None:
      user = session["USERNAME"]
      if is_admin_user(user):
          return True


def user_has_staff_permission():
    if session.get("USERNAME", None) is not None:
      user = session["USERNAME"]
      if is_staff_user(user):
          return True


def get_staff_username_in_session():
    staff_username = None

    if session.get("USERNAME", None) is not None:
        username = session["USERNAME"]
        employee_account = get_employee_by_username(username)
        if employee_account is not None:
            if employee_account[8] == 0:
                staff_username = employee_account[4]
    return staff_username

######################################################

MAKES = ["Toyota", "Honda", "Tesla", "Mercedes-Benz"]
MANUFACTURING_YEAR = [2023, 2022, 2021, 2020,
                      2019, 2018, 2017, 2016, 2015, 2014, 2013]
SEATING_CAPACITY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


#######################################################


@app.route('/employee-sign-in', methods=['GET', 'POST'])
def employee_sign_in():

    req = request.form
    # is_admin = False

    if request.method == "POST":
        username_provided = req.get("username")
        password_provided = req.get("password")

        # Check if account exists in the database, fetch one record and return result
        employee_account = get_employee_by_username(username_provided)

        if employee_account is None:
            flash("Username not found", 'danger')
            return redirect(request.url)
        else:
            pass_from_db = employee_account[9]

            if password_provided == pass_from_db and employee_account[8] == 1:
                session["USERNAME"] = employee_account[4]
                print(session["USERNAME"])
                # is_admin = True
                # print("User added to session")
                return redirect(url_for("admin_dashboard", username=session["USERNAME"]))
            elif password_provided == pass_from_db and employee_account[8] == 0:
                session["USERNAME"] = employee_account[4]
                # is_admin = False
                return redirect(url_for("staff_dashboard", username=session["USERNAME"]))
            else:
                flash("Password incorrect", "warning")
                return redirect(request.url)

    return render_template("employee/employee_sign_in.html")


@app.route("/staff-dashboard/<username>")
def staff_dashboard(username):

    if session.get('USERNAME', None) is not None:
        employee_account = get_employee_by_username(session["USERNAME"])
        if employee_account is not None and employee_account[8] == 0:
            username = employee_account[4]
            return render_template("employee/staff_dashboard.html", employee_account=employee_account, username=username)
    else:
        flash("User not found")
        return redirect(url_for('employee_sign_in'))


@app.route("/admin-dashboard/<username>")
def admin_dashboard(username):
    employee_account = get_employee_by_username(username)

    if session.get('USERNAME', None) is not None:
        username = employee_account[4]
        return render_template("employee/admin_dashboard.html", employee_account=employee_account, username=username)
    else:
        flash("User not found")
        return redirect(url_for('employee_sign_in'))


@app.route("/list-customers")
def list_customers():
    if user_has_employee_permission():  
      all_customers = get_all_customers()
      return render_template("employee/list_customers.html", all_customers=all_customers)
    else:
      return redirect(url_for("employee_sign_in"))


@app.route("/add-customer", methods=['GET', 'POST'])
def add_customer():
    req = request.form
    if user_has_admin_permission():
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
            flash('You have successfully added a new customer!', 'success')
            return redirect(url_for('list_customers'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!', 'warning')
        return redirect(request.url)
        
    return render_template("employee/add_customer.html")


@app.route("/customer-profile", methods=["GET"])
def customer_profile():

    if not user_has_employee_permission():
        flash("You need to sign in as an employee", "warning")
        return redirect(url_for("employee_sign_in"))
    else:
        if request.method == 'GET':
            customer_username = request.args.get("username")

            if customer_username is not None:
                customer_details = get_customer_by_username(customer_username)

                if customer_details is not None:
                    return render_template("employee/customer_profile.html", customer_username=customer_username, customer_details=customer_details)


    return redirect(url_for("admin_dashboard", username=session["USERNAME"]))


@app.route("/update-customer", methods=["GET"])
def fetch_customer_username():

    if user_has_admin_permission():

        if request.method == 'GET':
            customer_username = request.args.get("username")

            if customer_username is not None:
                customer_details = get_customer_by_username(customer_username)

                if customer_details is not None:
                    return render_template("employee/update_customer.html", customer_details=customer_details)
                
            else:
                flash("Customer not found", "danger")
                return redirect(url_for("list_customers"))
            
    else:
        flash("You have no permission to view this page", "warning")
        return redirect(url_for("employee_sign_in"))        
    
            
@app.route("/update-customer", methods=["POST"])
def update_customer():

    if user_has_admin_permission():
        if request.method == "POST":
            req = request.form
            customer_username = req.get("customer_username")

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

            print(formatted_address)
            print(customer_username)

            # insert updated info into customers table where username = username
            update_customer_info(formatted_address, customer_username)
            flash("You have successfully update the customer infomation", "success")
        return redirect(url_for("customer_profile"))
        
    else:
        flash("You have no permission to view this page", "warning")
        return redirect(url_for("employee_sign_in"))


@app.route("/delete-customer", methods=['GET'])
def delete_customer():
  if user_has_admin_permission():
    if request.method == 'GET':
        customer_username = request.args.get("username")

        # delete customer from to Customers table
        delete_customer_by_username(customer_username)
        flash("You have successfully delete the customer!", "success")
        return redirect(url_for("list_customers"))
    return redirect(url_for("list_customers"))


@app.route("/list-employees")
def list_employees():
    return render_template("employee/list_employees.html")


@app.route("/cars")
def list_cars():
    cars = get_all_cars()
    if session.get("USERNAME", None) is not None:
        user = session["USERNAME"]
        if is_admin_user(user):
            return render_template("employee/cars.html", cars=cars)
        else:
            flash("You do not have permission to view this page", "warning")
    else:
        return redirect(url_for("employee_sign_in"))


@app.route("/add-car", methods=['GET', 'POST'])
def add_car():
  if user_has_employee_permission():
    if request.method == 'POST':

        req = request.form
        registration_num = req.get("registration_num").upper()
        make = req.get("make")
        model = req.get("model").capitalize()
        manufacturing_year = req.get("manufacturing_year")
        seating_capacity = req.get("seating_capacity")
        rental_per_day = req.get("rental_per_day")

        car_img = request.files['car_img']
        car_img_filenname = car_img.filename


        # # check registration number is unique
        registration_num_in_db = get_registration_num_in_db_as_list()
        if registration_num in registration_num_in_db:
            flash("Registration number already exists", "danger")
            return redirect(request.url)
        
        if car_img_filenname is not None:
            car_img_path = f"static/img/car_img/{car_img_filenname}"

        # insert car info to Cars table
        insert_into_cars(registration_num, make, model,
                          manufacturing_year, seating_capacity, rental_per_day, car_img_path)
        flash("You have successfully added the car!", "success")
        return redirect(url_for("admin_dashboard", username=session["USERNAME"]))

  return render_template("employee/add_car.html",
                    MAKES=MAKES, SEATING_CAPACITY=SEATING_CAPACITY,\
                    MANUFACTURING_YEAR=MANUFACTURING_YEAR)


@app.route("/delete-car", methods=['GET', 'POST'])
def delete_car():
  if user_has_employee_permission():
    if request.method == 'POST':
        req = request.form
        registration_num = req.get("registration_num").upper()

        # delete car from to Cars table
        delete_car_by_registration_num(registration_num)
        flash("You have successfully delete the car!", "success")
        return redirect(url_for("list_cars"))
    return render_template("employee/delete_car.html")


@app.route("/update-car", methods=['GET'])
def fetch_registration_num():
    if user_has_employee_permission():

      if request.method == 'GET':
        registration_num = request.args.get("registration_num")
        if registration_num is not None:
            car_details = get_car_by_registration_num(registration_num)
            if car_details is not None:
                return render_template("employee/update_car.html", car_details=car_details)
            else:
                flash("Car not found", "danger")
                return redirect(url_for("list_cars"))
        else:
            flash("Car registration number not provided", "danger")
            return redirect(url_for("list_cars"))
    else:
        return redirect(url_for("employee_sign_in"))


@app.route("/update-car", methods=['POST'])
def update_car():
    if user_has_employee_permission():
      if request.method == "POST":
        req = request.form
        reg_num = req.get("registration_num")
        seating_capacity = req.get("seating_capacity")
        rental_per_day = req.get("rental_per_day")

        # print(reg_num)
        # print(seating_capacity)
        # print(rental_per_day)

        update_car_info(seating_capacity, rental_per_day, reg_num)
        flash("You have successfully update car information", "success")
        return redirect(url_for("admin_dashboard",username=session["USERNAME"]))


@app.route("/staff")
def staff():
    if not user_has_admin_permission():
        flash("You do not have permission to view this page", "warning")
        return redirect(url_for("employee_sign_in"))

    else:
        employees = get_all_employees()
        
        staff_username = None
        
        # print(employees)
        return render_template("employee/staff.html", employees = employees) 


@app.route("/add-staff", methods=['GET', 'POST'])
def add_staff():
  if not user_has_admin_permission():
      flash("You do not have permission to view this page.", "warning")
      return redirect(url_for("employee_sign_in"))
  else:
    if request.method == 'POST':
        req = request.form
        is_admin = 0
        initial_pass = "staffpass123"

        fname = req.get("fname").capitalize()
        lname = req.get("lname").capitalize()
        birthday_str = req.get("birthday")
        if birthday_str is not None:
            birthday_dt = datetime.strptime(birthday_str,"%Y-%m-%d")

        provided_staff_username = req.get("username")
        staff_addr = req.get("address")
        staff_email = req.get("email")
        staff_phone = req.get("phone")

        # # check staff user number is unique
        employee_in_db = get_employee_by_username(provided_staff_username)
        if employee_in_db is not None:
            flash("staff username already exists", "warning")
            return redirect(request.url)
        else:
         # insert staff info to Employees table
            insert_into_employees(fname, lname, birthday_dt, provided_staff_username, staff_addr, staff_email, staff_phone, is_admin, initial_pass)
            flash("You have successfully added a new staff!", "success")
        return redirect(url_for("staff"))

    return render_template("employee/add_staff.html")


@app.route("/update-staff", methods=['GET'])
def fetch_staff_username():
    if user_has_admin_permission():
        staff_username = request.args.get("staff_username")
        print(staff_username)
        if staff_username is not None:
            staff_details = get_employee_by_username(staff_username)
            print(staff_details)
            return render_template("employee/update_staff.html", staff_username=staff_username, staff_details=staff_details)
        else:
            flash("Staff user name is not provided", "warning")    
        return redirect(url_for("staff"))
    
    else:
        flash("You don't have the permission to view this page.", "warning")
        return redirect(url_for("home"))


@app.route("/update-staff", methods=['POST'])
def update_staff():
    if user_has_admin_permission():
        req = request.form
        staff_username = req.get("staff_username")           
        birthday_str = req.get("birthday")
        staff_addr = req.get("address")
        if birthday_str:
            birthday_dt = datetime.strptime(birthday_str,"%Y-%m-%d")
            
            update_staff_info(birthday_dt, staff_addr, staff_username)
            flash("You have successfully update car information", "success")
        return redirect(url_for("staff"))
    else:
        flash("You don't have permission to view this page.", "warning")
        return redirect("/home")


@app.route("/delete-staff", methods=['GET', 'POST'])
def delete_staff():
    if user_has_employee_permission():
      if request.method == "GET":
        target_staff = request.args.get("staff_username")
        delete_staff_by_username(target_staff)
    flash("You have successfully delete the stuff info", "success")
    return redirect(url_for("staff"))



@app.route("/staff-edit-profile", methods=['GET'])
def fetch_staff_username_and_render_edit_template():
    staff_username = request.args.get("username")
    staff_details = get_employee_by_username(staff_username)
    print(staff_username)
    if user_has_staff_permission():
        return render_template("employee/staff_edit_profile.html", username = staff_username, details=staff_details)



@app.route("/staff-edit-profile", methods=['POST'])
def staff_edit_profile():
    if user_has_staff_permission():
        req = request.form
        staff_username = req.get("username")           
        birthday_str = req.get("birthday")
        
        # get original details from database, if no change made, keep the original data in database
        staff_details = get_employee_by_username(staff_username)

        # format address info to populate database Customer table Address collumn
        address = req.get("address")
        city = req.get("city")
        postcode = req.get("postcode")

        texts_in_address = [address, city, postcode]
        valid_text_in_address = [text for text in texts_in_address if text]

        if len(valid_text_in_address) == 0:
            formatted_address == staff_details[5]
        else:
            formatted_address = ", ".join(valid_text_in_address)
        
        birthday_dt = None
        if birthday_str:
            birthday_dt = datetime.strptime(birthday_str,"%Y-%m-%d")

        
        print(staff_username)
        print(birthday_dt)
        print(formatted_address)
            
        update_staff_info(birthday_dt, formatted_address, staff_username)
        flash("You have successfully update information", "success")
        return redirect(url_for("staff_dashboard", username=session['USERNAME']))
    else:
        flash("You don't have permission to view this page.", "warning")
        return redirect("/home")


@app.route("/staff-reset-pass", methods=['GET', 'POST'])
def staff_reset_pass():
    if user_has_staff_permission and request.method == 'GET':
        staff_username = request.args.get("username")
        staff_details = get_employee_by_username(staff_username)
        return render_template("employee/staff_reset.html", username = staff_username, details=staff_details)

    elif user_has_staff_permission and request.method == 'POST':
        req = request.form
        staff_username = req.get("username")           
        new_pass = req.get("new_pass")
        comfirm_pass = req.get("comfirm_pass")

        #validate
        print(staff_username)
        print(new_pass)

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
                #check if new pass is different from the old_pass
                employee_account = get_employee_by_username(staff_username)
                if employee_account is None:
                    flash("Staff user not found", "warning")
                    return redirect(url_for("staff_dashboard", username=session["USERNAME"]))
                
                old_pass = employee_account[9]
                if new_pass == old_pass:
                    flash("New password should be different from the old password", "warning")
                else:
                    staff_change_pass(new_pass, staff_username)
                    flash("You've successfully changed your password", "success")
                    return redirect(url_for("staff_dashboard", username=session["USERNAME"]))



@app.route("/staff-view-customer-list", methods=['GET'])
def staff_view_customer_list():
    if not user_has_staff_permission():
        flash("You don't have permission to view this page", "danger")
        return redirect(url_for("employee_sign_in"))
    
    else:
        all_customers = get_all_customers()
        return render_template("employee/staff_view_customer_list.html", all_customers=all_customers)
        

@app.route("/staff-view-customer-profile", methods=['GET'])
def staff_view_customer_profile():
    if not user_has_staff_permission():
        flash("You don't have permission to view this page", "danger")
        return redirect(url_for("employee_sign_in"))

    else:
        username = request.args.get("username")
        customer_details = get_customer_by_username(username)
        return render_template("employee/staff_view_customer_profile.html", customer_details=customer_details)
        

@app.route("/staff-view-car-list", methods=['GET'])
def staff_view_car_list():
    if not user_has_staff_permission():
        flash("You don't have permission to view this page", "danger")
        return redirect(url_for("employee_sign_in"))
    
    else:
        cars = get_all_cars()
        return render_template("employee/staff_view_car_list.html", cars=cars)
    


@app.route("/staff-add-car", methods=['GET','POST'])
def staff_add_car():
    if not user_has_staff_permission():
        flash("You don't have permission to view this page", "danger")
        return redirect(url_for("employee_sign_in"))
    else:
        if request.method == "POST":
            req = request.form
            registration_num = req.get("registration_num").upper()
            make = req.get("make")
            model = req.get("model").capitalize()
            manufacturing_year = req.get("manufacturing_year")
            seating_capacity = req.get("seating_capacity")
            rental_per_day = req.get("rental_per_day")

            # # check registration number is unique
            registration_num_in_db = get_registration_num_in_db_as_list()
            if registration_num in registration_num_in_db:
                flash("Registration number already exists", "danger")
                return redirect(request.url)


            # insert car info to Cars table
            insert_into_cars(registration_num, make, model,
                            manufacturing_year, seating_capacity, rental_per_day)
            flash("You have successfully added the car!", "success")
            return redirect(url_for("staff-view-car-list", username=session["USERNAME"]))

    return render_template("employee/staff-add-car.html",\
                        MAKES=MAKES, SEATING_CAPACITY=SEATING_CAPACITY,\
                        MANUFACTURING_YEAR=MANUFACTURING_YEAR)



@app.route("/staff-delete-car", methods=['GET','POST'])
def staff_delete_car():
        if not user_has_staff_permission():
            flash("You don't have permission to view this page", "danger")
            return redirect(url_for("employee_sign_in"))
        else:
            if request.method == 'GET':
                registration_num = request.args.get("registration_num").upper()

                # delete car from to Cars table
                delete_car_by_registration_num(registration_num)
                flash("You have successfully delete the car!", "success")
                return redirect(url_for("staff_view_car_list"))



@app.route("/staff-update-car", methods=['GET', 'POST'])
def staff_update_car():
    if request.method == "GET":
        registration_num = request.args.get("registration_num")
        car_details = get_car_by_registration_num(registration_num)
        
        return render_template("employee/staff_update_car.html", car_details=car_details,registration_num=registration_num)
    
    elif request.method == "POST":
        req = request.form
        reg_num = req.get("registration_num")
        seating_capacity = req.get("seating_capacity")
        rental_per_day = req.get("rental_per_day")

        update_car_info(seating_capacity, rental_per_day, reg_num)
        flash("You have successfully update car information", "success")
        return redirect(url_for("staff_view_car_list"))







    
    
