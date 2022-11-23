CREATE OR REPLACE FUNCTION to_seconds(t text)
  RETURNS integer AS
$BODY$
DECLARE
    hs INTEGER;
    ms INTEGER;
    s INTEGER;
BEGIN
    SELECT (EXTRACT( HOUR FROM  t::time) * 60*60) INTO hs;
    SELECT (EXTRACT (MINUTES FROM t::time) * 60) INTO ms;
    SELECT (EXTRACT (SECONDS from t::time)) INTO s;
    SELECT (hs + ms + s) INTO s;
    RETURN s;
END;
$BODY$
  LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION to_time_notation(t float)
  RETURNS text AS
$BODY$
DECLARE
    total_minutes FLOAT;
    decimal_seconds INTEGER;
    total_seconds INTEGER;
BEGIN
    SELECT t / 60 INTO total_minutes;
    SELECT (ROUND(total_minutes, 2) - CAST(total_minutes AS INT)) * 100 INTO decimal_seconds;
    SELECT decimal_seconds * 60 INTO decimal_seconds;
    RETURN CONCAT(total_minutes, ':', total_seconds);
END;
$BODY$
  LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION is_blind(i_map_id int, i_side text, i_rotation int, i_role text)
  RETURNS boolean AS
$BODY$
DECLARE
    opposite_rotation INTEGER;
BEGIN
    SELECT pick_rotation FROM aux_view WHERE aux_view.map_id = i_map_id AND aux_view.side != i_side AND aux_view.role = i_role INTO opposite_rotation;
    IF i_side = 'blue' THEN
        IF i_rotation > opposite_rotation THEN
            RETURN FALSE;
        END IF;
        IF i_rotation = opposite_rotation THEN
            RETURN TRUE;
        END IF;
        RETURN TRUE;
    END IF;
    IF i_side = 'red' THEN
        IF i_rotation < opposite_rotation THEN
            RETURN TRUE;
        END IF;
        RETURN FALSE;
    END IF;
END;
$BODY$
  LANGUAGE 'plpgsql';
