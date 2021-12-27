create table login(
	id int not null auto_increment,
	`user` varchar(30) not null unique,
    passwd text not null,
    primary key (id)
)default charset = utf8;

alter table login
modify user varchar(100);
