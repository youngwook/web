drop table if exists user;
create table user (
    u_id integer primary key autoincrement,
    username varchar(20) not null,
    pwd varchar(20) not null
);

drop table if exists blog;
create table blog (
    b_id integer primary key autoincrement,
    title varchar not null,
    content text not null,
    u_id integer not null,
    time datetime not null
);

drop table if exists word;
create table word (
    w_id integer primary key autoincrement,
    content varchar(20) not null,
    who integer not null,
    whom integer not null,
    time datetime not null
);