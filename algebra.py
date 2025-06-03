"""
Módulo para operações de álgebra linear, em particular, escalonamento de matrizes.
Implementa o algoritmo de eliminação de Gauss com pivotamento parcial.
"""

from fractions import Fraction as Fr

class MatrizEscada:
    """
    Classe para transformar uma matriz em sua forma escalonada (não reduzida),
    registrando o histórico de operações realizadas.

    Atributos:
        matriz (list[list[Fr]]): A matriz a ser escalonada, com elementos como frações.
        historico (list[dict]): Lista de operações realizadas durante o escalonamento.
    """

    def __init__(self, matriz):
        """
        Inicializa a matriz convertendo todos os elementos para frações.    

        Args:
            matriz (list[list]): Matriz de entrada (lista de listas de números ou strings).
        """
        self.matriz = [[Fr(valor) for valor in linha] for linha in matriz]
        self.historico = []

    def registrar_operacao(self, operacao):
        """
        Registra uma operação no histórico.

        Args:
            operacao (dict): Dicionário representando a operação, contendo pelo menos a chave 'tipo'.
        """
        self.historico.append(operacao)

    def encontrar_pivo(self, coluna, linha_inicio):
        """
        Encontra a linha do pivô para uma coluna dada, a partir de uma linha inicial.

        O pivô é o elemento de maior valor absoluto na coluna, a partir da linha_inicio.

        Args:
            coluna (int): Índice da coluna para buscar o pivô.
            linha_inicio (int): Índice da linha a partir da qual se inicia a busca.

        Returns:
            int: Índice da linha com o pivô, ou -1 se a coluna for inválida ou todos os elementos forem zero.
        """
        linhas = len(self.matriz)
        # Verificação crítica para evitar index errors
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

    def eliminar_abaixo(self, linha, coluna):
        """
        Elimina os elementos abaixo do pivô na coluna dada.

        Args:
            linha (int): Índice da linha do pivô.
            coluna (int): Índice da coluna do pivô.

        Returns:
            bool: True se alguma operação de eliminação foi realizada, False caso contrário.
        """
        alterou = False
        pivot_val = self.matriz[linha][coluna]
        if pivot_val == 0:
            return False
            
        for i in range(linha + 1, len(self.matriz)):
            fator = self.matriz[i][coluna] / pivot_val
            if fator != 0:
                self.matriz[i] = [
                    self.matriz[i][j] - fator * self.matriz[linha][j]
                    for j in range(len(self.matriz[i]))
                ]
                alterou = True
        return alterou

    def trocar_linhas(self, linha1, linha2):
        """
        Troca duas linhas da matriz.

        Args:
            linha1 (int): Índice da primeira linha.
            linha2 (int): Índice da segunda linha.

        Returns:
            bool: True se a troca foi realizada, False se as linhas são iguais.
        """
        if linha1 != linha2:
            self.matriz[linha1], self.matriz[linha2] = self.matriz[linha2], self.matriz[linha1]
            return True
        return False

    def escalonar(self):
        """
        Realiza o escalonamento da matriz (forma escalonada) com pivotamento parcial.

        Returns:
            list[list[Fr]]: A matriz escalonada.

        Registra no histórico todas as operações realizadas.
        """
        self.historico = []
        linhas = len(self.matriz)
        if linhas == 0:
            return self.matriz

        colunas = len(self.matriz[0])
        pivot_linha = 0
        pivot_col = 0

        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz inicial:",
            'matriz': self.matriz_copia()
        })

        passo = 1
        while pivot_linha < linhas and pivot_col < colunas:
            self.registrar_operacao({
                'tipo': 'passo',
                'descricao': f"--- PASSO {passo} ---"
            })
            passo += 1

            max_row = self.encontrar_pivo(pivot_col, pivot_linha)

            # Tratamento de colunas com todos zeros
            if max_row == -1 or self.matriz[max_row][pivot_col] == 0:
                pivot_col += 1  # Avança coluna mantendo mesma linha
                continue        # Retorna ao início do loop

            if max_row != pivot_linha:
                self.trocar_linhas(pivot_linha, max_row)
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Troca: Linha {pivot_linha+1} ↔ Linha {max_row+1}",
                    'matriz': self.matriz_copia()
                })

            # Verificação otimizada para eliminação
            if any(self.matriz[i][pivot_col] != 0 for i in range(pivot_linha + 1, linhas)):
                if self.eliminar_abaixo(pivot_linha, pivot_col):
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Eliminação abaixo: Subtrações na coluna {pivot_col+1}",
                        'matriz': self.matriz_copia()
                    })
            else:
                self.registrar_operacao({
                    'tipo': 'descricao',
                    'descricao': "Eliminação abaixo: Nenhuma operação necessária (já zerado)"
                })

            pivot_linha += 1
            pivot_col += 1

        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz escalonada final:",
            'matriz': self.matriz_copia()
        })

        return self.matriz

    def matriz_copia(self):
        """
        Retorna uma cópia da matriz atual.

        Returns:
            list[list[Fr]]: Cópia da matriz.
        """
        return [linha[:] for linha in self.matriz]
    
    @staticmethod
    def formatar_valor(valor):
        """
        Formata um valor (fração) para string de forma legível.

        Args:
            valor (Fr): Fração a ser formatada.

        Returns:
            str: String representando a fração (ex: "1/2" ou "2" se for inteiro).
        """
        if isinstance(valor, Fr):
            if valor.denominator == 1:
                return str(valor.numerator)
            return f"{valor.numerator}/{valor.denominator}"
        return str(valor)