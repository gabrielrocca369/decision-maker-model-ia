import matplotlib.pyplot as plt
import tempfile
import os
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox, filedialog
import logging
import numpy as np
import seaborn as sns  # Adicionando seaborn para o box plot

# Definir caminho para a fonte Open Sans
FONT_PATH = os.path.join('C:/Users/GabrielRocca/source/repos/games/decision-maker/assets/fonts/Open_Sans/static', 'OpenSans-Regular.ttf')

# Definir uma fonte padrão
if os.path.exists(FONT_PATH):
    plt.rcParams['font.family'] = 'Open Sans'
    plt.rcParams['pdf.fonttype'] = 42  # Para garantir que a fonte seja incorporada corretamente
else:
    logging.warning("Fonte Open Sans não encontrada. Usando fonte padrão DejaVu Sans.")
    plt.rcParams['font.family'] = 'DejaVu Sans'

def download_results(results):
    try:
        # Remover as chaves que não são valores numéricos simples
        plot_results = {k: v for k, v in results.items() if k not in ["Recomendações", "Simulação de Monte Carlo", "Coluna Analisada"]}
        simulated_projections = results.get("Simulação de Monte Carlo", [])

        # Verificar se plot_results contém apenas valores numéricos
        for key, value in plot_results.items():
            if not isinstance(value, (int, float, np.integer, np.floating)):
                raise ValueError(f"O valor de '{key}' não é numérico.")

        plt.figure(figsize=(10, 12))

        # Primeiro subplot: Gráfico de Barras
        plt.subplot(2, 1, 1)
        metrics = list(plot_results.keys())
        values = list(plot_results.values())

        # Gerar uma lista de cores dinamicamente para o número de métricas
        colors = plt.cm.viridis(np.linspace(0, 1, len(metrics)))

        bars = plt.bar(metrics, values, color=colors)
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

        # Segundo subplot: Box Plot da Simulação de Monte Carlo
        plt.subplot(2, 1, 2)
        if isinstance(simulated_projections, np.ndarray) and simulated_projections.size > 0:
            # Achatar o array se for multidimensional
            if simulated_projections.ndim > 1:
                simulated_projections_flat = simulated_projections.flatten()
            else:
                simulated_projections_flat = simulated_projections

            box_plot = sns.boxplot(y=simulated_projections_flat, color='lightblue')
            plt.xlabel('Simulações')
            plt.ylabel('Valores Projetados')
            plt.title('Simulação de Monte Carlo - Box Plot das Projeções Futuras')
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Adicionar rótulos de dados
            quartiles = np.percentile(simulated_projections_flat, [25, 50, 75])
            mediana = quartiles[1]
            q1, q3 = quartiles[0], quartiles[2]

            plt.text(0, mediana, f'Mediana: {mediana:.2f}', horizontalalignment='center', color='black', weight='semibold')
            plt.text(0, q1, f'Q1: {q1:.2f}', horizontalalignment='center', color='blue')
            plt.text(0, q3, f'Q3: {q3:.2f}', horizontalalignment='center', color='blue')
        else:
            logging.warning("Simulação de Monte Carlo não encontrada ou está vazia.")

        # Salvar o gráfico como imagem temporária
        plt.tight_layout()
        temp_dir = tempfile.gettempdir()
        chart_path = os.path.join(temp_dir, 'chart.png')
        plt.savefig(chart_path, format='png')
        plt.close()

        # Criar o PDF e adicionar o gráfico
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, txt="Resultados da Análise de Dados", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt=f"Coluna Analisada: {results['Coluna Analisada']}", ln=True)
        pdf.ln(5)

        # Adicionar as métricas no relatório
        for key, value in plot_results.items():
            pdf.cell(0, 10, txt=f"{key}: {value:.2f}", ln=True)
        pdf.ln(10)

        # Adicionar resumo da Simulação de Monte Carlo
        if isinstance(simulated_projections, np.ndarray) and simulated_projections.size > 0:
            pdf.set_font("Arial", 'B', size=14)
            pdf.cell(0, 10, txt="Resumo da Simulação de Monte Carlo:", ln=True)
            pdf.set_font("Arial", size=12)
            monte_carlo_mean = np.mean(simulated_projections_flat)
            monte_carlo_std = np.std(simulated_projections_flat)
            pdf.cell(0, 10, txt=f"Média da Simulação: {monte_carlo_mean:.2f}", ln=True)
            pdf.cell(0, 10, txt=f"Desvio Padrão da Simulação: {monte_carlo_std:.2f}", ln=True)
            pdf.ln(10)
        else:
            pdf.cell(0, 10, txt="Simulação de Monte Carlo não disponível.", ln=True)

        # Adicionar recomendações
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, txt="Recomendações:", ln=True)
        pdf.set_font("Arial", size=12)
        for rec in results.get("Recomendações", []):
            pdf.multi_cell(0, 10, txt=f"- {rec}")
        pdf.ln(10)

        # Inserir o gráfico no PDF
        pdf.image(chart_path, x=15, w=180)

        # Solicitar ao usuário um local para salvar o PDF
        root = tk.Tk()
        root.withdraw()  # Oculta a janela principal do Tkinter

        save_path = filedialog.asksaveasfilename(
            defaultextension='.pdf',
            filetypes=[('PDF Files', '*.pdf')],
            title="Salvar Relatório",
            initialfile='resultado_analise.pdf'
        )

        root.destroy()  # Destruir a janela raiz do Tkinter

        if save_path:
            # Salvar o PDF no local especificado
            pdf.output(save_path)
            # Remover a imagem temporária
            os.remove(chart_path)

            # Exibir mensagem de sucesso
            messagebox.showinfo("PDF Gerado", f"PDF gerado com sucesso e salvo em:\n{save_path}")
        else:
            # Usuário cancelou a operação de salvar
            os.remove(chart_path)
            messagebox.showinfo("Operação Cancelada", "A operação de salvar o PDF foi cancelada.")

    except Exception as e:
        logging.error(f"Erro ao baixar resultados: {e}")
        print("Erro ao baixar resultados. Verifique o log para mais detalhes.")
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", f"Ocorreu um erro ao baixar os resultados:\n{e}")
        root.destroy()
