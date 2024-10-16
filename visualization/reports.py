import matplotlib.pyplot as plt
import tempfile
import os
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox
import logging

def download_results(results, file_path):
    try:
        # Remover as chaves "Recomendações" e "Simulação de Monte Carlo" para o gráfico de barras
        plot_results = {k: v for k, v in results.items() if k not in ["Recomendações", "Simulação de Monte Carlo"]}
        simulated_projections = results["Simulação de Monte Carlo"]

        plt.figure(figsize=(10, 12))

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
        temp_dir = tempfile.gettempdir()
        chart_path = os.path.join(temp_dir, 'chart.png')
        plt.savefig(chart_path, format='png')
        plt.close()

        # Criar o PDF e adicionar o gráfico
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(200, 10, txt="Resultados da Análise de Dados", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        for key, value in plot_results.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
        pdf.ln(10)

        # Adicionar recomendações
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(200, 10, txt="Recomendações:", ln=True)
        pdf.set_font("Arial", size=12)
        for rec in results["Recomendações"]:
            pdf.multi_cell(0, 10, txt=f"- {rec}")
        pdf.ln(10)

        # Inserir o gráfico no PDF
        pdf.image(chart_path, x=15, w=180)

        # Salvar o PDF
        output_path = os.path.join(os.path.dirname(file_path), "resultado_analise.pdf")
        pdf.output(output_path)

        # Remover a imagem temporária
        os.remove(chart_path)

        # Adicionar uma caixa de aviso ao final informando que o PDF foi gerado com sucesso
        root = tk.Tk()
        root.withdraw()  # Oculta a janela principal do Tkinter
        messagebox.showinfo("PDF Gerado", f"PDF gerado com sucesso e salvo em:\n{output_path}")

    except Exception as e:
        logging.error(f"Erro ao baixar resultados: {e}")
        print("Erro ao baixar resultados. Verifique o log para mais detalhes.")