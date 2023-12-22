CREATE OR REPLACE FUNCTION show_table_med()
RETURNS TABLE
            (
                med_id INTEGER,
          name_m VARCHAR,
          dosage NUMERIC ,
          cat VARCHAR ,
          quantity INTEGER ,
          ins VARCHAR
            ) AS $$
BEGIN
    RETURN QUERY (SELECT medic.medicines.med_id,
          medic.medicines.name_medic ,
          medic.medicines.dosage ,
          medic.categories.name_cat ,
          medic.medicines.quantity ,
          medic.instructions.name_inst
          FROM medic.medicines
				  JOIN medic.categories ON medic.medicines.category_id = medic.categories.cat_id
				 JOIN medic.instructions ON medic.medicines.instruction_id = medic.instructions.ins_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_to_medic(
    name_med VARCHAR,
	dosage_med NUMERIC,
	category_name VARCHAR,
	quantity_med INTEGER,
	instruction_name VARCHAR
)
RETURNS BOOLEAN AS $$
DECLARE
    categ_id INTEGER;
    instruct_id INTEGER;
BEGIN
    IF EXISTS (SELECT med_id FROM medic.medicines WHERE medic.medicines.name_medic = name_med) THEN
        RETURN FALSE;
    ELSE
        IF NOT EXISTS (SELECT 1 FROM medic.categories WHERE name_cat = category_name) THEN
            INSERT INTO medic.categories(name_cat)  VALUES ( category_name);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM medic.instructions WHERE name_inst = instruction_name) THEN
            INSERT INTO medic.instructions(name_inst) VALUES (instruction_name);
        END IF;
        SELECT cat_id INTO categ_id FROM medic.categories WHERE name_cat = category_name;
        SELECT ins_id INTO instruct_id FROM medic.instructions WHERE name_inst = instruction_name;
        INSERT INTO medic.medicines(name_medic, dosage, category_id, quantity,instruction_id)
        VALUES (name_med, dosage_med, categ_id, quantity_med,instruct_id);
        RETURN TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION dell_medic(name_med VARCHAR)
RETURNS BOOLEAN AS $$
BEGIN
    IF NOT EXISTS (SELECT med_id FROM medic.medicines WHERE name_medic = name_med) THEN
        RETURN FALSE;
    ELSE
        DELETE FROM medic.medicines WHERE name_medic = name_med;
        RETURN TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_medic(
    name_med VARCHAR
)
RETURNS BOOLEAN AS $$
BEGIN
    IF NOT EXISTS (SELECT med_id FROM medic.medicines WHERE medic.medicines.name_medic = name_med) THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;
