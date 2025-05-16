use mytest

create table personalInfo(
	ID int identity(1,1) primary key,
	Name nvarchar(50),
	Email nvarchar(100),
	Phone nvarchar(20),
	ssn nvarchar(20) -- ÁÖ¹Îµî·Ï¹øÈ£
);

insert into personalInfo(Name,Email,Phone,ssn) values
(N'È«±æµ¿1','1hong123@example.com','010-120-0000','741111-0123655'),
(N'È«±æµ¿2','2hong123@example.com','010-564-4879','458022-0123655'),
(N'È«±æµ¿3','3hong123@example.com','010-254','741111');

select * from personalInfo

create table partialinfo(
	id int identity(1,1) primary key,
	fullname nvarchar(50),
	emailaddress nvarchar(100)
);

insert into partialinfo (fullname,emailaddress) values
(N'±è¿µÈñ', 'younghee1@gmail.com'),
(N'¹ÚÁ¤¿ì', 'jungwoo@gmail.com'),
(N'È«»ó¿ø', '¾øÀ½');
select * from partialinfo