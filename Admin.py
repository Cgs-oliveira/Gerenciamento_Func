import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk
from BackEnd import Database


class Admin:
    def __init__(self):
        self.db = Database('gerenciamento_funcionarios.db')
        self.root = tk.Tk()
        self.root.title("Tela de Administração")
        self.root.geometry("1300x700")
        self.root.configure(bg="#f0f0f0")

        # Frame principal alinhado à esquerda
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, anchor='nw')

        # Botões para abrir janelas de CRUD
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)

        button_employee = tk.Button(buttons_frame, text="Adicionar Funcionário", command=self.open_add_employee_window, bg="#2196F3", fg="white", width=25)
        button_employee.grid(row=0, column=0, padx=5, pady=5)

        button_user = tk.Button(buttons_frame, text="Cadastrar Usuário", command=self.open_add_user_window, bg="#4CAF50", fg="white", width=25)
        button_user.grid(row=0, column=1, padx=5, pady=5)

        button_department = tk.Button(buttons_frame, text="Adicionar Departamento", command=self.open_add_department_window, bg="#FF9800", fg="white", width=25)
        button_department.grid(row=1, column=0, padx=5, pady=5)

        button_project = tk.Button(buttons_frame, text="Adicionar Projeto", command=self.open_add_project_window, bg="#9C27B0", fg="white", width=25)
        button_project.grid(row=1, column=1, padx=5, pady=5)

        button_task = tk.Button(buttons_frame, text="Adicionar Tarefa", command=self.open_add_task_window, bg="#E91E63", fg="white", width=25)
        button_task.grid(row=2, column=0, padx=5, pady=5)

        button_logout = tk.Button(main_frame, text="Logout", command=self.logout, bg="#f44336", fg="white", width=25)
        button_logout.grid(row=3, column=0, pady=20, sticky='w')

        # Frame para exibir dados (Exemplo: Funcionários)
        data_frame = tk.Frame(main_frame, bg="#f0f0f0")
        data_frame.grid(row=4, column=0, sticky='nw', padx=10, pady=10)

        # Tabela de Funcionários
        self.tree = ttk.Treeview(data_frame, columns=("ID", "Nome", "CPF", "Email", "Salário", "Cargo", "Departamento"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salário", text="Salário")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Departamento", text="Departamento")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Carregar dados ao iniciar
        self.load_employees()

        # Executar a janela
        self.root.mainloop()

    def load_employees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        employees = self.db.get_employees()
        for emp in employees:
            self.tree.insert("", "end", values=emp)

    def refresh_data(self):
        self.load_employees()

    # Métodos para abrir janelas de CRUD
    def open_add_employee_window(self):
        AddEmployeeWindow(self.db, self)

    def open_add_user_window(self):
        AddUserWindow(self.db, self)

    def open_add_department_window(self):
        AddDepartmentWindow(self.db, self)

    def open_add_project_window(self):
        AddProjectWindow(self.db, self)

    def open_add_task_window(self):
        AddTaskWindow(self.db, self)

    def logout(self):
        self.root.destroy()
        # Reiniciar a tela de login
        from FrontEnd import Frontend
        Frontend().run()


# Janelas de CRUD

class AddEmployeeWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Adicionar Funcionário")
        self.window.geometry("400x400")
        self.window.configure(bg="#f0f0f0")

        # Formulário de Funcionário
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_nome = tk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="CPF:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_cpf = tk.Entry(form_frame, width=30)
        self.entry_cpf.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Email:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_email = tk.Entry(form_frame, width=30)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Salário:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_salario = tk.Entry(form_frame, width=30)
        self.entry_salario.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cargo:", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.entry_cargo = tk.Entry(form_frame, width=30)
        self.entry_cargo.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Departamento ID:", bg="#f0f0f0").grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.entry_id_dep = tk.Entry(form_frame, width=30)
        self.entry_id_dep.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        # Botão de Adicionar
        button_add = tk.Button(self.window, text="Adicionar", command=self.add_employee, bg="#4CAF50", fg="white", width=20)
        button_add.pack(pady=20)

    def add_employee(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        email = self.entry_email.get()
        salario = self.entry_salario.get()
        cargo = self.entry_cargo.get()
        id_dep = self.entry_id_dep.get()

        # Validação de campos
        if not (nome and cpf and email and salario and cargo):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            salario = float(salario)
        except ValueError:
            messagebox.showerror("Erro", "Salário deve ser um número.")
            return

        id_dep = id_dep if id_dep else None

        try:
            # Verifique se id_dep existe, se não for None
            if id_dep:
                departamentos = self.db.get_departments()
                dep_ids = [dep[0] for dep in departamentos]
                if int(id_dep) not in dep_ids:
                    messagebox.showerror("Erro", "Departamento ID inválido.")
                    return

            # Adicionar pessoal
            id_pessoal = self.db.add_pessoal(nome, cpf, telefone=None, data_nascimento=None)  # Ajuste conforme necessário

            # Adicionar funcionário
            user_id = None  # Não é permitido atualmente adicionar funcionário sem usuário
            self.db.add_employee(id_pessoal, email, salario, cargo, id_dep, user_id)  # Isso causará erro devido a USER_ID NOT NULL
            messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso!")
            self.window.destroy()
            self.admin.refresh_data()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao adicionar funcionário: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")


class AddUserWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Cadastrar Usuário e Funcionário")
        self.window.geometry("400x500")  # Aumentei a altura 
        self.window.configure(bg="#f0f0f0")

        # Formulário de Usuário e Funcionário
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        # Campos de Usuário
        tk.Label(form_frame, text="Usuário:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_username = tk.Entry(form_frame, width=30)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Senha:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_password = tk.Entry(form_frame, show="*", width=30)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Papel:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_role = tk.Entry(form_frame, width=30)
        self.entry_role.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Campos de Funcionário
        tk.Label(form_frame, text="Nome:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_nome = tk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="CPF:", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.entry_cpf = tk.Entry(form_frame, width=30)
        self.entry_cpf.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Email:", bg="#f0f0f0").grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.entry_email = tk.Entry(form_frame, width=30)
        self.entry_email.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Salário:", bg="#f0f0f0").grid(row=6, column=0, padx=10, pady=10, sticky='e')
        self.entry_salario = tk.Entry(form_frame, width=30)
        self.entry_salario.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cargo:", bg="#f0f0f0").grid(row=7, column=0, padx=10, pady=10, sticky='e')
        self.entry_cargo = tk.Entry(form_frame, width=30)
        self.entry_cargo.grid(row=7, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Departamento ID :", bg="#f0f0f0").grid(row=8, column=0, padx=10, pady=10, sticky='e')
        self.entry_id_dep = tk.Entry(form_frame, width=30)
        self.entry_id_dep.grid(row=8, column=1, padx=10, pady=10, sticky='w')

        # Botão de Adicionar
        button_add_user = tk.Button(self.window, text="Cadastrar", command=self.add_user_and_employee, bg="#4CAF50", fg="white", width=20)
        button_add_user.pack(pady=20)

    def add_user_and_employee(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        role = self.entry_role.get()
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        email = self.entry_email.get()
        salario = self.entry_salario.get()
        cargo = self.entry_cargo.get()
        id_dep = self.entry_id_dep.get()

        # Validação de campos
        if not (username and password and role and nome and cpf and email and salario and cargo):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        if role not in ['admin', 'user']:
            messagebox.showerror("Erro", "Papel deve ser 'admin' ou 'user'.")
            return

        try:
            salario = float(salario)
        except ValueError:
            messagebox.showerror("Erro", "Salário deve ser um número.")
            return

        id_dep = id_dep if id_dep else None

        try:
            # Adicionar usuário
            user_id = self.db.add_user(username, password, role)
            # Adicionar pessoal
            id_pessoal = self.db.add_pessoal(nome, cpf, telefone=None, data_nascimento=None)  # Ajuste conforme necessário
            # Adicionar funcionário, associando ao usuário e pessoal
            self.db.add_employee(id_pessoal, email, salario, cargo, id_dep, user_id)
            messagebox.showinfo("Sucesso", "Usuário e Funcionário adicionados com sucesso!")
            self.window.destroy()
            self.admin.refresh_data()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário ou funcionário: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")


class AddDepartmentWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Adicionar Departamento")
        self.window.geometry("400x200")
        self.window.configure(bg="#f0f0f0")

        # Formulário de Departamento
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Nome do Departamento:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_depto_nome = tk.Entry(form_frame, width=30)
        self.entry_depto_nome.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Botão de Adicionar
        button_add_depto = tk.Button(self.window, text="Adicionar", command=self.add_department, bg="#4CAF50", fg="white", width=20)
        button_add_depto.pack(pady=20)

    def add_department(self):
        nome = self.entry_depto_nome.get()

        # Validação de campo
        if not nome:
            messagebox.showerror("Erro", "Por favor, preencha o nome do departamento.")
            return

        try:
            self.db.add_department(nome)
            messagebox.showinfo("Sucesso", "Departamento adicionado com sucesso!")
            self.window.destroy()
            self.admin.refresh_data()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao adicionar departamento: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")


class AddProjectWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Adicionar Projeto")
        self.window.geometry("400x300")
        self.window.configure(bg="#f0f0f0")

        # Formulário de Projeto
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Nome do Projeto:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_proj_nome = tk.Entry(form_frame, width=30)
        self.entry_proj_nome.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cliente:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_proj_cliente = tk.Entry(form_frame, width=30)
        self.entry_proj_cliente.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cargo:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_proj_cargo = tk.Entry(form_frame, width=30)
        self.entry_proj_cargo.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Botão de Adicionar
        button_add_proj = tk.Button(self.window, text="Adicionar", command=self.add_project, bg="#4CAF50", fg="white", width=20)
        button_add_proj.pack(pady=20)

    def add_project(self):
        nome = self.entry_proj_nome.get()
        cliente = self.entry_proj_cliente.get()
        cargo = self.entry_proj_cargo.get()

        # Validação de campos
        if not (nome and cliente and cargo):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            self.db.add_project(nome, cliente, cargo)
            messagebox.showinfo("Sucesso", "Projeto adicionado com sucesso!")
            self.window.destroy()
            self.admin.refresh_data()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao adicionar projeto: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")


class AddTaskWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Adicionar Tarefa")
        self.window.geometry("400x250")
        self.window.configure(bg="#f0f0f0")

        # Formulário de Tarefa
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Descrição da Tarefa:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_tarefa_desc = tk.Entry(form_frame, width=30)
        self.entry_tarefa_desc.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="ID Funcionário:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_tarefa_idfunc = tk.Entry(form_frame, width=30)
        self.entry_tarefa_idfunc.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Botão de Adicionar
        button_add_tarefa = tk.Button(self.window, text="Adicionar", command=self.add_task, bg="#4CAF50", fg="white", width=20)
        button_add_tarefa.pack(pady=20)

    def add_task(self):
        descricao = self.entry_tarefa_desc.get()
        id_func = self.entry_tarefa_idfunc.get()

        # Validação de campos
        if not (descricao and id_func):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            id_func = int(id_func)
        except ValueError:
            messagebox.showerror("Erro", "ID Funcionário deve ser um número.")
            return

        try:
            # Verifique se id_func existe
            employees = self.db.get_employees()
            emp_ids = [emp[0] for emp in employees]
            if id_func not in emp_ids:
                messagebox.showerror("Erro", "ID Funcionário não encontrado.")
                return

            self.db.add_task(descricao, id_func)
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            self.window.destroy()
            self.admin.refresh_data()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao adicionar tarefa: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")


# Executar a tela de administração
if __name__ == "__main__":
    Admin()
