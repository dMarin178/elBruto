--1
--No usamos PROCEDURE porque no venia integrado con la version de postgres que tenemos instalada
CREATE OR REPLACE FUNCTION  update_nivel(userName VARCHAR) RETURNS VOID
AS
$$
DECLARE
    nivel_actual avatar.nivel%TYPE;
    nuevo_nivel avatar.nivel%TYPE;
    puntosExp avatar.ptosexp%TYPE;
BEGIN
    puntosExp := (SELECT a.ptosexp FROM avatar a WHERE a.nick = userName);
    nivel_actual := (SELECT a.nivel FROM avatar a WHERE a.nick = userName);
    IF (puntosExp>150) THEN
        nuevo_nivel := ceil((puntosExp-100)/50)+1;
        IF (nuevo_nivel <> nivel_actual) THEN
            UPDATE avatar SET nivel = nuevo_nivel WHERE nick = userName;
	    END IF;
    END IF;
EXCEPTION
    WHEN plpgsql_error THEN
        RAISE NOTICE 'error PLPGSQL_ERROR';
    COMMIT;
END;
$$
LANGUAGE plpgsql;


--2
CREATE OR REPLACE FUNCTION jugadorToxico (username varchar) RETURNS BOOLEAN
AS
$$
DECLARE
	aux jugador.nick%TYPE;
BEGIN
	SELECT j.nick INTO aux
	FROM jugador j, avatar av
	WHERE j.nick = username AND cantreportes > 15 AND nivel > 9;
	IF aux IS NOT NULL THEN
		RETURN TRUE;
	ELSE
		RETURN FALSE;
	END IF;
END;
$$
LANGUAGE plpgsql

--3
CREATE OR REPLACE FUNCTION porcentajeToxico () RETURNS NUMERIC
AS $$
DECLARE
	cantTotal INTEGER;
	cantToxicos INTEGER:=0;
	porcentaje NUMERIC;
	toxicos CURSOR FOR 
		SELECT j.nick
		FROM jugador j ,avatar av
		WHERE j.nick = av.nick AND j.cantreportes > 15 AND av.nivel > 9;
BEGIN
	cantTotal :=(SELECT COUNT(*) cantTotal
	FROM jugador);
	
	FOR record IN toxicos LOOP
		cantToxicos := cantToxicos +1;
	END LOOP;
	porcentaje := cantToxicos::numeric/cantTotal::numeric*100;
	RETURN porcentaje;
END;
$$
LANGUAGE plpgsql

--4
CREATE OR REPLACE FUNCTION topNiveles () RETURNS TABLE(nick varchar,nivel integer)
AS $$
BEGIN
	RETURN QUERY
    SELECT nick,nivel
	FROM avatar
	ORDER BY ptosexp DESC
	LIMIT 3;
END;
$$
LANGUAGE plpgsql


--Entrega 2

--1 Trnasformar un jugador en administrador 
--Tuvimos que agregar constraints para la eliminacion de el avatar
ALTER TABLE jugador
ADD CONSTRAINT nick 
FOREIGN KEY (nick) 
REFERENCES Avatar (nick) ON DELETE CASCADE
CREATE OR REPLACE FUNCTION tranformarEnAdmin (nickJugador varchar) RETURNS VOID
AS
$function$

--Procedimiento
CREATE OR REPLACE FUNCTION tranformarEnAdmin (nickJugador varchar) RETURNS VOID
AS
$function$
DECLARE
	nombresA administrador.nombres%TYPE;
	apellidopA administrador.apellidop%TYPE;
	apellidomA administrador.apellidom%TYPE;
	correoA administrador.correo%TYPE;
	contraseñaA administrador.contraseña%TYPE;
	paisA administrador.pais%TYPE;
BEGIN
	SELECT nombres, apellidop, apellidom, correo, contraseña, pais
	INTO nombresA, apellidopA, apellidomA, correoA, contraseñaA, paisA
	FROM jugador
	WHERE jugador.nick = nickJugador;
	
	INSERT INTO Administrador(nick,nombres,apellidoP,apellidoM,correo,contraseña,pais)
		VALUES(nickJugador,nombresA,apellidopA,apellidomA,correoA,contraseñaA,paisA);
		
	DELETE 
	FROM avatar
	WHERE avatar.nick = nickJugador;
END;
$function$
LANGUAGE plpgsql


--2 Bloque PL en donde para cada jugador que tenga más de 10 reportes, restarle 5 puntos de vida a su Avatar (Esto debe guardarse en la base de datos)

CREATE OR REPLACE FUNCTION checkToxic() RETURNS VOID
AS
$$
BEGIN
	UPDATE avatar
	SET vida = vida - 5
	WHERE nick = (SELECT nick
					FROM jugador
					WHERE cantreportes > 10);
END;
$$
lANGUAGE plpgsql

--3 Crear un Trigger para que cuando se añada un administrador, corroborar que no tenga ningún avatar asociado. Si lo tiene,
-- se deben eliminar todos los registros de su Avatar y su perfil de jugador. 

CREATE OR REPLACE FUNCTION nuevoAdminFunc() returns trigger as
$$
BEGIN 
	delete from avatar where avatar.nick = new.nick;
END;
$$
LANGUAGE plpgsql

CREATE TRIGGER nuevoAdministrador 
AFTER INSERT
ON administrador
EXECUTE PROCEDURE nuevoAdminFunc();

--4 Crear un Trigger que se ejecute cada vez que se actualice información en la experiencia de un avatar (cuando gane experiencia), 
--y que actualice el nivel del personaje en caso de que el nivel que tiene no corresponda al de la experiencia que tiene (similar al procedimiento 1).

CREATE OR REPLACE FUNCTION  update_LVL() returns trigger
AS
$$
DECLARE
	nuevo_nivel avatar.nivel%TYPE;
BEGIN
    IF (new.ptosexp>150) THEN
        nuevo_nivel := ceil((new.ptosexp-100)/50)+1;
    END IF;
	UPDATE avatar SET nivel = nuevo_nivel where avatar.nick = new.nick;
EXCEPTION
    WHEN plpgsql_error THEN
        RAISE NOTICE 'error PLPGSQL_ERROR';
    COMMIT;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER actualizarNivel
AFTER UPDATE
ON avatar
EXECUTE PROCEDURE update_lvl();


--5 Crear un Trigger que se ejecute cada vez que se haga un reporte. Si un jugador tiene más de 20 reportes, este automáticamente es baneado.
CREATE OR REPLACE FUNCTION  updatenivel() returns trigger
AS
$$
DECLARE
	nuevo_nivel avatar.nivel%TYPE;
BEGIN
	IF new.cantreportes > 19 THEN
		UPDATE jugador
	    SET ban_S_N = TRUE
		WHERE jugador.nick = old.nick;
	END IF;
    COMMIT;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER banAutomatico
AFTER UPDATE OF cantreportes
ON jugador EXECUTE PROCEDURE updatenivel();

