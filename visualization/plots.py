import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import logging
import numpy as np

def visualize_results(results):
    """
    Função para visualizar os resultados da análise de dados. Gera dois gráficos:
    1. Gráfico de barras para as principais métricas (excluindo simulações e recomendações).
    2. Histograma das projeções geradas pela simulação de Monte Carlo.

    Parâmetros:
    - results: Dicionário contendo os resultados da análise de dados.
    """
    try:
        # Filtrar as chaves que contêm métricas numéricas
        plot_results = {k: v for k, v in results.items() if k not in ["Recomendações", "Simulação de Monte Carlo", "Coluna Analisada"]}
        simulated_projections = results.get("Simulação de Monte Carlo", [])

        # Verificar se plot_results contém apenas valores numéricos
        for key, value in plot_results.items():
            if not isinstance(value, (int, float, np.integer, np.floating)):
                raise ValueError(f"O valor de '{key}' não é numérico.")

        # Inicializar o Tkinter
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Visualização", "Os resultados serão exibidos em um gráfico.")
        root.destroy()  # Destruir a janela raiz do Tkinter

        plt.figure(figsize=(10, 12))  # Configurar o tamanho da figura para dois gráficos

        # Primeiro subplot: Gráfico de Barras para as Métricas
        plt.subplot(2, 1, 1)
        metrics = list(plot_results.keys())
        values = list(plot_results.values())
        bars = plt.bar(metrics, values, color='skyblue')
        plt.xlabel('Métricas')
        plt.ylabel('Valores')
        plt.title('Resultados da Análise de Dados')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Rotacionar labels do eixo X se houver muitas métricas
        if len(metrics) > 5:
            plt.xticks(rotation=45, ha='right')

        # Adicionar rótulos de dados em cada barra
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05,
                     f"{yval:.2f}", ha='center', va='bottom')

        # Segundo subplot: Histograma da Simulação de Monte Carlo
        if isinstance(simulated_projections, np.ndarray) and simulated_projections.size > 0:
            plt.subplot(2, 1, 2)
            plt.hist(simulated_projections, bins=30, color='lightgreen', edgecolor='black')
            plt.xlabel('Valores Projetados')
            plt.ylabel('Frequência')
            plt.title('Simulação de Monte Carlo - Distribuição das Projeções Futuras')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
        else:
            logging.warning("Simulação de Monte Carlo não encontrada nos resultados.")

        plt.tight_layout()
        plt.show()

    except Exception as e:
        logging.error(f"Erro ao visualizar resultados: {e}")
        print("Erro ao visualizar resultados. Verifique o log para mais detalhes.")
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", f"Ocorreu um erro ao visualizar os resultados:\n{e}")
        root.destroy()

def plot_histogram(data, column_name, bins=30, screen=None):
    """
    Gera um histograma com base nos dados fornecidos.

    Parâmetros:
    - data: A coluna de dados numéricos.
    - column_name: Nome da coluna a ser exibido no gráfico.
    - bins: Número de intervalos no histograma.
    - screen: Objeto opcional para garantir execução na main thread (usado com Tkinter ou Pygame).
    """
    try:
        if len(data) == 0:
            raise ValueError("Os dados estão vazios. Não é possível gerar o histograma.")

        # Verificar se estamos na main thread (por exemplo, com Tkinter)
        if screen is not None:
            # Use screen para garantir que o histograma seja exibido na thread correta
            screen.after(0, lambda: plot_histogram(data, column_name, bins))
            return

        # Geração do histograma
        plt.figure(figsize=(8, 6))
        plt.hist(data, bins=bins, color='blue', edgecolor='black', alpha=0.7)
        plt.title(f'Histograma da Coluna: {column_name}')
        plt.xlabel('Valores')
        plt.ylabel('Frequência')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

        logging.info(f"Histograma gerado com sucesso para a coluna: {column_name}")

    except Exception as e:
        logging.error(f"Erro ao gerar o histograma: {e}")
        print(f"Erro ao gerar o histograma: {e}")
