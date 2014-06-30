drop table if exists entries;
create table People(
	P_id integer primary key autoincrement,
	name varchar(10) not null,
	text text not null
);