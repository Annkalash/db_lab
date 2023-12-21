CREATE OR REPLACE FUNCTION get_cat()
RETURNS TABLE (
                cat_id INTEGER ,
				name_cat VARCHAR
            ) AS $$
BEGIN
    RETURN QUERY (SELECT * FROM medic.categories );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_med_cat(in_cat INTEGER)
RETURNS TABLE (
    name_m VARCHAR,
    amount INTEGER
) AS $$
BEGIN
    RETURN QUERY SELECT name_medic, quantity
                 FROM medic.medicines
                 WHERE medic.medicines.category_id = in_cat;
END;
$$ LANGUAGE plpgsql;
