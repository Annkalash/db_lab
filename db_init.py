import psycopg2
import os
from pathlib import Path

def init_db():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='123456789' host='127.0.0.1'")
    cur = conn.cursor()

    with open('init_db.sql', 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        cur.execute("SELECT f_create_db('medichome')")
        conn.commit()

    with open('create_db.sql', 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        cur.execute("SELECT create_db()")

    with open('categories.sql', 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()

    with open('del.sql', 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()

    with open('instructions.sql', 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()

    with open('medicines.sql', 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()

    with open('triggers.sql', 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()

    with open('writing.sql', 'r') as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
        conn.commit()

    conn.close()

def db_connect() -> psycopg2._psycopg.connection:
    conn_params = {
        "host": "127.0.0.1",
        "port": 5432,
        "database": "postgres",
        "user": "postgres",
        "password": "123456789"
    }
    return psycopg2.connect(**conn_params)
def show_table_med() :
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute('select * FROM show_table_med()')
            result = cur.fetchall()
            return result
def show_table_writ():
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select * FROM show_table_writ()")
            result = cur.fetchall()
            return result
def get_cat() -> dict[str, int]:
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select * from get_cat()")
            result = cur.fetchall()
            return {item[0]: item[1] for item in result}

def get_med_cat(in_cat):
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("SELECT * from get_med_cat(%s::integer)", (in_cat,))
            result = cur.fetchone()
            return result
def get_ins() -> dict[str, int]:
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select * from get_ins()")
            result = cur.fetchall()
            return {item[0]: item[1] for item in result}
def get_med_ins(in_ins):
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select * from get_med_ins(%s::int)",(in_ins,))
            result = cur.fetchone()
            return result
def add_to_medic(name_med, dosage_med, category_name, quantity_med, instruction_name) -> bool:
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select add_to_medic(%s::varchar, %s::numeric,%s::varchar, %s::int,%s::varchar)",
                        (name_med, dosage_med, category_name, quantity_med, instruction_name))
            connect.commit()
            result = cur.fetchone()
            return result[0]
def add_to_use(name_med, quantity_med):
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select * FROM add_to_use(%s::varchar, %s::int)",
                        (name_med,  quantity_med))
            connect.commit()
def dell_medic(name_med):
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("SELECT * FROM dell_medic(%s::varchar)", (name_med,))
            result = cur.fetchone()
            connect.commit()
            return result[0]
def check_medic(name_med):
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select check_medic(%s::varchar)",(name_med))
            result = cur.fetchone()
            connect.commit()
            return result[0]
def ch_medic(name_med, dosage_med, category_name, quantity_med, instruction_name) -> bool:
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select dell_medic(%s::varchar)", (name_med))
            cur.execute("select add_to_medic(%s::varchar, %s::numeric,%s::varchar, %s::int,%s::varchar)",
                        (name_med, dosage_med, category_name, quantity_med, instruction_name))
            result = cur.fetchone()
            connect.commit()
            return result[0]
def truncate_tables():
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select trunc_all()")
def clear_medic():
    with db_connect() as connect:
        connect.autocommit = True
        with connect.cursor() as cur:
            cur.execute("select clear_medicines()")
            return cur.fetchone()[0]
def drop_db():
    command = f"dropdb -h ""localhost"" -p  5432 -U ""my_user"" -e ""my_database"" --if-exists --force"
    os.system(command)



