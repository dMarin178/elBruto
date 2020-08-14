CREATE DATABASE Gutierrez_Marin;

create table Jugador(nick varchar(30) not null primary key
					,nombres varchar(30) not null
					,apellidoP varchar(30) not null
					,apellidoM varchar(30) not null
					,correo varchar(50) not null
					,contraseña varchar(30) not null
					,pais varchar(30) not null
					,cantReportes integer
					,ban_S_N boolean
					,ultimoLogin date not null
					,peleasDisponibles integer not null);

create table Administrador(nick varchar(30) not null primary key
					,nombres varchar(30) not null
					,apellidoP varchar(30) not null
					,apellidoM varchar(30) not null
					,correo varchar(50) not null
					,contraseña varchar(30) not null
					,pais varchar(30) not null);

create table Avatar(nick varchar(30) references jugador(nick)
				   ,ataque integer not null
				   ,velocidad integer not null
				   ,vida integer not null
				   ,ptosExp integer
				   ,primary key(nick));

                
insert into Administrador(nick,nombres,apellidoP,apellidoM,correo,contraseña,pais)
values
('dinoco','Dino Bastian','Marin','Diaz','dinomarindiaz178@gmail.com','dino123','Chile'),
('dio','Dio','Brando','Muñoz','hell@gmail.com','123','Peru');

insert into Jugador(nick,nombres,apellidoP,apellidoM,correo,contraseña,pais,cantReportes,ban_S_N,ultimoLogin,peleasDisponibles)
values
('JoJo','Joseph','Joestar','Muñoz','jojo@gmail.com','123','Bolivia',0,False,'2020-07-21',5),	
('zizu','Zinedine','Zidane','Rios','zizu@gmail.com','123','Francia',0,False,'2020-07-21',5),
('as7','Alexis','Sanchez','Klose','jojo@gmail.com','123','Chile',0,False,'2020-07-21',5),	
('pitbull','Gary','Medel','Medel','zizu@gmail.com','123','Chile',0,False,'2020-07-21',5),
('perking','arturo','vidal','vidal','arturo@gmail.com','123','Chile',0,False,'2020-07-19',2);
insert into Avatar(nick,ataque,velocidad,vida,ptosExp)
values
('JoJo',3,5,20,0),
('zizu',4,4,18,0),
('as7',5,4,20,0),
('pitbull',6,3,13,0),
('perking',5,4,12,0);

					
