import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from algebra import MatrizEscada
from fractions import Fraction as Fr

class Utils:
    @staticmethod
    def centralizar_janela(janela):
        janela.update_idletasks()
        largura_janela = janela.winfo_width()
        altura_janela = janela.winfo_height()
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura_janela // 2)
        y = (altura_tela // 2) - (altura_janela // 2)
        janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    
    @staticmethod
    def formatar_fracoes(valor):
        if isinstance(valor, Fr):
            if valor.numerator == 0:
                return "0"
            if valor.denominator == 1:
                return str(valor.numerator)
            return f"{valor.numerator}/{valor.denominator}"
        return str(valor)
    
    @staticmethod
    def formatar_matriz_com_bordas(matriz):
        if not matriz or not matriz[0]:
            return ""
            
        col_widths = []
        for j in range(len(matriz[0])):
            max_width = 0
            for linha in matriz:
                formatted = Utils.formatar_fracoes(linha[j])
                if len(formatted) > max_width:
                    max_width = len(formatted)
            col_widths.append(max_width + 2)
        
        lines = []
        for i, linha in enumerate(matriz):
            elements = []
            for j, valor in enumerate(linha):
                formatted = Utils.formatar_fracoes(valor)
                padding = col_widths[j] - len(formatted)
                left_pad = padding // 2
                right_pad = padding - left_pad
                elements.append(f"{' ' * left_pad}{formatted}{' ' * right_pad}")
            
            line_str = "│ " + " │ ".join(elements) + " │"
            lines.append(line_str)
            
            if i < len(matriz) - 1:
                separators = []
                for width in col_widths:
                    separators.append('─' * width)
                separator = "├─" + "─┼─".join(separators) + "─┤"
                lines.append(separator)
        
        top_bottom = []
        for width in col_widths:
            top_bottom.append('─' * width)
        
        top = "┌─" + "─┬─".join(top_bottom) + "─┐"
        bottom = "└─" + "─┴─".join(top_bottom) + "─┘"
        
        return "\n".join([top] + lines + [bottom])

class JanelaHistorico:
    def __init__(self, parent, historico):
        self.janela = tk.Toplevel(parent)
        self.janela.title("Passo a Passo do Processo")
        self.janela.geometry("900x700")
        self.janela.configure(bg='#f5f7fa')
        
        style = ttk.Style()
        style.configure('Hist.TFrame', background='#f5f7fa')
        style.configure('Hist.TButton', background='#4a7abc', foreground='white')
        
        main_frame = ttk.Frame(self.janela, padding=15)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Passo a Passo do Processo", 
                 font=('Arial', 14, 'bold'), foreground='#2c3e50').pack(pady=(0, 15))
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill='both', expand=True)
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame, wrap='word', font=('Courier New', 10), 
            bg='#ffffff', relief='flat', padx=15, pady=15
        )
        self.text_area.pack(fill='both', expand=True)
        
        self.text_area.tag_configure('passo', foreground='#2980b9', font=('Arial', 12, 'bold'))
        self.text_area.tag_configure('descricao', foreground='#333', font=('Arial', 11))
        self.text_area.tag_configure('matriz', font=('Courier New', 9))
        
        self.text_area.config(state='normal')
        for etapa in historico:
            if etapa.get('tipo') == 'passo':
                self.text_area.insert(tk.END, etapa['descricao'] + "\n", 'passo')
                self.text_area.insert(tk.END, "\n")
            elif etapa.get('tipo') == 'matriz':
                self.text_area.insert(tk.END, etapa['descricao'] + "\n", 'descricao')
                self.text_area.insert(tk.END, "\n")
                formatted = Utils.formatar_matriz_com_bordas(etapa['matriz'])
                self.text_area.insert(tk.END, formatted + "\n\n", 'matriz')
        self.text_area.config(state='disabled')
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=15)
        
        ttk.Button(btn_frame, text="Fechar", command=self.janela.destroy, 
                  style='Hist.TButton', width=15).pack(pady=5)
        
        Utils.centralizar_janela(self.janela)
        self.janela.grab_set()

class JanelaVerificacao:
    def __init__(self, parent, matriz_original, matriz_inversa, produto):
        self.janela = tk.Toplevel(parent)
        self.janela.title("Verificação da Matriz Inversa")
        self.janela.geometry("800x600")
        self.janela.configure(bg='#f5f7fa')
        
        main_frame = ttk.Frame(self.janela, padding=15)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Verificação: A × A⁻¹ = I", 
                 font=('Arial', 14, 'bold'), foreground='#2c3e50').pack(pady=(0, 15))
        
        # Frame com scroll
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Texto de verificação
        text_area = tk.Text(scrollable_frame, wrap='none', font=('Courier New', 10),
                           bg='#ffffff', relief='flat', padx=15, pady=15, height=25)
        
        # Adicionar conteúdo
        text_area.insert(tk.END, "MATRIZ ORIGINAL (A):\n\n")
        text_area.insert(tk.END, Utils.formatar_matriz_com_bordas(matriz_original) + "\n\n")
        
        text_area.insert(tk.END, "MATRIZ INVERSA (A⁻¹):\n\n")
        text_area.insert(tk.END, Utils.formatar_matriz_com_bordas(matriz_inversa) + "\n\n")
        
        text_area.insert(tk.END, "PRODUTO A × A⁻¹:\n\n")
        text_area.insert(tk.END, Utils.formatar_matriz_com_bordas(produto) + "\n\n")
        
        # Verificar se é identidade
        n = len(produto)
        is_identity = True
        for i in range(n):
            for j in range(n):
                esperado = Fr(1) if i == j else Fr(0)
                if produto[i][j] != esperado:
                    is_identity = False
                    break
            if not is_identity:
                break
        
        if is_identity:
            text_area.insert(tk.END, "✓ VERIFICAÇÃO CONFIRMADA: A × A⁻¹ = I\n")
            text_area.insert(tk.END, "A matriz inversa está CORRETA!")
        else:
            text_area.insert(tk.END, "✗ ERRO: A × A⁻¹ ≠ I\n")
            text_area.insert(tk.END, "Houve um problema no cálculo da matriz inversa.")
        
        text_area.config(state='disabled')
        text_area.pack(fill='both', expand=True)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=15)
        
        ttk.Button(btn_frame, text="Fechar", command=self.janela.destroy, width=15).pack()
        
        Utils.centralizar_janela(self.janela)
        self.janela.grab_set()

class Aplicacao:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Calculadora de Matrizes - Escalonamento e Inversa")
        self.janela.geometry("1100x700")
        self.janela.configure(bg='#f5f7fa')
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#f5f7fa')
        style.configure('TLabel', background='#f5f7fa', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Section.TLabelframe.Label', font=('Arial', 11, 'bold'), foreground='#2c3e50')
        style.configure('Section.TLabelframe', background='#f5f7fa', borderwidth=1, relief='solid')
        style.configure('Accent.TButton', background='#4a7abc', foreground='white')
        style.map('Accent.TButton', background=[('active', '#3a6aac')])
        style.configure('Success.TButton', background='#27ae60', foreground='white')
        style.map('Success.TButton', background=[('active', '#229954')])
        
        self.linhas = tk.IntVar(value=3)
        self.colunas = tk.IntVar(value=3)
        self.transformador = None
        self.ultima_operacao = None
        self.matriz_original = None
        self.resultado_atual = None
        
        self.criar_widgets()
        self.desenhar_matriz_entrada()
        Utils.centralizar_janela(self.janela)
    
    def criar_widgets(self):
        main_frame = ttk.Frame(self.janela, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Calculadora de Matrizes", 
                 style='Title.TLabel').pack(pady=(0, 20))
        
        config_frame = ttk.LabelFrame(main_frame, text=" Configurações ", style='Section.TLabelframe', padding=15)
        config_frame.pack(fill='x', pady=(0, 20))
        
        dim_frame = ttk.Frame(config_frame)
        dim_frame.pack(fill='x', pady=10)
        
        ttk.Label(dim_frame, text="Dimensões:", font=('Arial', 10, 'bold')).pack(side='left', padx=(0, 10))
        ttk.Label(dim_frame, text="Linhas:", font=('Arial', 10)).pack(side='left', padx=(0, 5))
        self.spin_linhas = ttk.Spinbox(dim_frame, from_=1, to=8, width=5,
                                      textvariable=self.linhas, command=self.atualizar_matriz,
                                      font=('Arial', 10))
        self.spin_linhas.pack(side='left', padx=5)
        
        ttk.Label(dim_frame, text="Colunas:", font=('Arial', 10)).pack(side='left', padx=(20, 5))
        self.spin_colunas = ttk.Spinbox(dim_frame, from_=1, to=8, width=5,
                                       textvariable=self.colunas, command=self.atualizar_matriz,
                                       font=('Arial', 10))
        self.spin_colunas.pack(side='left', padx=5)
        
        # Frame para botões principais
        btn_frame = ttk.Frame(config_frame)
        btn_frame.pack(fill='x', pady=15)
        
        ttk.Button(btn_frame, text="Escalonar", command=self.realizar_escalonamento,
                  style='Accent.TButton', width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Calcular Inversa", command=self.calcular_inversa,
                  style='Success.TButton', width=15).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar, width=12).pack(side='left', padx=5)
        
        # Frame para botões secundários
        btn_frame2 = ttk.Frame(config_frame)
        btn_frame2.pack(fill='x', pady=5)
        
        self.historico_btn = ttk.Button(btn_frame2, text="Ver Passo a Passo", 
                                      command=self.mostrar_historico, state='disabled', width=15)
        self.historico_btn.pack(side='left', padx=5)
        
        self.verificar_btn = ttk.Button(btn_frame2, text="Verificar Inversa", 
                                      command=self.verificar_inversa, state='disabled', width=15)
        self.verificar_btn.pack(side='left', padx=5)
        
        # Quadrado obrigatório para inversa
        self.info_label = ttk.Label(config_frame, text="ℹ Para calcular a inversa, a matriz deve ser quadrada", 
                                   font=('Arial', 9), foreground='#7f8c8d')
        self.info_label.pack(pady=5)
        
        matrizes_frame = ttk.Frame(main_frame)
        matrizes_frame.pack(fill='both', expand=True)
        
        entrada_frame = ttk.LabelFrame(matrizes_frame, text=" Matriz de Entrada ", 
                                     style='Section.TLabelframe', padding=15)
        entrada_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        entrada_canvas = tk.Canvas(entrada_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(entrada_frame, orient="vertical", command=entrada_canvas.yview)
        self.entrada_scrollable = ttk.Frame(entrada_canvas)
        
        self.entrada_scrollable.bind(
            "<Configure>",
            lambda e: entrada_canvas.configure(scrollregion=entrada_canvas.bbox("all"))
        )
        
        entrada_canvas.create_window((0, 0), window=self.entrada_scrollable, anchor="nw")
        entrada_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        entrada_canvas.pack(side="left", fill="both", expand=True)
        
        self.entrada_container = self.entrada_scrollable
        
        resultado_frame = ttk.LabelFrame(matrizes_frame, text=" Resultado ", 
                                       style='Section.TLabelframe', padding=15)
        resultado_frame.pack(side='right', fill='both', expand=True, padx=10)
        
        self.resultado_container = ttk.Frame(resultado_frame)
        self.resultado_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.resultado_scroll = scrolledtext.ScrolledText(
            self.resultado_container, wrap='none', font=('Courier New', 11),
            bg='#ffffff', relief='flat', padx=10, pady=10
        )
        self.resultado_scroll.pack(fill='both', expand=True)
        self.resultado_scroll.config(state='disabled')
    
    def atualizar_matriz(self):
        self.desenhar_matriz_entrada()
        # Atualizar info sobre matriz quadrada
        linhas = self.linhas.get()
        colunas = self.colunas.get()
        if linhas == colunas:
            self.info_label.config(text="✓ Matriz quadrada - Pronta para calcular a inversa", 
                                 foreground='#27ae60')
        else:
            self.info_label.config(text="ℹ Para calcular a inversa, a matriz deve ser quadrada", 
                                 foreground='#7f8c8d')
    
    def desenhar_matriz_entrada(self):
        for widget in self.entrada_container.winfo_children():
            widget.destroy()
        
        linhas = self.linhas.get()
        colunas = self.colunas.get()
        
        self.campos_entrada = []
        for i in range(linhas):
            linha_campos = []
            for j in range(colunas):
                frame = ttk.Frame(self.entrada_container)
                frame.grid(row=i, column=j, padx=3, pady=3)
                
                entry = ttk.Entry(frame, width=6, justify='center', font=('Arial', 10))
                entry.pack()
                entry.insert(0, "1" if i == j else "0")
                linha_campos.append(entry)
            self.campos_entrada.append(linha_campos)
    
    def mostrar_resultado(self, matriz, titulo="Resultado"):
        self.resultado_scroll.config(state='normal')
        self.resultado_scroll.delete(1.0, tk.END)
        
        self.resultado_scroll.insert(tk.END, f"{titulo}:\n\n")
        formatted = Utils.formatar_matriz_com_bordas(matriz)
        self.resultado_scroll.insert(tk.END, formatted)
        self.resultado_scroll.config(state='disabled')
    
    def obter_matriz(self):
        matriz = []
        linhas = self.linhas.get()
        colunas = self.colunas.get()
        
        try:
            for i in range(linhas):
                linha_vals = []
                for j in range(colunas):
                    valor = self.campos_entrada[i][j].get().strip()
                    
                    if not valor:
                        valor = "0"
                    
                    if '/' in valor:
                        partes = valor.split('/')
                        if len(partes) == 2:
                            num = int(partes[0])
                            den = int(partes[1])
                            if den != 0:
                                linha_vals.append(Fr(num, den))
                            else:
                                raise ValueError("Denominador zero")
                        else:
                            raise ValueError("Formato de fração inválido")
                    else:
                        linha_vals.append(Fr(valor))
                matriz.append(linha_vals)
            
            return matriz
        except Exception as e:
            messagebox.showerror("Erro de Entrada", 
                                f"Valor inválido encontrado: {str(e)}\n\n"
                                "Use números inteiros ou frações (ex: 1/2)")
            return None
    
    def realizar_escalonamento(self):
        matriz = self.obter_matriz()
        if matriz is None:
            return
        
        try:
            self.transformador = MatrizEscada(matriz)
            self.matriz_original = [linha[:] for linha in matriz]  # Cópia da matriz original
            resultado = self.transformador.escalonar()
            self.resultado_atual = resultado
            self.ultima_operacao = "escalonamento"
            
            self.mostrar_resultado(resultado, "Matriz Escalonada")
            self.historico_btn.config(state='normal')
            self.verificar_btn.config(state='disabled')  # Não aplicável para escalonamento
        except Exception as e:
            messagebox.showerror("Erro no Processamento", f"Ocorreu um erro:\n{str(e)}")
    
    def calcular_inversa(self):
        matriz = self.obter_matriz()
        if matriz is None:
            return
        
        # Verificar se a matriz é quadrada
        linhas = len(matriz)
        colunas = len(matriz[0]) if matriz else 0
        
        if linhas != colunas:
            messagebox.showerror("Erro", "A matriz deve ser quadrada para calcular a inversa!")
            return
        
        try:
            self.transformador = MatrizEscada(matriz)
            self.matriz_original = [linha[:] for linha in matriz]  # Cópia da matriz original
            inversa = self.transformador.calcular_inversa()
            self.resultado_atual = inversa
            self.ultima_operacao = "inversa"
            
            self.mostrar_resultado(inversa, "Matriz Inversa")
            self.historico_btn.config(state='normal')
            self.verificar_btn.config(state='normal')  # Habilitar verificação
            
            messagebox.showinfo("Sucesso", "Matriz inversa calculada com sucesso!\n\n"
                              "Use 'Verificar Inversa' para confirmar o resultado.")
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            self.historico_btn.config(state='disabled')
            self.verificar_btn.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao calcular inversa: {str(e)}")
            self.historico_btn.config(state='disabled')
            self.verificar_btn.config(state='disabled')
    
    def verificar_inversa(self):
        if (self.matriz_original is None or self.resultado_atual is None or 
            self.ultima_operacao != "inversa"):
            messagebox.showwarning("Aviso", "Calcule uma matriz inversa primeiro!")
            return
        
        try:
            # Criar uma nova instância para verificação
            verificador = MatrizEscada(self.matriz_original)
            is_valid, produto = verificador.verificar_inversa(self.matriz_original, self.resultado_atual)
            
            # Mostrar janela de verificação
            JanelaVerificacao(self.janela, self.matriz_original, self.resultado_atual, produto)
            
        except Exception as e:
            messagebox.showerror("Erro na Verificação", f"Erro ao verificar a inversa: {str(e)}")
    
    def limpar(self):
        linhas = self.linhas.get()
        colunas = self.colunas.get()
        
        for i in range(linhas):
            for j in range(colunas):
                self.campos_entrada[i][j].delete(0, tk.END)
                self.campos_entrada[i][j].insert(0, "1" if i == j else "0")
        
        self.resultado_scroll.config(state='normal')
        self.resultado_scroll.delete(1.0, tk.END)
        self.resultado_scroll.config(state='disabled')
        
        self.historico_btn.config(state='disabled')
        self.verificar_btn.config(state='disabled')
        self.transformador = None
        self.ultima_operacao = None
        self.matriz_original = None
        self.resultado_atual = None
    
    def mostrar_historico(self):
        if self.transformador and hasattr(self.transformador, 'historico'):
            JanelaHistorico(self.janela, self.transformador.historico)
        else:
            messagebox.showinfo("Histórico Indisponível", 
                              "Execute uma operação primeiro para gerar o histórico")

if __name__ == "__main__":
    janela = tk.Tk()
    app = Aplicacao(janela)
    janela.mainloop()