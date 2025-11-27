import mysql.connector
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()

db_config = {
    'host': 'mysql-db', 
    'user': 'root',
    'password': '',
    'database': 'prueba'
}

print("Conectando a la base de datos...")
conn = mysql.connector.connect(**db_config)
c = conn.cursor()

print("Creando tabla users...")
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT NOT NULL AUTO_INCREMENT,
        username varchar(20),
        password varchar(256),
        role varchar(20),
        PRIMARY KEY (id)
    );
''')

print("Insertando usuarios...")
# Limpiamos tabla para no duplicar si corres el script dos veces
c.execute("TRUNCATE TABLE users")
c.execute('''
    INSERT INTO users (username, password, role) VALUES
    (%s, %s, %s),
    (%s, %s, %s)
''', ('admin', hash_password('password'), 'admin',
      'user', hash_password('password'), 'user'))

print("Creando tabla tasks...")
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
    id INT NOT NULL AUTO_INCREMENT,
    tasks  VARCHAR(100),
    user_id INT,      
    PRIMARY KEY (id)  
);
''')

print("Insertando tareas...")
c.execute("TRUNCATE TABLE tasks")
c.execute('''
    INSERT INTO tasks (tasks,user_id) VALUES
    (%s,%s),
    (%s,%s)
''', ('correr',1, 'saltar',2))

conn.commit()
c.close()
conn.close()
print("¡Base de datos inicializada correctamente!")
