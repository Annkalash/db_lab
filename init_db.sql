CREATE EXTENSION IF NOT EXISTS dblink;

CREATE OR REPLACE FUNCTION public.f_create_db(dbname text)
  RETURNS void AS
$$
BEGIN
-- проверка на существование БД с таким же именем
IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN
   -- Возвращаем сообщение (не ошибку)
   RAISE NOTICE 'Database already exists';
ELSE
   PERFORM dblink_exec('dbname=' || current_database()|| ' hostaddr=127.0.0.1 port=5432 user=postgres password=123456789',
                      'CREATE DATABASE ' || quote_ident(dbname));

END IF;
END
$$ LANGUAGE plpgsql;