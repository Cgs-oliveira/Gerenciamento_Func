import sqlite3
import bcrypt


import sqlite3

class Database:
    def __init__(self, db_name):
        self.connect = sqlite3.connection(db_name)
        self.cursor = self.connection.cursor()

    def get_employees(self):
        self.cursor.execute("SELECT * FROM FUNC")
        return self.cursor.fetchall()

    def add_employee(self, id_pessoal, email, salario, cargo, id_dep, user_id):
        self.cursor.execute("INSERT INTO FUNC (ID_NOME, EMAIL, SALARIO, CARGO, ID_DEP, USER_ID) VALUES (?, ?, ?, ?, ?, ?)", 
                            (id_pessoal, email, salario, cargo, id_dep, user_id))
        self.connection.commit()

    def get_departments(self):
        self.cursor.execute("SELECT * FROM DEPARTAMENTO")
        return self.cursor.fetchall()

    def add_department(self, nome):
        self.cursor.execute("INSERT INTO DEPARTAMENTO (NOME) VALUES (?)", (nome,))
        self.connection.commit()

    def add_user(self, username, password, role):
        self.cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, ROLE) VALUES (?, ?, ?)", (username, password, role))
        self.connection.commit()

    def close(self):
        self.connection.close()


    # ======== CRUD para PESSOAL ========

    def add_pessoal(self, nome, cpf, telefone=None, data_nascimento=None):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PESSOAL (NOME, CPF, TELEFONE, DATA_NASCIMENTO)
                VALUES (?, ?, ?, ?)
            """, (nome, cpf, telefone, data_nascimento))
            conn.commit()
            return cursor.lastrowid

    def get_pessoal_by_id(self, id_pessoal):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID, NOME, CPF, TELEFONE, DATA_NASCIMENTO
                FROM PESSOAL
                WHERE ID = ?
            """, (id_pessoal,))
            return cursor.fetchone()

    def update_pessoal(self, id_pessoal, nome, cpf, telefone, data_nascimento):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE PESSOAL
                SET NOME = ?, CPF = ?, TELEFONE = ?, DATA_NASCIMENTO = ?
                WHERE ID = ?
            """, (nome, cpf, telefone, data_nascimento, id_pessoal))
            conn.commit()

    def delete_pessoal(self, id_pessoal):
        with self.connection() as conn:
            cursor = conn.cursor()
            # Primeiro, deletar de FUNC para manter a integridade referencial
            cursor.execute("DELETE FROM FUNC WHERE ID_NOME = ?", (id_pessoal,))
            cursor.execute("DELETE FROM PESSOAL WHERE ID = ?", (id_pessoal,))
            conn.commit()

    # ======== CRUD para ENDERECO ========

    def add_endereco(self, id_func, rua, cidade, estado, cep):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ENDERECO (ID_FUNC, RUA, CIDADE, ESTADO, CEP)
                VALUES (?, ?, ?, ?, ?)
            """, (id_func, rua, cidade, estado, cep))
            conn.commit()
            return cursor.lastrowid

    def get_enderecos_by_user(self, id_func):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID, RUA, CIDADE, ESTADO, CEP
                FROM ENDERECO
                WHERE ID_FUNC = ?
            """, (id_func,))
            return cursor.fetchall()

    def update_endereco(self, id_endereco, rua, cidade, estado, cep):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE ENDERECO
                SET RUA = ?, CIDADE = ?, ESTADO = ?, CEP = ?
                WHERE ID = ?
            """, (rua, cidade, estado, cep, id_endereco))
            conn.commit()

    def delete_endereco(self, id_endereco):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ENDERECO WHERE ID = ?", (id_endereco,))
            conn.commit()

    # ======== CRUD para TAREFAS ========

    def add_task(self, tarefa, idfunc):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO TAREFAS (TAREFA, IDFUNC) VALUES (?, ?)", 
                           (tarefa, idfunc))
            conn.commit()
            return cursor.lastrowid

    def get_tasks_by_user(self, idfunc):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID, TAREFA
                FROM TAREFAS
                WHERE IDFUNC = ?
            """, (idfunc,))
            return cursor.fetchall()

    def update_task(self, id_tarefa, tarefa, idfunc):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE TAREFAS 
                SET TAREFA = ?, IDFUNC = ? 
                WHERE ID = ?
            """, (tarefa, idfunc, id_tarefa))
            conn.commit()

    def delete_task(self, id_tarefa):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM TAREFAS WHERE ID = ?", (id_tarefa,))
            conn.commit()

    # ======== CRUD para outras tabelas (DEPARTAMENTO, FUNC, USERS, PROJETO) ========
    # (Implementação conforme necessidade) JOIN

    # ======== Método de Verificação de Usuário ========

    def verify_user(self, username, password):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT PASSWORD, ROLE, ID FROM USERS WHERE USERNAME=?", (username,))
            result = cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0]): 
                return result[1], result[2]  
            return None, None
        
         # ======== Método de Verificação de Usuário ADMIN ========
    def create_default_admin(self):
        with self.connection() as conn:
            cursor = conn.cursor()
            # Verificar se o usuário 'admin' já existe
            cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", ('admin',))
            admin_exists = cursor.fetchone()

        if not admin_exists:
            # Hash da senha 'masterkey'
            hashed_password = bcrypt.hashpw('masterkey'.encode('utf-8'), bcrypt.gensalt())

            try:
                cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, ROLE) VALUES (?, ?, ?)",
                               ('admin', hashed_password, 'admin'))
                conn.commit()
                print("Usuário admin padrão criado com sucesso!")
            except sqlite3.IntegrityError as e:
                print(f"Erro ao criar usuário admin: {e}")
