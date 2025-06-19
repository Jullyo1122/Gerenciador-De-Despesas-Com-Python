import tkinter as tk
from tkinter import messagebox
import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt

ARQUIVO = 'despesas.csv'

#Cria o arquivo csv se não existir
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, 'w', newline='')as f:
        writer = csv.writer(f)
        writer.writerow(['Data', 'Categoria', 'Valor'])

#Adiciona as despesas
def adicionar_despesas():
    data = entry_data.get()
    categoria = entry_categoria.get()
    valor = entry_valor.get()
    renda_input = entry_renda.get()


    with open(ARQUIVO, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data, categoria, valor])

    if not data or not categoria or not valor:
        messagebox.showwarning("Campos vazios", "Preencha os campos.")
        return
    
    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor númerico.")
        return
    
    messagebox.showinfo("Sucesso!", "Despesa adicionada!")
    entry_data.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    
# Carrega a renda atual do arquivo
    if not os.path.exists('renda.csv'):
        messagebox.showerror("Erro", "Renda não definida.")
        return

    with open('renda.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            try:
                renda = float(row[0])
            except (ValueError, IndexError):
                messagebox.showerror("Erro", "Renda inválida.")
                return
            break
        else:
            renda = 0

    if valor > renda:
        messagebox.showwarning("Renda insuficiente", "O valor da despesa é maior que a renda disponível.")
        return

    # Atualiza a renda
    renda -= valor
    with open('renda.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Renda"])
        writer.writerow([renda])

    renda_atual.set(f"R$ {renda:.2f}")



#Cria o gráfico visual das despesas
def mostrar_grafico():
    categorias = defaultdict(float)

    with open(ARQUIVO, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                categorias[row['Categoria']] += float(row['Valor'])
            except (ValueError, KeyError):
                continue  # Ignora linhas inválidas


    if not categorias:
        messagebox.showinfo("Info", "Nenhuma despesa cadastrada.")
        return

    plt.figure(figsize=(6,6))
    plt.pie(categorias.values(), labels=categorias.keys(), autopct='%1.1f%%', startangle=90)
    plt.title("Gastos por Categoria")
    plt.axis('equal')
    plt.show()

#Função para definir uma renda 
def definir_renda():
    renda = entry_renda.get()

    if not renda:
        messagebox.showwarning("Campos vazios", "Preencha o campo.")
        return
    
    try:
        renda = float(renda)
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor númerico.")
        return
    
    with open('renda.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Renda"])
        writer.writerow([renda])

    entry_renda.delete(0, tk.END)
    renda_atual.set(f"R$ {renda:.2f}") 
    messagebox.showinfo("Sucesso", "Sua renda está definida!")

#Mostra a renda na Interface
def carregar_renda():
    if not os.path.exists('renda.csv'):
        return "R$ 0.00"
    
    with open('renda.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            try: 
                 return f"R$ {float(row[0]):.2f}"
            except (ValueError, IndexError):
                return "R$ 0.00"
    return "R$ 0.00"
    
    
#Interface com Tkinter 
janela = tk.Tk()
janela.title("Gerenciador de Despesas")

renda_atual = tk.StringVar()
renda_atual.set(carregar_renda())

tk.Label(janela, text="Renda Atual:").grid(row=7, column=0)
tk.Label(janela, textvariable=renda_atual).grid(row=7, column=1)

tk.Label(janela, text="Data (DD/MM/AAAA)").grid(row=0, column=0)
tk.Label(janela, text="Categoria").grid(row=1, column=0)
tk.Label(janela, text="Valor").grid(row=2, column=0)

entry_data = tk.Entry(janela)
entry_categoria = tk.Entry(janela)
entry_valor = tk.Entry(janela)

entry_data.grid(row=0, column=1)
entry_categoria.grid(row=1, column=1)
entry_valor.grid(row=2, column=1)

btn_adicionar = tk.Button(janela, text="Adicionar Despesa", command=adicionar_despesas)
btn_grafico = tk.Button(janela, text="Mostrar Gráfico", command=mostrar_grafico)

btn_adicionar.grid(row=3, column=0, columnspan=2, pady=5)
btn_grafico.grid(row=4, column=0, columnspan=2)

entry_renda = tk.Entry(janela)
entry_renda.grid(row=5, column=1)

btn_definirRenda = tk.Button(janela, text="Definir renda", command=definir_renda)
btn_definirRenda.grid(row=6, column=0, columnspan=2,)

janela.mainloop()