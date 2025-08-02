"""
Módulo para operações de escalonamento de matrizes.
Implementa o algoritmo de eliminação de Gauss-Jordan para obtenção da forma escalonada completa
e cálculo de matriz inversa com histórico detalhado.
"""
from fractions import Fraction as Fr  # Importa Fraction para cálculos exatos com frações

class MatrizEscada:
    """
    Classe para transformar uma matriz em sua forma escalonada completa (forma escada),
    registrando o histórico de operações realizadas durante o processo.
    """

    def __init__(self, matriz):
        """Inicializa a matriz convertendo todos os elementos para frações"""
        self.matriz = [[Fr(valor) for valor in linha] for linha in matriz]
        self.historico = []
        self.pivos = []

    def registrar_operacao(self, operacao):
        self.historico.append(operacao)

    def encontrar_pivo(self, coluna, linha_inicio):
        linhas = len(self.matriz)
        if coluna >= len(self.matriz[0]) or linha_inicio >= linhas:
            return -1
        max_row = linha_inicio
        max_val = abs(self.matriz[linha_inicio][coluna])
        for r in range(linha_inicio + 1, linhas):
            valor = abs(self.matriz[r][coluna])
            if valor > max_val:
                max_val = valor
                max_row = r
        return max_row

    def trocar_linhas(self, linha1, linha2):
        if linha1 != linha2:
            self.matriz[linha1], self.matriz[linha2] = self.matriz[linha2], self.matriz[linha1]
            return True
        return False

    def multiplicar_linha(self, linha, escalar):
        if escalar != 0:
            self.matriz[linha] = [elemento * escalar for elemento in self.matriz[linha]]
            return True
        return False

    def combinar_linha(self, linha_alvo, linha_origem, escalar):
        if escalar != 0:
            nova_linha = [
                self.matriz[linha_alvo][j] + escalar * self.matriz[linha_origem][j]
                for j in range(len(self.matriz[linha_alvo]))
            ]
            self.matriz[linha_alvo] = nova_linha
            return True
        return False

    def escalonar(self):
        self.historico = []
        self.pivos = []
        linhas = len(self.matriz)
        if linhas == 0:
            return self.matriz
        colunas = len(self.matriz[0])
        pivot_linha = 0
        pivot_col = 0
        passo = 1
        
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz inicial:",
            'matriz': self.matriz_copia()
        })
        
        while pivot_linha < linhas and pivot_col < colunas:
            self.registrar_operacao({
                'tipo': 'passo',
                'descricao': f"--- PASSO {passo} (Fase descendente) ---"
            })
            passo += 1
            max_row = self.encontrar_pivo(pivot_col, pivot_linha)
            if max_row == -1 or self.matriz[max_row][pivot_col] == 0:
                pivot_col += 1
                continue
            if max_row != pivot_linha:
                self.trocar_linhas(pivot_linha, max_row)
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Operação I: Permuta L{pivot_linha+1} ↔ L{max_row+1}",
                    'matriz': self.matriz_copia()
                })
            pivot_val = self.matriz[pivot_linha][pivot_col]
            if pivot_val != 1:
                escalar = Fr(1, pivot_val) if pivot_val != 0 else Fr(0)
                self.multiplicar_linha(pivot_linha, escalar)
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Operação II: Normalização L{pivot_linha+1} ← {self.formatar_valor(escalar)} × L{pivot_linha+1}",
                    'matriz': self.matriz_copia()
                })
            self.pivos.append((pivot_linha, pivot_col))
            for i in range(pivot_linha + 1, linhas):
                if self.matriz[i][pivot_col] != 0:
                    escalar = -self.matriz[i][pivot_col]
                    self.combinar_linha(i, pivot_linha, escalar)
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Operação III: Eliminação L{i+1} ← L{i+1} + ({self.formatar_valor(escalar)}) × L{pivot_linha+1}",
                        'matriz': self.matriz_copia()
                    })
            pivot_linha += 1
            pivot_col += 1
        
        self.registrar_operacao({
            'tipo': 'passo',
            'descricao': "--- FASE ASCENDENTE (Eliminação para trás) ---"
        })
        
        for linha, col in reversed(self.pivos):
            for i in range(linha - 1, -1, -1):
                if self.matriz[i][col] != 0:
                    escalar = -self.matriz[i][col]
                    self.combinar_linha(i, linha, escalar)
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Operação III: Eliminação L{i+1} ← L{i+1} + ({self.formatar_valor(escalar)}) × L{linha+1}",
                        'matriz': self.matriz_copia()
                    })
        
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz na forma escalonada completa:",
            'matriz': self.matriz_copia()
        })
        return self.matriz

    def calcular_inversa(self):
        """
        Calcula a matriz inversa usando o método de Gauss-Jordan com histórico detalhado.
        A matriz [A|I] é transformada em [I|A^-1]
        """
        self.historico = []  # Limpa o histórico anterior
        linhas = len(self.matriz)
        colunas = len(self.matriz[0])
        
        if linhas != colunas:
            raise ValueError("A matriz deve ser quadrada para ter inversa.")
        
        # Cria a matriz identidade
        identidade = [[Fr(1) if i == j else Fr(0) for j in range(linhas)] for i in range(linhas)]
        
        # Cria a matriz aumentada [A|I]
        matriz_aumentada = []
        for i in range(linhas):
            linha_aumentada = self.matriz[i][:] + identidade[i][:]
            matriz_aumentada.append(linha_aumentada)
        
        # Salva a matriz original e trabalha com a aumentada
        matriz_original = self.matriz
        self.matriz = matriz_aumentada
        
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz aumentada [A|I] inicial:",
            'matriz': self.matriz_copia()
        })
        
        passo = 1
        
        # Fase 1: Transformar A em forma escalonada
        for i in range(linhas):
            self.registrar_operacao({
                'tipo': 'passo',
                'descricao': f"--- PASSO {passo} (Processando coluna {i+1}) ---"
            })
            passo += 1
            
            # Encontrar o melhor pivô
            pivo_linha = i
            for k in range(i + 1, linhas):
                if abs(self.matriz[k][i]) > abs(self.matriz[pivo_linha][i]):
                    pivo_linha = k
            
            # Verificar se a matriz é invertível
            if self.matriz[pivo_linha][i] == 0:
                self.matriz = matriz_original  # Restaura matriz original
                raise ValueError("Matriz não invertível (determinante = 0)")
            
            # Trocar linhas se necessário
            if pivo_linha != i:
                self.matriz[i], self.matriz[pivo_linha] = self.matriz[pivo_linha], self.matriz[i]
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Permuta L{i+1} ↔ L{pivo_linha+1}",
                    'matriz': self.matriz_copia()
                })
            
            # Normalizar a linha do pivô
            pivot_val = self.matriz[i][i]
            if pivot_val != 1:
                fator = Fr(1) / pivot_val
                for j in range(2 * linhas):
                    self.matriz[i][j] *= fator
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Normalização L{i+1} ← {self.formatar_valor(fator)} × L{i+1}",
                    'matriz': self.matriz_copia()
                })
            
            # Eliminar elementos abaixo do pivô
            for k in range(i + 1, linhas):
                if self.matriz[k][i] != 0:
                    fator = -self.matriz[k][i]
                    for j in range(2 * linhas):
                        self.matriz[k][j] += fator * self.matriz[i][j]
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Eliminação L{k+1} ← L{k+1} + ({self.formatar_valor(fator)}) × L{i+1}",
                        'matriz': self.matriz_copia()
                    })
        
        # Fase 2: Eliminação para trás (transformar em identidade)
        self.registrar_operacao({
            'tipo': 'passo',
            'descricao': "--- FASE DE ELIMINAÇÃO PARA TRÁS ---"
        })
        
        for i in range(linhas - 1, 0, -1):
            for k in range(i - 1, -1, -1):
                if self.matriz[k][i] != 0:
                    fator = -self.matriz[k][i]
                    for j in range(2 * linhas):
                        self.matriz[k][j] += fator * self.matriz[i][j]
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Eliminação L{k+1} ← L{k+1} + ({self.formatar_valor(fator)}) × L{i+1}",
                        'matriz': self.matriz_copia()
                    })
        
        # Extrair a matriz inversa (parte direita da matriz aumentada)
        inversa = []
        for i in range(linhas):
            linha_inversa = self.matriz[i][linhas:]
            inversa.append(linha_inversa)
        
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz inversa extraída:",
            'matriz': [linha[:] for linha in inversa]
        })
        
        # Restaurar a matriz original
        self.matriz = matriz_original
        
        return inversa

    def matriz_copia(self):
        return [linha[:] for linha in self.matriz]

    @staticmethod
    def formatar_valor(valor):
        if isinstance(valor, Fr):
            if valor.denominator == 1:
                return str(valor.numerator)
            return f"{valor.numerator}/{valor.denominator}"
        return str(valor)
    
    def verificar_inversa(self, matriz_original, matriz_inversa):
        """
        Verifica se o produto A × A^-1 = I
        """
        n = len(matriz_original)
        produto = [[Fr(0) for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    produto[i][j] += matriz_original[i][k] * matriz_inversa[k][j]
        
        # Verificar se é identidade
        for i in range(n):
            for j in range(n):
                esperado = Fr(1) if i == j else Fr(0)
                if produto[i][j] != esperado:
                    return False, produto
        
        return True, produto