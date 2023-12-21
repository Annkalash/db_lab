CREATE OR REPLACE FUNCTION trunc_all()
RETURNS VOID
AS
$$
BEGIN
    TRUNCATE TABLE medic.writing CASCADE;
    TRUNCATE TABLE medic.medicines CASCADE;
    TRUNCATE TABLE medic.instructions CASCADE;
    TRUNCATE TABLE medic.categories CASCADE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clear_medicines()
RETURNS VOID AS $$
BEGIN
    DELETE FROM medic.medicines WHERE quantity = 0;
END;
$$ LANGUAGE plpgsql;