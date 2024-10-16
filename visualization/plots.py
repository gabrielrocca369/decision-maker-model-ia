import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import logging
import numpy as np

def visualize_results(results):
    try:
        # Remover as chaves que não são valores numéricos simples
        plot_results = {k: v for k, v in results.items() if k not in ["Recomendações", "Simulação de Monte Carlo", "Coluna Analisada"]}
        simulated_projections = results["Simulação de Monte Carlo"]

        # Verificar se plot_results contém apenas valores numéricos
        for key, value in plot_results.items():
            if not isinstance(value, (int, float, np.integer, np.floating)):
                raise ValueError(f"O valor de '{key}' não é numérico.")

        # Inicializar o Tkinter
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Visualização", "Os resultados serão exibidos em um gráfico.")
        root.destroy()  # Destruir a janela raiz do Tkinter

        plt.figure(figsize=(10, 12))  # Aumentar o tamanho para acomodar dois gráficos

        # Primeiro subplot: Gráfico de Barras
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
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", f"Ocorreu um erro ao visualizar os resultados:\n{e}")
        root.destroy()
