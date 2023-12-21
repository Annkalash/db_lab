CREATE OR REPLACE FUNCTION get_ins()
RETURNS TABLE(
                ins_id INTEGER ,
				name_inst VARCHAR
            ) AS $$
BEGIN
    RETURN QUERY (SELECT * FROM medic.instructions );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_med_ins(in_ins INTEGER)
RETURNS TABLE (
				name_m VARCHAR,
				amount INTEGER
            ) AS $$
BEGIN
    RETURN QUERY (SELECT name_medic,quantity FROM medic.medicines WHERE medic.medicines.instruction_id = in_ins);
END;
$$ LANGUAGE plpgsql;