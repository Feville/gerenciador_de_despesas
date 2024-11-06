import tkinter as tk
from tkinter import messagebox
import requests

# URL base da API Flask
API_URL = "http://127.0.0.1:8000"


def login_user():
    email = entry_email.get()
    password = entry_password.get()

    response = requests.post(
        f"{API_URL}/login", json={"email": email, "password": password}
    )

    if response.status_code == 200:
        messagebox.showinfo("Sucesso", "Usuário logado com sucesso!")
        root.withdraw()  # Esconde a tela de login
        show_finance_screen(email)
    else:
        messagebox.showerror("Erro", "Problema ao logar usuário")


def register_user():
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()
    response = requests.post(
        f"{API_URL}/register",
        json={"username": username, "email": email, "password": password},
    )
    if response.status_code == 200:
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        root.withdraw()
        show_finance_screen(email)
    else:
        messagebox.showerror("Erro", "Problema ao registrar usuário")


def show_finance_screen(email):
    finance_screen = tk.Toplevel(root)
    finance_screen.title("Tela de Finanças")

    # Tela de finanças
    tk.Label(finance_screen, text="Saldo").grid(row=0, column=0)
    tk.Button(
        finance_screen, text="Mostrar Saldo", command=lambda: get_balance(email)
    ).grid(row=0, column=1)

    tk.Label(finance_screen, text="Adicionar Despesa").grid(row=1, column=0)
    tk.Label(finance_screen, text="Categoria").grid(row=1, column=1)
    tk.Label(finance_screen, text="Valor").grid(row=1, column=2)

    entry_category = tk.Entry(finance_screen)
    entry_category.grid(row=2, column=1)

    entry_amount = tk.Entry(finance_screen)
    entry_amount.grid(row=2, column=2)

    tk.Button(
        finance_screen,
        text="Adicionar Despesa",
        command=lambda: add_user_balance(
            email, entry_category.get(), entry_amount.get()
        ),
    ).grid(row=3, columnspan=3)


def get_balance(email):
    response = requests.get(f"{API_URL}/get_balance/{email}")
    if response.status_code == 200:
        data = response.json()
        messagebox.showinfo("Saldo", f"Saldo: {data['msg']}")
    else:
        messagebox.showerror("Erro", "Erro ao obter saldo")


def add_user_balance(email, category, amount):
    response = requests.post(
        f"{API_URL}/add_user_balance",
        json={"email": email, "amount": int(amount), "category_name": category},
    )
    if response.status_code == 201:
        messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
    else:
        messagebox.showerror("Erro", "Erro ao adicionar despesa")


# Configuração da interface Tkinter
root = tk.Tk()
root.title("Gerenciador de Despesas")

# Tela de Login
root.geometry("300x250")  # Aumentado para acomodar o campo "Nome de Usuário"

# Campo para Nome de Usuário (usado apenas para registro)
tk.Label(root, text="Nome de Usuário:").grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Email:").grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Senha:").grid(row=2, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Login", command=login_user).grid(row=3, columnspan=2, pady=10)
tk.Button(root, text="Registrar", command=register_user).grid(
    row=4, columnspan=2, pady=10
)

root.mainloop()
