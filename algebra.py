"""
Módulo para operações de escalonamento de matrizes.
Implementa o algoritmo de eliminação de Gauss-Jordan para obtenção da forma escalonada completa.
"""
from fractions import Fraction as Fr  # Importa Fraction para cálculos exatos com frações

class MatrizEscada:
    """
    Classe para transformar uma matriz em sua forma escalonada completa (forma escada),
    registrando o histórico de operações realizadas durante o processo.
    """

    def __init__(self, matriz):
        """Inicializa a matriz convertendo todos os elementos para frações"""
        # Converte cada elemento da matriz para Fraction (para precisão matemática)
        self.matriz = [[Fr(valor) for valor in linha] for linha in matriz]
        self.historico = []  # Armazena histórico de operações (passos e matrizes intermediárias)
        self.pivos = []     # Lista para registrar posições (linha, coluna) dos pivôs

    def registrar_operacao(self, operacao):
        """Adiciona uma operação ao histórico de transformações"""
        self.historico.append(operacao)

    def encontrar_pivo(self, coluna, linha_inicio):
        """
        Encontra a linha com melhor pivô (maior valor absoluto) em uma coluna específica,
        a partir de uma linha inicial.
        """
        linhas = len(self.matriz)
        # Verifica se coluna ou linha inicial estão fora dos limites da matriz
        if coluna >= len(self.matriz[0]) or linha_inicio >= linhas:
            return -1  # Retorno inválido para indicar erro

        # Inicializa variáveis com os valores da linha inicial
        max_row = linha_inicio
        max_val = abs(self.matriz[linha_inicio][coluna])

        # Percorre as linhas abaixo da linha inicial
        for r in range(linha_inicio + 1, linhas):
            valor = abs(self.matriz[r][coluna])  # Valor absoluto do elemento
            # Atualiza se encontrar valor maior
            if valor > max_val:
                max_val = valor
                max_row = r

        return max_row  # Retorna índice da linha com melhor pivô

    def trocar_linhas(self, linha1, linha2):
        """Operação elementar I: Troca duas linhas de posição (L_i ↔ L_j)"""
        if linha1 != linha2:  # Só executa se linhas forem diferentes
            # Troca fisicamente as linhas na matriz
            self.matriz[linha1], self.matriz[linha2] = self.matriz[linha2], self.matriz[linha1]
            return True  # Indica que troca foi realizada
        return False  # Indica que não houve troca

    def multiplicar_linha(self, linha, escalar):
        """Operação elementar II: Multiplica linha por escalar não nulo (L_i ← kL_i)"""
        if escalar != 0:  # Verifica escalar válido
            # Multiplica cada elemento da linha pelo escalar
            self.matriz[linha] = [elemento * escalar for elemento in self.matriz[linha]]
            return True  # Indica sucesso
        return False  # Indica falha (escalar zero)

    def combinar_linha(self, linha_alvo, linha_origem, escalar):
        """
        Operação elementar III: Combina linha_alvo com múltiplo da linha_origem 
        (L_i ← L_i + kL_j)
        """
        if escalar != 0:  # Verifica escalar válido
            # Cria nova linha somando elemento a elemento
            nova_linha = [
                self.matriz[linha_alvo][j] + escalar * self.matriz[linha_origem][j]
                for j in range(len(self.matriz[linha_alvo]))
            ]
            self.matriz[linha_alvo] = nova_linha  # Atualiza a linha na matriz
            return True  # Indica sucesso
        return False  # Indica falha

    def escalonar(self):
        """Método principal: Executa o escalonamento completo (Gauss-Jordan)"""
        # Reinicia estruturas de dados para novo cálculo
        self.historico = []
        self.pivos = []
        linhas = len(self.matriz)
        
        # Caso especial: matriz vazia
        if linhas == 0:
            return self.matriz

        colunas = len(self.matriz[0])
        pivot_linha = 0  # Linha atual do pivô
        pivot_col = 0    # Coluna atual do pivô
        passo = 1        # Contador de passos para histórico

        # Registra matriz inicial no histórico
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz inicial:",
            'matriz': self.matriz_copia()
        })

        # FASE DESCENDENTE: Criação da forma escalonada
        while pivot_linha < linhas and pivot_col < colunas:
            # Registra início de novo passo
            self.registrar_operacao({
                'tipo': 'passo',
                'descricao': f"--- PASSO {passo} (Fase descendente) ---"
            })
            passo += 1

            # Encontra melhor pivô na coluna atual
            max_row = self.encontrar_pivo(pivot_col, pivot_linha)
            
            # Se não encontrou pivô válido, avança para próxima coluna
            if max_row == -1 or self.matriz[max_row][pivot_col] == 0:
                pivot_col += 1
                continue

            # Se pivô não está na linha atual, troca linhas
            if max_row != pivot_linha:
                self.trocar_linhas(pivot_linha, max_row)
                # Registra operação de troca
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Operação I: Permuta L{pivot_linha+1} ↔ L{max_row+1}",
                    'matriz': self.matriz_copia()
                })

            # Normaliza pivô para 1 (se necessário)
            pivot_val = self.matriz[pivot_linha][pivot_col]
            if pivot_val != 1:
                # Calcula fator de normalização (inverso do pivô)
                escalar = Fr(1, pivot_val) if pivot_val != 0 else Fr(0)
                self.multiplicar_linha(pivot_linha, escalar)
                # Registra operação de normalização
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Operação II: Normalização L{pivot_linha+1} ← {self.formatar_valor(escalar)} × L{pivot_linha+1}",
                    'matriz': self.matriz_copia()
                })

            # Armazena posição do pivô para uso posterior
            self.pivos.append((pivot_linha, pivot_col))

            # Eliminação: Zera elementos abaixo do pivô
            for i in range(pivot_linha + 1, linhas):
                if self.matriz[i][pivot_col] != 0:
                    # Calcula fator para zerar elemento
                    escalar = -self.matriz[i][pivot_col]
                    self.combinar_linha(i, pivot_linha, escalar)
                    # Registra operação de eliminação
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Operação III: Eliminação L{i+1} ← L{i+1} + ({self.formatar_valor(escalar)}) × L{pivot_linha+1}",
                        'matriz': self.matriz_copia()
                    })

            # Avança para próximo pivô (diagonal inferior direita)
            pivot_linha += 1
            pivot_col += 1

        # FASE ASCENDENTE: Criação da forma escalonada completa
        self.registrar_operacao({
            'tipo': 'passo',
            'descricao': "--- FASE ASCENDENTE (Eliminação para trás) ---"
        })

        # Processa pivôs de baixo para cima
        for linha, col in reversed(self.pivos):
            # Zera elementos acima do pivô atual
            for i in range(linha - 1, -1, -1):
                if self.matriz[i][col] != 0:
                    # Calcula fator para zerar elemento
                    escalar = -self.matriz[i][col]
                    self.combinar_linha(i, linha, escalar)
                    # Registra operação de eliminação
                    self.registrar_operacao({
                        'tipo': 'matriz',
                        'descricao': f"Operação III: Eliminação L{i+1} ← L{i+1} + ({self.formatar_valor(escalar)}) × L{linha+1}",
                        'matriz': self.matriz_copia()
                    })

        # Registra resultado final
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz na forma escalonada completa:",
            'matriz': self.matriz_copia()
        })

        return self.matriz  # Retorna matriz escalonada

    def matriz_copia(self):
        """Cria cópia profunda da matriz atual (para registro no histórico)"""
        return [linha[:] for linha in self.matriz]  # Usa slicing para copiar cada linha
    
    @staticmethod
    def formatar_valor(valor):
        """
        Formata valores Fraction para exibição amigável:
        - Inteiros: mostra como número inteiro (ex: '3')
        - Frações: mostra como fração (ex: '2/3')
        - Outros tipos: converte para string
        """
        if isinstance(valor, Fr):  # Verifica se é Fraction
            if valor.denominator == 1:  # Se denominador é 1, é inteiro
                return str(valor.numerator)
            return f"{valor.numerator}/{valor.denominator}"  # Formato fração
        return str(valor)  # Para outros tipos (não deve ocorrer)
