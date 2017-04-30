# script for MySQL

## basic config

### 1 创建一个新的库之后，先查看当前各个选项的字符编码形式
create database 库名(tesla);
必须先选中库，才能改字符编码：
use 库名（tesla）;
show variables like'%char%';

### 2 设置（临时）
set character_set_****=utf8;  (****为对应的名)

### 3 完成后再建库、建表
mysql> show variables like'%char%';
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | utf8                       |
| character_set_filesystem | utf8                       |
| character_set_results    | utf8                       |
| character_set_server     | utf8                       |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
8 rows in set (0.00 sec)

## user table：
create table user(
id int not NULL auto_increment,
username varchar(16) not NULL,
password varchar(16) not NULL,
nickname varchar(32) not NULL,
email varchar(32) not NULL,
regtime datetime not NULL,
PRIMARY KEY (id)
);

用户ID改成从某个数开始自增：
alter table user auto_increment=1000;

注册时间在后端实现：
insert into user(username, password, nickname, email, regtime) values("wj", "123", "特斯拉", "wujian@github.com", now());
不得不写一句，curtime()



用户表：
ID
用户名
密码
邮箱
注册时间

##  post table：
create table post(
id int not NULL auto_increment,
title varchar(32) not NULL,
author varchar(16) not NULL,
text text not NULL,
posttime datetime not NULL,
tag varchar(16) not NULL,
PRIMARY KEY (id)
);

alter table post auto_increment=1000;

投递post表里，tag的思考：
出于方便存储、方便前端使用的考虑，决定每篇文章只定一个tag。这样可以直接存储，省下工作量，可以快速上线，
前端投稿时做限制，只能选一个标签tag。搜索时，则可以直接在数据库查询关键字。
后期如果有更强大的需求可以再优化此处。
搜索还可以用这个：
select title from article where text like "%微信%";

[ ] 需要在前端限制标题长度、文章长度

## video table:
create table math(
id int not NULL auto_increment,
title varchar(32) not NULL,
info varchar(256) not NULL,
url varchar(256) not NUll,
tag varchar(16) not NULL,
PRIMARY KEY (id)
);

alter table math auto_increment=10000;

insert into math(title, info, url, tag) values("数学基础课2", "适合初中学生观看，语言为英语。", "http://7xshru.com1.z0.glb.clouddn.com/video/2.mp4", "数学");

# Tensor Part

## user table

create table tuser(
id int not NULL auto_increment,
username varchar(32) not NULL,
password varchar(16) not NULL,
email varchar(32) not NULL,
regtime datetime not NULL,
PRIMARY KEY (id)
);
alter table post auto_increment=9000;

测试
insert into tuser(username, password, email, regtime) values("wj", "123", "wujian@github.com", now());
