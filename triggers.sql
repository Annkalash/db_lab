CREATE OR REPLACE FUNCTION update_quantity()
   RETURNS TRIGGER AS
$$
BEGIN
   UPDATE medic.medicines
   SET quantity = quantity - NEW.amount_used
   WHERE med_id = NEW.medicine_id;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER usage_trigger
AFTER INSERT ON medic.writing
FOR EACH ROW
EXECUTE FUNCTION update_quantity();

