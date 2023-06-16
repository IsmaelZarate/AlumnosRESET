create database servicioAlumno ;
use servicioAlumno;

create table carreras(
idCarrera int, 
nombre varchar(200),
siglas varchar(10),
creditos varchar(20),
plan varchar(20),
especialidad varchar(200),
estatus varchar(20),
constraint pk_carreras primary key (idCarrera)
);
DROP TABLE carreras;

delete from carreras;
delete from carreras where id=2;
insert into carreras values (1,"Ing. en Sistemas Computacionales", "ISC", "260","ISC-204-1010","Full-Stack","Activo");
insert into carreras values (2,"Gestion", "IGE", "260","IGE-204-1010","Administracion","Activo");

create table Alumno (
idAlumno int ,
nombre varchar(200),
anioIngreso varchar(30),
anioEgreso varchar(30),
sexo varchar(200),
telefono varchar(20),
correo varchar(200),
passwords varchar(20),
nControl varchar(10),
tipo varchar(50),
estatus varchar(50),
idCarrera int ,
constraint pk_idAlumno primary key (idAlumno),
foreign key (idCarrera) references carreras(idCarrera)
);
ALTER TABLE Alumno
ADD CONSTRAINT fk_carrerass
FOREIGN KEY (idCarrera) REFERENCES carreras(idCarrera);

use servicioalumno;
create table notificaciones(
id int,
mensaje varchar(200),
correo_destino varchar(200),
idAlumno int,
idCarrera int
);
alter table notificaciones
add constraint fk_carre_notificacion FOREIGN KEY (idCarrera) REFERENCES carreras(idCarrera);
alter table notificaciones
add constraint fk_alumno_notificacion FOREIGN KEY (idAlumno) REFERENCES Alumno(idAlumno);

ALTER TABLE Alumno
ADD INDEX idx_carreras_idCarrera (idCarrera);
select * from Alumno;
insert into Alumno values (1,"Miguel Martinez","2019","Proximamente", "Macho","3511568719","michelan441@gmail.com", "Pichula", "19010376","Alumno","Activo",1);
insert into Alumno values (2,"Benito Mendez","2019","Proximamente jiji", "Macho","351316513","benito@gmail.com", "Hola.123", "19010377","Alumno","Activo",2);
insert into Alumno values (3,"Jenifer","hoy","2026", "hembra","3511555050","Jenif@gmail.com", "123.Hola", "19010380","Alumno","Activo",1);