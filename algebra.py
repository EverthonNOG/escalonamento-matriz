from fractions import Fraction as Fr

class MatrizCondensadaEscada:
    def __init__(self, matriz):
        # Converte todos os valores para Fraction para precisão matemática
        self.matriz = [[Fr(valor) for valor in linha] for linha in matriz]
        self.historico = []  # Armazena todas as operações para o passo-a-passo

    def registrar_operacao(self, operacao):
        """Registra uma operação no histórico para fins didáticos"""
        self.historico.append(operacao)

    def encontrar_pivo(self, coluna, linha_inicio):
        """Localiza o maior pivô na coluna para melhor estabilidade numérica"""
        linhas = len(self.matriz)
        if coluna >= len(self.matriz[0]):  # Evita indexação fora dos limites
            return -1

        max_row = linha_inicio
        max_val = abs(self.matriz[linha_inicio][coluna])

        for r in range(linha_inicio + 1, linhas):
            valor = abs(self.matriz[r][coluna])
            if valor > max_val:
                max_val = valor
                max_row = r

        return max_row

    def normalizar_linha(self, linha, coluna):
        """Transforma o pivô em 1 dividindo toda a linha pelo pivô"""
        pivot = self.matriz[linha][coluna]
        if pivot != 0:
            self.matriz[linha] = [x / pivot for x in self.matriz[linha]]
            return True
        return False

    def eliminar_abaixo(self, linha, coluna):
        """Zera elementos abaixo do pivô usando operações elementares"""
        alterou = False
        for i in range(linha + 1, len(self.matriz)):
            fator = self.matriz[i][coluna]
            if fator != 0:
                # Operação: Linha_i = Linha_i - fator * Linha_pivo
                self.matriz[i] = [
                    self.matriz[i][j] - fator * self.matriz[linha][j]
                    for j in range(len(self.matriz[i]))
                ]
                alterou = True
        return alterou

    def eliminar_acima(self, linha, coluna):
        """Zera elementos acima do pivô (OPCIONAL para forma reduzida)"""
        alterou = False
        for i in range(linha):
            fator = self.matriz[i][coluna]
            if fator != 0:
                # Operação: Linha_i = Linha_i - fator * Linha_pivo
                self.matriz[i] = [
                    self.matriz[i][j] - fator * self.matriz[linha][j]
                    for j in range(len(self.matriz[i]))
                ]
                alterou = True
        return alterou

    def trocar_linhas(self, linha1, linha2):
        """Operação elementar: Permuta duas linhas"""
        if linha1 != linha2:
            self.matriz[linha1], self.matriz[linha2] = self.matriz[linha2], self.matriz[linha1]
            return True
        return False

    def condensar(self):
        """Executa o algoritmo de escalonamento (Eliminação Gaussiana)"""
        self.historico = []
        linhas = len(self.matriz)
        if linhas == 0:
            return self.matriz

        colunas = len(self.matriz[0])
        pivot_linha = 0  # Controla a posição atual do pivô
        pivot_col = 0

        # Registro inicial importante para o histórico
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

            # Fase 1: Localização do pivô
            max_row = self.encontrar_pivo(pivot_col, pivot_linha)

            # Pula colunas sem pivôs não-nulos
            if max_row == -1 or self.matriz[max_row][pivot_col] == 0:
                pivot_col += 1
                continue

            # Fase 2: Permuta de linhas (se necessário)
            if max_row != pivot_linha:
                self.trocar_linhas(pivot_linha, max_row)
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Troca: Linha {pivot_linha+1} ↔ Linha {max_row+1}",
                    'matriz': self.matriz_copia()
                })

            # Fase 3: Normalização do pivô
            pivot_val = self.matriz[pivot_linha][pivot_col]
            if pivot_val != 0:
                self.normalizar_linha(pivot_linha, pivot_col)
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Normalização: Linha {pivot_linha+1} ÷ {self.formatar_valor(pivot_val)}",
                    'matriz': self.matriz_copia()
                })

            # Fase 4: Eliminação para baixo
            if self.eliminar_abaixo(pivot_linha, pivot_col):
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Eliminação abaixo: Subtrações na coluna {pivot_col+1}",
                    'matriz': self.matriz_copia()
                })

            # ======= FORMA ESCADA REDUZIDA (OPCIONAL) =======
            # Descomente para Gauss-Jordan (forma reduzida)
            '''
            if self.eliminar_acima(pivot_linha, pivot_col):
                self.registrar_operacao({
                    'tipo': 'matriz',
                    'descricao': f"Eliminação acima: Subtrações na coluna {pivot_col+1}",
                    'matriz': self.matriz_copia()
                })
            '''
            # ===============================================

            pivot_linha += 1
            pivot_col += 1

        # Resultado final
        self.registrar_operacao({
            'tipo': 'matriz',
            'descricao': "Matriz escalonada final:",
            'matriz': self.matriz_copia()
        })

        return self.matriz

    def matriz_copia(self):
        """Cria uma cópia segura da matriz para registro histórico"""
        return [linha[:] for linha in self.matriz]
    
    @staticmethod
    def formatar_valor(valor):
        """Formata valores para exibição amigável no histórico"""
        if isinstance(valor, Fr):
            if valor.denominator == 1:
                return str(valor.numerator)
            return f"{valor.numerator}/{valor.denominator}"
        return str(valor)