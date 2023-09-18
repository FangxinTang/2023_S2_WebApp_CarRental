-- create database car_rental_DB;

-- use car_rental_DB;

-- create table Customers (
-- cust_id int not null auto_increment primary key,
-- fname varchar(50) not null,
-- lname varchar(50) not null,
-- username varchar(50) not null,
-- cust_addr varchar(255),
-- cust_email varchar(255) not null,
-- cust_phone varchar(50) not null,
-- cust_pass varchar(255) not null
-- ) auto_increment = 1001;

-- INSERT INTO Customers (fname, lname, username, cust_addr, cust_email, cust_phone, cust_pass)
-- VALUES
--   ('Alice', 'Johnson', 'user1', '42 Elm Street, Wellington', 'alice@example.com', '+64 9 123 4567', 'securepass123'),
--   ('Bob', 'Smith', 'user2', '123 Maple Ave, Auckland', 'bob@example.com', '+64 21 987 6543', 'password456'),
--   ('Emily', 'Williams', 'user3', '36 Green Road, Christchurch', 'emily@example.com', '+64 22 111 2222', 'securepass789'),
--   ('Michael', 'Brown', 'user4', '8 Blue Street, Dunedin', 'michael@example.com', '+64 27 333 4444', 'password987'),
--   ('Sophia', 'Taylor', 'user5', '14 Yellow Avenue, Hamilton', 'sophia@example.com', '+64 29 555 6666', 'pass123word');




-- create table Employees (
-- staff_id int not null auto_increment primary key,
-- fname varchar(50) not null,
-- lname varchar(50) not null,
-- birthday DATE,
-- username varchar(50) not null,
-- staff_addr varchar(255),
-- staff_email varchar(255) not null,
-- staff_phone varchar(50) not null,
-- is_admin tinyint not null default 0,
-- staff_pass varchar(255) not null
-- ) auto_increment = 1;


-- INSERT INTO Employees (fname, lname, birthday, username, staff_addr, staff_email, staff_phone, is_admin, staff_pass)
-- VALUES
--   ('Lisa', 'La', '2000-11-03', 'admin', '1 Victoria Street, Auckland', 'john@example.com', '+64 9 123 4577', 1, 'adminpass123'),
--   ('Jisoo', 'Flower', '2000-11-03', 'staff1', '9/2 Carr Street, Auckland', 'jisoo@example.com', '+64 9 123 4567', 0, 'staff1pass123'),
--   ('Rose','Park','2000-11-03', 'staff2', '115 Rayment Avenue, Christchurch', 'rose@example.com', '+64 27 933 6983', 0, 'staff2pass123'),
--   ('Jennie', 'Kim', '2000-11-03', 'staff3', '22 Queen Street, Wellington', 'jane@example.com', '+64 21 987 6543', 0, 'staff3pass123');




-- create table Cars(
-- car_id int not null auto_increment primary key,
-- registration_num varchar(100) not null,
-- make varchar(100) not null,
-- model varchar(100) not null,
-- manufacturing_year year not null,
-- seating_capacity int not null,
-- rental_per_day decimal(10,2) not null,
-- car_img varchar(255)
-- ) auto_increment=1;



-- INSERT INTO Cars (registration_num, make, model, manufacturing_year, seating_capacity, rental_per_day, car_img)
-- VALUES
--   ('ABC123', 'Toyota', 'Corolla', '2021', 5, 50.00, 'static/img/car_img/car_1.jpg'),
--   ('XYZ456', 'Honda', 'Civic', '2022', 5, 55.00, 'static/img/car_img/car_2.jpg'),
--   ('PQR789', 'Tesla', 'Model 3', '2023', 4, 80.00, 'static/img/car_img/car_3.jpg'),
--   ('LMN321', 'Mercedes-Benz', 'C-Class', '2021', 5, 70.00, 'static/img/car_img/car_4.jpg'),
--   ('DEF456', 'Toyota', 'Camry', '2022', 5, 53.00, 'static/img/car_img/car_5.jpg'),
--   ('GHI789', 'Honda', 'Accord', '2021', 5, 52.00, 'static/img/car_img/car_6.jpg'),
--   ('JKL123', 'Mercedes-Benz', 'E-Class', '2022', 5, 75.00, 'static/img/car_img/car_7.jpg'),
--   ('MNO056', 'Tesla', 'Model S', '2023', 4, 90.00, 'static/img/car_img/car_8.jpg'),
--   ('PQR689', 'Toyota', 'Rav4', '2021', 5, 60.00, 'static/img/car_img/car_9.jpg'),
--   ('STU123', 'Honda', 'CR-V', '2022', 5, 58.00, 'static/img/car_img/car_10.jpg'),
--   ('VWX456', 'Mercedes-Benz', 'GLC', '2023', 5, 85.00, 'static/img/car_img/car_11.jpg'),
--   ('YZA789', 'Tesla', 'Model X', '2021', 4, 95.00, 'static/img/car_img/car_12.jpg'),
--   ('BBC103', 'Toyota', 'Yaris', '2021', 2, 40.00, 'static/img/car_img/car_13.jpg'),
--   ('XYZ466', 'Honda', 'Fit', '2022', 4, 45.00, 'static/img/car_img/car_14.jpg'),
--   ('PQM789', 'Mercedes-Benz', 'A-Class', '2023', 2, 60.00, 'static/img/car_img/car_15.jpg'),
--   ('LQN321', 'Tesla', 'Model 3', '2021', 2, 80.00, 'static/img/car_img/car_16.jpg'),
--   ('DEA456', 'Toyota', 'Sienna', '2021', 7, 80.00, 'static/img/car_img/car_17.jpg'),
--   ('GXI789', 'Honda', 'Odyssey', '2022', 8, 90.00, 'static/img/car_img/car_18.jpg'),
--   ('JBL123', 'Mercedes-Benz', 'S-Class', '2023', 5, 150.00, 'static/img/car_img/car_19.jpg'),
--   ('MNO456', 'Tesla', 'Model X', '2021', 6, 120.00, 'static/img/car_img/car_20.jpg');





-- CREATE TABLE Rentals (
--   rental_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
--   cust_id INT NOT NULL,
--   car_id INT NOT NULL,
--   is_returned tinyint not null default 0,
--   FOREIGN KEY (cust_id) REFERENCES Customers(cust_id),
--   FOREIGN KEY (car_id) REFERENCES Cars(car_id)
-- )auto_increment = 101;

-- insert into Rentals (cust_id, car_id, is_returned)
-- values
-- (1002, 1, 0),
-- (1001, 2, 0),
-- (1003, 3, 1),
-- (1005, 19, 0)


