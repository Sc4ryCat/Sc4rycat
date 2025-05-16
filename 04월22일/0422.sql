use mytest



create table comments(
	id int identity(1,1) primary key,
	content nvarchar(max) null
);

select * from comments

insert into comments (content) values ('test')


delete from comments;


