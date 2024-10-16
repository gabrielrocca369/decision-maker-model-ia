import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import logging

def visualize_results(results):
    try:
        # Remover as chaves "Recomendações" e "Simulação de Monte Carlo" para o gráfico de barras
        plot_results = {k: v for k, v in results.items() if k not in ["Recomendações", "Simulação de Monte Carlo"]}
        simulated_projections = results["Simulação de Monte Carlo"]

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Visualização", "Os resultados serão exibidos em um gráfico.")

        plt.figure(figsize=(10, 12))  # Aumentar o tamanho para acomodar dois gráficos

        # Primeiro subplot: Gráfico de Barras
        plt.subplot(2, 1, 1)
        bars = plt.bar(plot_results.keys(), plot_results.values(), color='skyblue')
        plt.xlabel('Métricas')
        plt.ylabel('Valores')
        plt.title('Resultados da Análise de Dados')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Adicionar rótulos de dados em cada barra
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05,
                     f"{round(yval, 2):,}", ha='center', va='bottom')

        # Segundo subplot: Histograma da Simulação de Monte Carlo
        plt.subplot(2, 1, 2)
        plt.hist(simulated_projections, bins=30, color='lightgreen', edgecolor='black')
        plt.xlabel('Valores Projetados')
        plt.ylabel('Frequência')
        plt.title('Simulação de Monte Carlo - Distribuição das Projeções Futuras')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.show()
    except Exception as e:
        logging.error(f"Erro ao visualizar resultados: {e}")
        print("Erro ao visualizar resultados. Verifique o log para mais detalhes.")
