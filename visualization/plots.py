import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import logging
import numpy as np
import seaborn as sns  # Adicionando seaborn para o box plot
import os

# Caminho para a fonte Open Sans
FONT_PATH = os.path.join(
    'C:/Users/GabrielRocca/source/repos/games/decision-maker/assets/fonts/Open_Sans/static',
    'OpenSans-Regular.ttf'
)

# Definir uma fonte padrão usando Open Sans
if os.path.exists(FONT_PATH):
    plt.rcParams['font.family'] = 'Open Sans'
    plt.rcParams['pdf.fonttype'] = 42  # Para garantir compatibilidade ao salvar em PDF
else:
    logging.warning("Fonte Open Sans não encontrada. Usando fonte padrão DejaVu Sans.")
    plt.rcParams['font.family'] = 'DejaVu Sans'


def visualize_results(results):
    """
    Função para visualizar os resultados da análise de dados.
    Plota um gráfico de barras e um box plot das projeções da Simulação de Monte Carlo.
    """
    try:
        # Filtrar resultados para plotagem (excluindo chaves específicas)
        plot_results = {k: v for k, v in results.items() if k not in ["Recomendações", "Simulação de Monte Carlo", "Coluna Analisada"]}
        simulated_projections = results.get("Simulação de Monte Carlo", [])

        # Verificar se os valores são numéricos
        for key, value in plot_results.items():
            if not isinstance(value, (int, float, np.integer, np.floating)):
                raise ValueError(f"O valor de '{key}' não é numérico.")

        # Informar o usuário que os gráficos serão exibidos
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Visualização", "Os resultados serão exibidos em um gráfico.")
        root.destroy()

        plt.figure(figsize=(10, 12))

        # Primeiro subplot: Gráfico de Barras
        plt.subplot(2, 1, 1)
        metrics = list(plot_results.keys())
        values = list(plot_results.values())

        # Gerar uma lista de cores dinamicamente
        colors = plt.cm.viridis(np.linspace(0, 1, len(metrics)))

        bars = plt.bar(metrics, values, color=colors)
        plt.xlabel('Métricas')
        plt.ylabel('Valores')
        plt.title('Resultados da Análise de Dados')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        if len(metrics) > 5:
            plt.xticks(rotation=45, ha='right')

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05,
                     f"{yval:.2f}", ha='center', va='bottom')

        # Segundo subplot: Box Plot da Simulação de Monte Carlo
        plt.subplot(2, 1, 2)
        if isinstance(simulated_projections, np.ndarray) and simulated_projections.size > 0:
            # Achatar o array se for multidimensional
            if simulated_projections.ndim > 1:
                simulated_projections_flat = simulated_projections.flatten()
            else:
                simulated_projections_flat = simulated_projections

            sns.boxplot(y=simulated_projections_flat, color='lightblue')
            plt.xlabel('Simulações')
            plt.ylabel('Valores Projetados')
            plt.title('Simulação de Monte Carlo - Box Plot das Projeções Futuras')
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


def plot_boxplot(data, dates, column_name, screen=None):
    """
    Gera um Box Plot com base nos dados fornecidos, mostrando os quartis.

    Parâmetros:
    - data: A coluna de dados numéricos (valores).
    - dates: As datas associadas a cada linha de dados (coluna A).
    - column_name: Nome da coluna de valores a ser exibido no gráfico.
    - screen: Objeto opcional para garantir execução na main thread (usado com Tkinter ou Pygame).
    """
    try:
        if len(data) == 0 or len(dates) == 0:
            raise ValueError("Os dados ou as datas estão vazios. Não é possível gerar o Box Plot.")

        if len(data) != len(dates):
            raise ValueError("O número de datas não corresponde ao número de valores.")

        # Verificar se estamos na main thread (por exemplo, com Tkinter)
        if screen is not None:
            # Use screen para garantir que o Box Plot seja exibido na thread correta
            screen.after(0, lambda: plot_boxplot(data, dates, column_name, screen))
            return

        # Preparar os dados para o Box Plot
        plt.figure(figsize=(10, 6))
        sns.boxplot(y=data, color='lightblue')
        plt.xlabel('Simulações')
        plt.ylabel('Valores Projetados')
        plt.title(f'Box Plot para: {column_name}')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Adicionar rótulos de dados
        quartiles = np.percentile(data, [25, 50, 75])
        mediana = quartiles[1]
        q1, q3 = quartiles[0], quartiles[2]

        plt.text(0, mediana, f'Mediana: {mediana:.2f}', horizontalalignment='center', color='black', weight='semibold')
        plt.text(0, q1, f'Q1: {q1:.2f}', horizontalalignment='center', color='blue')
        plt.text(0, q3, f'Q3: {q3:.2f}', horizontalalignment='center', color='blue')

        plt.tight_layout()
        plt.show()

        logging.info(f"Box Plot gerado com sucesso para a coluna: {column_name}")

    except Exception as e:
        logging.error(f"Erro ao gerar o Box Plot: {e}")
        print(f"Erro ao gerar o Box Plot: {e}")
        if screen:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o Box Plot:\n{e}")
            root.destroy()
