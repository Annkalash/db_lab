
CREATE OR REPLACE FUNCTION create_db()
RETURNS void AS
$$
BEGIN
        CREATE SCHEMA IF NOT EXISTS medic;
        DROP TABLE medic.instructions CASCADE;
        DROP TABLE medic.categories CASCADE;
        DROP TABLE medic.medicines CASCADE;
        DROP TABLE medic.writing CASCADE;
        CREATE TABLE IF NOT EXISTS medic.instructions
        (
          ins_id SERIAL NOT NULL PRIMARY KEY,
          name_inst VARCHAR(255) NOT NULL UNIQUE
        );

		CREATE TABLE IF NOT EXISTS medic.categories
        (
          cat_id SERIAL NOT NULL PRIMARY KEY,
          name_cat VARCHAR(255) NOT NULL UNIQUE
        );

		CREATE TABLE IF NOT EXISTS medic.medicines
        (
          med_id SERIAL NOT NULL PRIMARY KEY,
          name_medic VARCHAR(255) NOT NULL UNIQUE,
          dosage NUMERIC NOT NULL,
          category_id SERIAL NOT NULL REFERENCES medic.categories (cat_id) ON DELETE RESTRICT,
          quantity INTEGER NOT NULL CHECK (quantity>=0),
          instruction_id SERIAL NOT NULL REFERENCES medic.instructions (ins_id) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS medic.writing
        (
          wr_id SERIAL NOT NULL PRIMARY KEY,
          medicine_id SERIAL NOT NULL REFERENCES medic.medicines (med_id) ON DELETE RESTRICT,
          amount_used INTEGER NOT NULL
        );
END
$$ LANGUAGE plpgsql;

