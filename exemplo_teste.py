#!/usr/bin/env python3
"""
Exemplos de teste para as funcionalidades de matriz.
Este arquivo demonstra como usar as classes diretamente no código.
"""

from algebra import MatrizEscada
from fractions import Fraction as Fr

def teste_escalonamento():
    """Testa o escalonamento de uma matriz"""
    print("=" * 60)
    print("TESTE DE ESCALONAMENTO")
    print("=" * 60)
    
    # Matriz de exemplo
    matriz = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]
    
    print("Matriz original:")
    for linha in matriz:
        print(linha)
    
    # Escalonar
    escalonador = MatrizEscada(matriz)
    resultado = escalonador.escalonar()
    
    print("\nMatriz escalonada:")
    for linha in resultado:
        linha_formatada = [str(escalonador.formatar_valor(val)) for val in linha]
        print(linha_formatada)
    
    return escalonador

def teste_inversa():
    """Testa o cálculo de matriz inversa"""
    print("\n" + "=" * 60)
    print("TESTE DE MATRIZ INVERSA")
    print("=" * 60)
    
    # Matriz quadrada de exemplo
    matriz = [
        [2, 1, 1],
        [1, 3, 2],
        [1, 0, 0]
    ]
    
    print("Matriz original:")
    for linha in matriz:
        print(linha)
    
    try:
        # Calcular inversa
        calculador = MatrizEscada(matriz)
        inversa = calculador.calcular_inversa()
        
        print("\nMatriz inversa:")
        for linha in inversa:
            linha_formatada = [str(calculador.formatar_valor(val)) for val in linha]
            print(linha_formatada)
        
        # Verificar se está correta
        is_valid, produto = calculador.verificar_inversa(matriz, inversa)
        
        print(f"\nVerificação: {'PASSOU' if is_valid else 'FALHOU'}")
        print("Produto A × A⁻¹:")
        for linha in produto:
            linha_formatada = [str(calculador.formatar_valor(val)) for val in linha]
            print(linha_formatada)
        
        return calculador
        
    except ValueError as e:
        print(f"Erro: {e}")
        return None

def teste_matriz_singular():
    """Testa uma matriz que não tem inversa"""
    print("\n" + "=" * 60)
    print("TESTE DE MATRIZ SINGULAR (SEM INVERSA)")
    print("=" * 60)
    
    # Matriz singular (determinante = 0)
    matriz = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    print("Matriz singular:")
    for linha in matriz:
        print(linha)
    
    try:
        calculador = MatrizEscada(matriz)
        inversa = calculador.calcular_inversa()
        print("ERRO: Esta matriz deveria ser singular!")
    except ValueError as e:
        print(f"\nRESULTADO ESPERADO: {e}")

def teste_matriz_com_fracoes():
    """Testa matriz com frações"""
    print("\n" + "=" * 60)
    print("TESTE COM FRAÇÕES")
    print("=" * 60)
    
    # Matriz com frações
    matriz = [
        [Fr(1,2), Fr(1,3)],
        [Fr(1,4), Fr(1,5)]
    ]
    
    print("Matriz original (com frações):")
    for linha in matriz:
        linha_formatada = [str(val) for val in linha]
        print(linha_formatada)
    
    try:
        calculador = MatrizEscada(matriz)
        inversa = calculador.calcular_inversa()
        
        print("\nMatriz inversa:")
        for linha in inversa:
            linha_formatada = [str(val) for val in linha]
            print(linha_formatada)
        
        # Verificar
        is_valid, produto = calculador.verificar_inversa(matriz, inversa)
        print(f"\nVerificação: {'PASSOU' if is_valid else 'FALHOU'}")
        
    except ValueError as e:
        print(f"Erro: {e}")

def exemplo_com_historico():
    """Mostra como acessar o histórico de operações"""
    print("\n" + "=" * 60)
    print("EXEMPLO DE HISTÓRICO DE OPERAÇÕES")
    print("=" * 60)
    
    matriz = [
        [1, 2],
        [3, 4]
    ]
    
    calculador = MatrizEscada(matriz)
    inversa = calculador.calcular_inversa()
    
    print("Histórico de operações:")
    print("-" * 40)
    
    for i, etapa in enumerate(calculador.historico, 1):
        if etapa.get('tipo') == 'passo':
            print(f"\n{etapa['descricao']}")
        elif etapa.get('tipo') == 'matriz':
            print(f"{etapa['descricao']}")
            # Mostrar apenas as primeiras linhas para não ocupar muito espaço
            matriz_etapa = etapa['matriz']
            if len(matriz_etapa) <= 2:
                for linha in matriz_etapa:
                    linha_formatada = [str(calculador.formatar_valor(val)) for val in linha]
                    print(f"  {linha_formatada}")
            else:
                print("  [Matriz mostrada na interface gráfica]")

def main():
    """Executa todos os testes"""
    print("CALCULADORA DE MATRIZES - TESTES")
    print("Executando exemplos de uso das funcionalidades...\n")
    
    # Executar testes
    teste_escalonamento()
    teste_inversa()
    teste_matriz_singular()
    teste_matriz_com_fracoes()
    exemplo_com_historico()
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS!")
    print("Execute 'python main.py' para usar a interface gráfica.")
    print("=" * 60)

if __name__ == "__main__":
    main()