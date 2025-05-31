from fractions import Fraction

class ProcessoEscalonamento:
    def __init__(self):
        self.passo_atual = 0
        self.historico = []
    
    def registrar_passo(self, matriz, operacao):
        self.passo_atual += 1
        matriz_copia = [linha[:] for linha in matriz]
        self.historico.append({
            'passo': self.passo_atual,
            'matriz': matriz_copia,
            'operacao': operacao
        })
    
    def mostrar_historico(self):
        print("\n" + "="*60)
        print("HISTÓRICO DE OPERAÇÕES")
        print("="*60)
        
        for etapa in self.historico:
            print(f"\nPASSO {etapa['passo']}: {etapa['operacao']}")
            self.imprimir_matriz(etapa['matriz'])
    
    def imprimir_matriz(self, matriz):
        """Imprime a matriz formatada com elementos como frações"""
        for linha in matriz:
            linha_formatada = []
            for elem in linha:
                if isinstance(elem, Fraction):
                    # Corrige representação de frações negativas
                    if elem.denominator < 0:
                        elem = Fraction(-elem.numerator, -elem.denominator)
                    
                    if elem.denominator == 1:
                        linha_formatada.append(str(elem.numerator))
                    else:
                        linha_formatada.append(f"{elem.numerator}/{elem.denominator}")
                else:
                    # Para números não fracionários
                    if elem == int(elem):
                        linha_formatada.append(str(int(elem)))
                    else:
                        linha_formatada.append(str(elem))
            print(' '.join(linha_formatada))
        print()

def ler_matriz_simples():
    """Solicita e valida a matriz do usuário"""
    print("\nINSIRA A MATRIZ:")
    print("Digite cada linha separada por espaços")
    print("Exemplo: 2 1 -1 8")
    print("Ou com frações: 1/2 3/4 -1/3")
    print("Digite 'fim' quando terminar\n")
    
    matriz = []
    while True:
        entrada = input("> ").strip()
        if entrada.lower() == 'fim':
            break
        if not entrada:
            continue
            
        elementos = entrada.split()
        linha_nums = []
        for elem in elementos:
            try:
                if '/' in elem:
                    partes = elem.split('/')
                    if len(partes) != 2:
                        raise ValueError("Formato inválido")
                    num = int(partes[0])
                    den = int(partes[1])
                    if den == 0:
                        raise ZeroDivisionError("Denominador zero")
                    frac = Fraction(num, den)
                    linha_nums.append(frac)
                else:
                    linha_nums.append(Fraction(elem))
            except Exception as e:
                print(f"Erro no elemento '{elem}': {e} - usando 0")
                linha_nums.append(Fraction(0))
                
        matriz.append(linha_nums)
    
    # Garante que a matriz seja retangular
    if matriz:
        num_colunas = max(len(linha) for linha in matriz)
        for linha in matriz:
            while len(linha) < num_colunas:
                linha.append(Fraction(0))
    
    return matriz

def forma_escada_com_fracoes(matriz, processo):
    """
    Transforma a matriz em forma de escada (escalonada) usando frações
    e registra cada passo do processo
    """
    A = [linha[:] for linha in matriz]
    linhas = len(A)
    if linhas == 0:
        return A
        
    colunas = len(A[0])
    linha_pivo = 0
    
    for j in range(colunas):
        if linha_pivo >= linhas:
            break
        
        # Encontrar o pivô na coluna atual
        pivo_index = None
        for i in range(linha_pivo, linhas):
            if A[i][j] != 0:
                pivo_index = i
                break
        
        if pivo_index is None:
            continue  # Não há pivô nesta coluna
        
        # Trocar linhas se necessário
        if pivo_index != linha_pivo:
            A[linha_pivo], A[pivo_index] = A[pivo_index], A[linha_pivo]
            processo.registrar_passo(A, 
                f"Troca L{linha_pivo+1} ↔ L{pivo_index+1}")
        
        pivô = A[linha_pivo][j]  # Guarda o valor ORIGINAL do pivô
        
        # Zerar elementos abaixo do pivô usando o valor ORIGINAL
        for i in range(linha_pivo + 1, linhas):
            if A[i][j] == 0:  # Evita operações desnecessárias
                continue
                
            fator = Fraction(A[i][j], pivô)
            operacao = f"L{i+1} ← L{i+1} - ({fator})×L{linha_pivo+1}"
            
            for k in range(j, colunas):
                A[i][k] = A[i][k] - fator * A[linha_pivo][k]
                
            processo.registrar_passo(A, operacao)
        
        # Normalizar a linha do pivô APÓS zerar elementos abaixo
        if pivô != 1:
            for k in range(j, colunas):
                A[linha_pivo][k] = Fraction(A[linha_pivo][k], pivô)
            processo.registrar_passo(A, 
                f"Normaliza L{linha_pivo+1} ÷ {pivô}")
        
        linha_pivo += 1
    
    processo.registrar_passo(A, "FORMA DE ESCADA FINAL")
    return A

def main():
    print("="*60)
    print("TRANSFORMAÇÃO DE MATRIZES PARA FORMA DE ESCADA")
    print("="*60)
    
    matriz = ler_matriz_simples()
    
    if not matriz:
        print("Matriz vazia! Encerrando programa.")
        return
    
    processo = ProcessoEscalonamento()
    processo.registrar_passo(matriz, "Matriz original")
    
    print("\nMatriz inserida:")
    processo.imprimir_matriz(matriz)
    
    resultado = forma_escada_com_fracoes(matriz, processo)
    
    processo.mostrar_historico()
    
    print("\n" + "="*60)
    print("RESULTADO FINAL (FORMA ESCADA)")
    processo.imprimir_matriz(resultado)
    print("="*60)

if __name__ == "__main__":
    main()