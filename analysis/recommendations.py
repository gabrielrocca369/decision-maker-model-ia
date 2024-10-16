import tkinter as tk
from tkinter import messagebox
import logging

def generate_recommendations(mean_value, ideal_value, pareto_80_20, std_dev, future_projection):
    recommendations = []
    if future_projection > ideal_value:
        recommendations.append("A projeção futura excede o valor ideal. Considere investir mais recursos.")
    else:
        recommendations.append("A projeção futura está abaixo do valor ideal. Avalie estratégias de melhoria.")
    if std_dev > (0.1 * mean_value):
        recommendations.append("Alta variabilidade nos dados. Considere padronizar os processos.")
    else:
        recommendations.append("Variabilidade aceitável nos dados.")
    return recommendations

def explain_results():
    try:
        root = tk.Tk()
        root.withdraw()
        explanation = (
            "Como Avaliar os Resultados:\n\n"
            "Média:\n"
            "A média representa o valor médio dos dados analisados. No contexto de tráfego e comportamento, "
            "pode indicar o número médio de visualizações, taxa média de abertura, etc.\n\n"
            "Maior Valor:\n"
            "O maior valor encontrado no conjunto de dados. Pode indicar o pico de visualizações ou a maior taxa "
            "de engajamento registrada.\n\n"
            "Menor Valor:\n"
            "O menor valor encontrado no conjunto de dados. Pode indicar o menor número de visualizações ou a menor "
            "taxa de abertura.\n\n"
            "Valor Ideal (Proporção Áurea):\n"
            "Um valor teórico obtido multiplicando a média pela Proporção Áurea (1.618). Pode servir como uma meta "
            "ideal para alcançar nos indicadores analisados.\n\n"
            "Pareto 80/20:\n"
            "Corresponde ao percentil 80 dos dados. Indica que 80% dos resultados estão abaixo deste valor. Útil para "
            "identificar os principais períodos ou campanhas que geraram a maior parte do tráfego ou engajamento.\n\n"
            "Desvio Padrão:\n"
            "Mede a dispersão dos dados em relação à média. Um desvio padrão alto indica grande variabilidade, "
            "enquanto um desvio padrão baixo indica consistência nos resultados.\n\n"
            "Projeção Futura:\n"
            "Estimativa do próximo valor com base na tendência atual dos dados. Pode ajudar a prever o desempenho "
            "futuro em termos de visualizações, engajamento, etc.\n\n"
            "Simulação de Monte Carlo:\n"
            "Método estatístico que utiliza a aleatoriedade para estimar a incerteza nos resultados futuros. A simulação "
            "gera uma distribuição de possíveis projeções futuras, permitindo entender a gama de resultados possíveis e "
            "suas probabilidades.\n\n"
            "Exemplo Prático:\n"
            "Ao analisar a taxa de engajamento em campanhas de marketing, a Simulação de Monte Carlo pode ajudar a "
            "prever a probabilidade de alcançar determinadas metas de engajamento, considerando a variabilidade histórica "
            "dos dados."
        )
        messagebox.showinfo("Como Avaliar os Resultados", explanation)
    except Exception as e:
        logging.error(f"Erro ao exibir explicação: {e}")
        print("Erro ao exibir explicação. Verifique o log para mais detalhes.")
