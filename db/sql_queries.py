import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

def get_data(sql:str, values:tuple=None, res_type=list):
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD)
    cursor = connection.cursor()
    try:
        cursor.execute(sql, values)
    except Exception as e:
        data = {"error":f"{e}"}

    if res_type == list:
        data = cursor.fetchall()
    else:
        data = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return data


def set_data(sql:str, values:tuple=None):
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD)
    cursor = connection.cursor()

    try:
        cursor.execute(sql, values)
        connection.commit()
        data = {"status":"ok"}
    except Exception as e:
        data = {"error":f"{e}"}
    cursor.close()
    connection.close()
    return data


def get_user_infos():
    sql = f'''
        SELECT users.id, email, password, name, address, phone, dob FROM users INNER JOIN user_informations ON users.id=user_informations.user_id;
        '''
    data = get_data(sql, res_type=list)
    users = []
    tpl_user = ('id', 'email', 'password', 'name',)
    tpl_user_informations = ('address', 'phone', 'dob')
    for dt in data:
        tpl_ui = dict(tuple([(tpl_user_informations[i], dt[len(tpl_user)+i]) for i in range(len(tpl_user_informations))]))
        user = dict(tuple([(tpl_user[i], dt[i]) for i in range(len(tpl_user))]))    
        user['user_informations'] = tpl_ui
        users.append(user)
    
    return users

sql = '''
    CREATE TABLE users(
        id  bigserial PRIMARY KEY,
        email VARCHAR(100) UNIQUE NOT NULL,
        name VARCHAR(100),
        password VARCHAR(128) NOT NULL
    );'''

sql_infos = '''
    CREATE TABLE user_informations(
        id bigserial PRIMARY KEY,
        address VARCHAR (500),
        phone VARCHAR(40),
        user_id INT,
        CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(id)
    );'''