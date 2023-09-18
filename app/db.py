from app import connect
import mysql.connector

# print("import done - establishing connection")

conn = mysql.connector.connect(user=connect.dbuser,
                               password=connect.dbpass,
                               host=connect.dbhost,
                               database=connect.dbname,
                               autocommit=True)
# print(f"connect_to_mysql_database done - {conn}")


# functions for database
def get_cursor():
    global conn # allows the function to redefine the global varaible conn.
    if not conn.is_connected():
        conn = mysql.connector.connect(user=connect.dbuser,
                                       password=connect.dbpass,
                                       host=connect.dbhost,
                                       database=connect.dbname,
                                       autocommit=True)
    cursor = conn.cursor()
    return cursor

def get_all_customers():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM Customers')
    all_customers = cursor.fetchall()
    return all_customers


def get_customer_by_username(username):
    cursor = get_cursor()
    cursor.execute('SELECT * FROM Customers WHERE username = %s', (username,))
    cusomer = cursor.fetchone()
    cursor.close()
    return cusomer

def create_a_new_customer(first_name, last_name, username, address, email, phone_number, password):
    cursor = get_cursor()
    cursor.execute(
        'INSERT INTO Customers \
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)',\
        (first_name, last_name, username, address, email, phone_number, password))
    cursor.close()


def get_all_employees():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM Employees')
    all_employees = cursor.fetchall()
    return all_employees


def get_employee_by_username(username):
    cursor = get_cursor()
    cursor.execute('SELECT * FROM Employees WHERE username = %s', (username,))
    employee = cursor.fetchone()
    cursor.close()
    return employee



def get_all_cars():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM Cars')
    cars = cursor.fetchall()
    cursor.close()
    return cars


def insert_into_cars(registration_num, make, model, manufacturing_year, seating_capacity, rental_per_day, car_img):
    cursor = get_cursor()
    sql_query = """
    INSERT INTO Cars (registration_num, make, model, manufacturing_year, seating_capacity, rental_per_day, car_img)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(sql_query, (registration_num, make, model, manufacturing_year, seating_capacity, rental_per_day, car_img))


def get_car_by_registration_num(registration_num):
    cursor = get_cursor()
    sql_query = 'SELECT * FROM Cars WHERE registration_num = %s'
    # need to pass a single tuple value, using ,
    cursor.execute(sql_query, (registration_num,))
    car_detail_in_db = cursor.fetchone()
    return car_detail_in_db


def delete_car_by_registration_num(registration_num):
    cursor = get_cursor()
    sql_query = "DELETE FROM Cars WHERE registration_num = %s"
    cursor.execute(sql_query,(registration_num,))


def delete_customer_by_username(customer_username):
    cursor = get_cursor()
    sql_query = "DELETE FROM Customers WHERE username = %s"
    cursor.execute(sql_query,(customer_username,))


def delete_staff_by_username(staff_username):
    cursor = get_cursor()
    sql_query = "DELETE FROM Employees WHERE username = %s"
    cursor.execute(sql_query,(staff_username,))



def update_car_info(seating_capacity, rental_per_day, registration_num, car_img):
    cursor = get_cursor()
    sql_query = "UPDATE Cars SET seating_capacity = %s, rental_per_day = %s WHERE registration_num = %s"
    cursor.execute(sql_query, (seating_capacity, rental_per_day, registration_num, car_img))


def update_customer_info(new_address, customer_username):
    cursor = get_cursor()
    sql_query = "UPDATE Customers SET cust_addr = %s WHERE username = %s"
    cursor.execute(sql_query, (new_address, customer_username))
    

def insert_into_employees(fname, lname, birthday, username, staff_addr, staff_email, staff_phone, is_admin, staff_pass):
    cursor = get_cursor()
    sql_query = """
    INSERT INTO Employees (fname, lname, birthday, username, staff_addr, staff_email, staff_phone, is_admin, staff_pass)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(sql_query, (fname, lname, birthday, username, staff_addr, staff_email, staff_phone, is_admin, staff_pass))


def update_staff_info(birthday, staff_address, username):
    cursor = get_cursor()
    sql_query = "UPDATE Employees SET birthday = %s, staff_addr = %s WHERE username = %s"
    cursor.execute(sql_query,(birthday, staff_address, username))


def staff_change_pass(new_pass, staff_username):
    cursor = get_cursor()
    sql_query = "UPDATE Employees SET staff_pass = %s WHERE username = %s"
    cursor.execute(sql_query,(new_pass, staff_username))


def cust_reset_pass(new_pass, customer_username):
    cursor = get_cursor()
    sql_query = "UPDATE Customers SET cust_pass = %s WHERE username = %s"
    cursor.execute(sql_query,(new_pass, customer_username))



def customer_edit_profile_in_db(cust_addr, cust_phone, username):
    cur = get_cursor()
    sql = "UPDATE Customers SET cust_addr = %s, cust_phone = %s WHERE username = %s"
    cur.execute(sql,(cust_addr, cust_phone, username))


def car_is_available(registration_num):
    car_is_available = False

    cur = get_cursor()
    sql = """
        select
            c.cust_id, 
            c.username,
            r.rental_id,
            r.is_returned,
            ca.car_id,
            ca.registration_num
        from
            Customers AS c
        inner join
            Rentals AS r ON c.cust_id = r.cust_id
        inner join
            Cars AS ca ON r.car_id = ca.car_id
        where
            registration_num = %s
    """
    cur.execute(sql, (registration_num,))
    rental = cur.fetchone()

    if rental is None:
        car_is_available = True
        return car_is_available
    else:
        if rental[3] == 1:
            car_is_available = True
            return car_is_available
        else:
            car_is_available = False
            return car_is_available
            





