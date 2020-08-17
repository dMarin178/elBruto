--1
--No usamos PROCEDURE porque no venia integrado con la version de postgres que tenemos instalada
CREATE OR REPLACE FUNCTION  update_nivel(userName VARCHAR)
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

