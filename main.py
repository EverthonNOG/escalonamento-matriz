#!/usr/bin/env python3
"""
Calculadora de Matrizes - Aplicação Principal
Executa a interface gráfica para cálculo de escalonamento e inversa de matrizes.

Para executar: python main.py
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def main():
    try:
        # Importar a aplicação
        from interface import Aplicacao
        
        # Criar janela principal
        root = tk.Tk()
        
        # Configurar ícone da janela (se disponível)
        try:
            # root.iconbitmap('icon.ico')  # Descomente se tiver um ícone
            pass
        except:
            pass
        
        # Inicializar aplicação
        app = Aplicacao(root)
        
        # Configurar evento de fechamento
        def on_closing():
            if messagebox.askokcancel("Sair", "Deseja realmente sair da aplicação?"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Iniciar loop principal
        root.mainloop()
        
    except ImportError as e:
        messagebox.showerror("Erro de Importação", 
                           f"Erro ao importar módulos necessários:\n{str(e)}\n\n"
                           "Certifique-se de que os arquivos 'algebra.py' e 'interface.py' "
                           "estão no mesmo diretório que este arquivo.")
        sys.exit(1)
    except Exception as e:
        messagebox.showerror("Erro Inesperado", 
                           f"Ocorreu um erro inesperado:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()