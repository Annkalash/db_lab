CREATE OR REPLACE FUNCTION add_to_use(
    name_med VARCHAR,
    amount INTEGER
)
RETURNS VOID AS $$
DECLARE
    medi_id INTEGER;
BEGIN
	SELECT med_id INTO medi_id FROM medic.medicines WHERE name_medic = name_med;
    INSERT INTO medic.writing(medicine_id,amount_used)
    VALUES (medi_id,amount);
END;
$$ LANGUAGE plpgsql;

--CREATE OR REPLACE FUNCTION show_table_writ()
--RETURNS TABLE
--            (
--                wri_id INTEGER ,
--          		am_used INTEGER,
--				name_med VARCHAR
--            ) AS $$
--BEGIN
--    RETURN QUERY (SELECT medic.writing.wr_id, medic.writing.amount_used, medic.medicines.name_medic FROM medic.writing
--				  JOIN medic.medicines ON medic.writing.medicine_id = medic.medicines.med_id );
--END;
--$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION show_table_writ()
RETURNS TABLE (
    wri_id INTEGER,
    am_used INTEGER,
    name_med VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT w.wr_id, w.amount_used, m.name_medic
    FROM medic.writing w
    JOIN medic.medicines m ON w.medicine_id = m.med_id;
END;
$$ LANGUAGE plpgsql;