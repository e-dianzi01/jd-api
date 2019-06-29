create database 91_api_db;
use 91_api_db;
create table app_user(
id integer primary key auto_increment,
user_name varchar(50) unique,
auth_string varchar(200),
nick_name varchar(50),
phone varchar(15), note text);


