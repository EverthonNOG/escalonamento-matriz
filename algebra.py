"""
Módulo para operações de escalonamento de matrizes.
Implementa o algoritmo de eliminação de Gauss-Jordan para obtenção da forma escalonada completa.
"""

from fractions import Fraction as Fr

class MatrizEscada:
    """
    Classe para transformar uma matriz em sua forma escalonada completa (forma escada),
    registrando o histórico de operações realizadas durante o processo.

    A forma escalonada completa atende às seguintes propriedades:
    1. O primeiro elemento não nulo de cada linha (pivô) é 1
    2. Cada coluna que contém um pivô tem todos os outros elementos iguais a zero
    3. O pivô de cada linha ocorre à direita do pivô da linha anterior
    4. Linhas nulas ficam abaixo das linhas não nulas

    Atributos:
        matriz (list[list[Fr]]): A matriz sendo transformada
        historico (list[dict]): Registro das operações realizadas
        pivos (list[tuple]): Posições dos pivôs (linha, coluna)
    """

    def __init__(self, matriz):
        """
        Inicializa a matriz convertendo elementos para frações.
        
        Args:
            matriz (list[list]): Matriz de entrada (números ou strings)
        """
        self.matriz = [[Fr(valor) for valor in linha] for linha in matriz]
        self.historico = []
        self.pivos = []  # Para armazenar posições dos pivôs

    def registrar_operacao(self, operacao):
        """Registra uma operação no histórico"""
        self.historico.append(operacao)

    def encontrar_pivo(self, coluna, linha_inicio):
        """
        Encontra o pivô para uma coluna a partir de linha inicial.
        
        O pivô é o elemento de maior valor absoluto na coluna.
        
        Args:
            coluna (int): Coluna para busca
            linha_inicio (int): Linha inicial para busca
            
        Returns:
            int: Índice da linha com melhor pivô ou -1 se inválido
        """
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
        """
        Operação elementar I: Permuta das i-ésima e j-ésima linhas (L_i ↔ L_j)
        
        Args:
            linha1 (int): Índice da primeira linha
            linha2 (int): Índice da segunda linha
            
        Returns:
            bool: True se troca foi realizada
        """
        if linha1 != linha2:
            self.matriz[linha1], self.matriz[linha2] = self.matriz[linha2], self.matriz[linha1]
            return True
        return False

    def multiplicar_linha(self, linha, escalar):
        """
        Operação elementar II: Multiplicação da i-ésima linha por escalar não nulo (L_i ← kL_i)
        
        Args:
            linha (int): Índice da linha
            escalar (Fr): Escalar multiplicador
            
        Returns:
            bool: True se operação realizada
        """
        if escalar != 0:
            self.matriz[linha] = [elemento * escalar for elemento in self.matriz[linha]]
            return True
        return False

    def substituir_linha(self, linha_alvo, linha_origem, escalar):
        """
        Operação elementar III: Substituição da i-ésima linha pela i-ésima linha mais k vezes a j-ésima (L_i ← L_i + kL_j)
        
        Args:
            linha_alvo (int): Linha a ser modificada
            linha_origem (int): Linha de referência
            escalar (Fr): Fator multiplicador
            
        Returns:
            bool: True se operação realizada
        """
        if escalar != 0:
            nova_linha = [
                self.matriz[linha_alvo][j] + escalar * self.matriz[linha_origem][j]
                for j in range(len(self.matriz[linha_alvo]))
            ]
            self.matriz[linha_alvo] = nova_linha
            return True
        return False

    def escalonar(self):
        """
        Transforma a matriz em sua forma escalonada completa usando eliminação de Gauss-Jordan.
        
        O processo ocorre em duas fases principais:
        1. Fase descendente: Cria pivôs e zera elementos abaixo deles
        2. Fase ascendente: Zera elementos acima dos pivôs
        
        Todas as operações são registradas no histórico para rastreamento.
        """
        self.historico = []
        self.pivos = []
        linhas = len(self.matriz)
        if linhas == 0:
            return self.matriz

        colunas = len(self.matriz[0])
        pivot_linha = 0
        pivot_col = 0
        passo = 1

        # Registrar matriz inicial
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz inicial:",
            'matriz': self.matriz_copia()
        })

        # FASE DESCENDENTE: Criação da forma escalonada
        while pivot_linha < linhas and pivot_col < colunas:
            self.registrar_operacao({
                'tipo': 'passo',
                'descricao': f"--- PASSO {passo} (Fase descendente) ---"
            })
            passo += 1

            # 1. Seleção do pivô (maior valor absoluto na coluna)
            max_row = self.encontrar_pivo(pivot_col, pivot_linha)
            
            # Correção aplicada: Verificação segura para pivô inválido
            if max_row == -1 or self.matriz[max_row][pivot_col] == 0:
                pivot_col += 1
                continue

            # 2. Permutar linhas se necessário (Operação I)
            if max_row != pivot_linha:
                self.trocar_linhas(pivot_linha, max_row)
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Operação I: Permuta L{pivot_linha+1} ↔ L{max_row+1}",
                    'matriz': self.matriz_copia()
                })

            # 3. Normalizar linha do pivô (Operação II)
            pivot_val = self.matriz[pivot_linha][pivot_col]
            if pivot_val != 1:
                escalar = Fr(1, pivot_val)
                self.multiplicar_linha(pivot_linha, escalar)
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Operação II: Normalização L{pivot_linha+1} ← {self.formatar_valor(escalar)} × L{pivot_linha+1}",
                    'matriz': self.matriz_copia()
                })

            # Registrar posição do pivô para fase ascendente
            self.pivos.append((pivot_linha, pivot_col))

            # 4. Eliminação para baixo (Operação III)
            for i in range(pivot_linha + 1, linhas):
                if self.matriz[i][pivot_col] != 0:
                    escalar = -self.matriz[i][pivot_col]
                    self.substituir_linha(i, pivot_linha, escalar)
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Operação III: Eliminação L{i+1} ← L{i+1} + ({self.formatar_valor(escalar)}) × L{pivot_linha+1}",
                        'matriz': self.matriz_copia()
                    })

            pivot_linha += 1
            pivot_col += 1

        # FASE ASCENDENTE: Criação da forma escalonada reduzida
        self.registrar_operacao({
            'tipo': 'passo',
            'descricao': "--- FASE ASCENDENTE (Eliminação para trás) ---"
        })

        # Processar pivôs de baixo para cima
        for linha, col in reversed(self.pivos):
            # Eliminação para cima (Operação III)
            for i in range(linha - 1, -1, -1):
                if self.matriz[i][col] != 0:
                    escalar = -self.matriz[i][col]
                    self.substituir_linha(i, linha, escalar)
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Operação III: Eliminação L{i+1} ← L{i+1} + ({self.formatar_valor(escalar)}) × L{linha+1}",
                        'matriz': self.matriz_copia()
                    })

        # Registrar matriz final
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz na forma escalonada completa:",
            'matriz': self.matriz_copia()
        })

        return self.matriz

    def matriz_copia(self):
        """Retorna cópia da matriz atual"""
        return [linha[:] for linha in self.matriz]
    
    @staticmethod
    def formatar_valor(valor):
        """
        Formata valores para exibição (frações simplificadas).
        
        Args:
            valor (Fr): Valor a formatar
            
        Returns:
            str: Representação simplificada
        """
        if isinstance(valor, Fr):
            if valor.denominator == 1:
                return str(valor.numerator)
            return f"{valor.numerator}/{valor.denominator}"
        return str(valor)