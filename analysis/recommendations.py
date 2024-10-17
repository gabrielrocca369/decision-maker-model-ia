import pygame
import logging
import os

# Caminho para a fonte Open Sans
FONT_PATH = os.path.join('C:/Users/GabrielRocca/source/repos/games/decision-maker/assets/fonts/Open_Sans/static', 'OpenSans-Regular.ttf')

def generate_recommendations(mean_value, ideal_value, tension_value, pareto_80_20, std_dev, future_projection, cagr=None, skewness=0, coef_var=None):
    try:
        recommendations = []

        # Verificar se os valores numéricos são válidos
        if mean_value is None or ideal_value is None or std_dev is None or future_projection is None:
            raise ValueError("Um ou mais parâmetros numéricos são inválidos ou nulos.")

        if mean_value == 0:
            raise ValueError("A média não pode ser zero ao calcular recomendações.")

        # Recomendações baseadas na projeção futura e valor ideal
        if future_projection > ideal_value:
            recommendations.append("A projeção futura excede o valor ideal. Considere investir mais recursos.")
        else:
            recommendations.append("A projeção futura está abaixo do valor ideal. Avalie estratégias de melhoria.")

        # Recomendações baseadas no desvio padrão e média
        if std_dev > (0.1 * mean_value):
            recommendations.append("Alta variabilidade nos dados. Considere padronizar os processos.")
        else:
            recommendations.append("Variabilidade aceitável nos dados.")

        # Recomendações com base no coeficiente de variação (se aplicável)
        if coef_var is not None:
            if coef_var > 20:
                recommendations.append("O coeficiente de variação é alto, indicando uma alta volatilidade nos dados.")
            else:
                recommendations.append("O coeficiente de variação está em um nível aceitável.")

        # Recomendações com base na análise de assimetria
        if abs(skewness) > 1:
            recommendations.append("Os dados apresentam alta assimetria. Considere transformar os dados ou ajustar sua análise para acomodar esse fator.")

        # Recomendações baseadas no valor de tensão
        if future_projection < tension_value:
            recommendations.append("A projeção futura está abaixo do valor de tensão. Avalie uma estratégia conservadora ou ajuste suas metas.")

        # Recomendações com base no CAGR (se aplicável)
        if cagr is not None:
            if cagr > 10:
                recommendations.append("A taxa de crescimento composta (CAGR) é alta. Considere manter ou expandir as estratégias atuais.")
            else:
                recommendations.append("A taxa de crescimento composta (CAGR) é baixa. Avalie novas estratégias de crescimento.")

        return recommendations

    except Exception as e:
        logging.error(f"Erro ao gerar recomendações: {e}", exc_info=True)
        print(f"Erro ao gerar recomendações: {e}")
        return ["Não foi possível gerar recomendações devido a um erro nos dados fornecidos."]


def explain_results(screen):
    try:
        # Definir o texto da explicação
        explanation = (
            "**Como Avaliar os Resultados:**\n\n"
            "**Média:**\n"
            "Pode indicar o número médio de visualizações, taxa média de abertura, etc. Comparar a média entre diferentes períodos pode ajudar a entender a tendência geral de crescimento ou queda no desempenho.\n\n"
            "**Maior Valor:**\n"
            "Pode indicar o pico de visualizações ou a maior taxa de engajamento registrada. Esse valor é útil para identificar campanhas ou conteúdos que tiveram desempenho excepcional.\n\n"
            "**Menor Valor:**\n"
            "Pode indicar o menor número de visualizações ou a menor taxa de abertura. Útil para entender os pontos baixos e avaliar o que pode ter causado baixo desempenho.\n\n"
            "**Valor Ideal (Proporção Áurea):**\n"
            "Um valor teórico obtido multiplicando a média pela Proporção Áurea (1.618). Pode servir como uma meta ideal para alcançar nos KPI's analisados. Comparar o valor atual com o valor ideal ajuda a definir metas ambiciosas, mas possíveis.\n\n"
            "**Pareto 80/20:**\n"
            "Corresponde ao percentil 80 dos dados. Indica que 80% dos resultados estão abaixo deste valor. Útil para identificar os principais dados que geraram a maior parte do tráfego ou engajamento, permitindo priorizar ações nas áreas que geram maior impacto.\n\n"
            "**Desvio Padrão:**\n"
            "Mede a dispersão dos dados em relação à média. Um desvio padrão alto indica grande variabilidade, enquanto um desvio padrão baixo indica consistência nos resultados. Use o desvio padrão para avaliar a estabilidade das métricas e identificar possíveis outliers.\n\n"
            "**Projeção Futura:**\n"
            "Estimativa do próximo valor com base na tendência atual dos dados. Pode ajudar a prever o desempenho futuro em termos de visualizações, engajamento, etc. Comparar a projeção futura com metas definidas auxilia na tomada de decisões estratégicas.\n\n"
            "**Coeficiente de Variação:**\n"
            "Mede a variabilidade relativa dos dados. Um coeficiente de variação alto indica maior volatilidade e incerteza nos resultados. Comparar o coeficiente de variação entre diferentes campanhas pode ajudar a identificar quais delas foram mais consistentes.\n\n"
            "**Simulação de Monte Carlo:**\n"
            "Método estatístico que utiliza a aleatoriedade para estimar a incerteza nos resultados futuros. A simulação gera uma distribuição de possíveis projeções futuras, permitindo entender a gama de resultados possíveis e suas probabilidades. Útil para avaliar riscos e definir estratégias que sejam robustas diante da incerteza.\n\n"
            "**CAGR (Taxa de Crescimento Composta):**\n"
            "Mede o crescimento médio anual composto ao longo do tempo. Útil para avaliar o desempenho em séries temporais. Comparar o CAGR entre diferentes períodos pode ajudar a identificar se o crescimento está acelerando, desacelerando ou permanecendo constante.\n\n"
            "**Exemplos Práticos:**\n"
            "**1. Comparação de Campanhas:** Ao analisar a taxa de engajamento de diferentes campanhas, o desvio padrão pode ser usado para determinar qual campanha teve o desempenho mais consistente, enquanto o Pareto 80/20 pode indicar quais campanhas foram responsáveis pela maior parte do engajamento.\n\n"
            "**2. Definição de Metas:** Use a Proporção Áurea e a Projeção Futura para definir metas realistas, mas desafiadoras, que levem em conta o histórico de desempenho.\n\n"
            "**3. Análise de Volatilidade:** O coeficiente de variação pode ser comparado entre diferentes períodos para avaliar a estabilidade dos resultados. Se uma campanha tiver alta volatilidade, pode ser necessário investigar e mitigar fatores externos que afetaram o desempenho.\n\n"
            "**4. Previsão de Desempenho Futuro:** A Simulação de Monte Carlo pode ser utilizada para prever a probabilidade de alcançar determinadas metas de engajamento, ajudando na alocação de recursos para campanhas futuras."
        )

        # Definir fonte e cores
        try:
            font_regular = pygame.font.Font(FONT_PATH, 24)  # Fonte regular Open Sans
            font_bold = pygame.font.Font(FONT_PATH, 24)  # Fonte para negrito Open Sans (simulando negrito)
        except FileNotFoundError:
            logging.error("Fonte Open Sans não encontrada. Certifique-se de que o caminho está correto.")
            font_regular = pygame.font.Font(None, 24)
            font_bold = pygame.font.Font(None, 24)

        font_bold.set_bold(True)  # Aplicando o negrito
        background_color = (0, 0, 0)  # Preto
        text_color = (248, 248, 242)  # Cor do texto regular
        title_color = (0, 200, 0)  # Verde para os títulos
        border_color = (248, 248, 242)  # Cor da borda
        border_radius = 15  # Raio dos cantos arredondados

        # Criar uma superfície para exibir o texto com margem
        screen_width, screen_height = screen.get_size()
        padding = 18  # Espaçamento interno
        explanation_width = screen_width - 2 * padding
        explanation_surface = pygame.Surface((explanation_width, 10000))  # Definindo uma altura alta para permitir a rolagem
        explanation_surface.fill(background_color)

        # Função para quebrar linhas automaticamente com base na largura da tela
        def wrap_text(text, font, max_width):
            words = text.split(' ')
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                text_width, _ = font.size(test_line)

                if text_width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "

            lines.append(current_line)  # Adicionar a última linha
            return lines

        # Dividir o texto em linhas e renderizar
        y_offset = padding
        for paragraph in explanation.split('\n\n'):
            for line in paragraph.split('\n'):
                if line.startswith("**") and line.endswith("**"):  # Detectar títulos
                    wrapped_lines = wrap_text(line[2:-2], font_bold, explanation_width - 2 * padding)
                    for wrapped_line in wrapped_lines:
                        text_surface = font_bold.render(wrapped_line, True, title_color)
                        explanation_surface.blit(text_surface, (padding, y_offset))
                        y_offset += font_bold.get_height() + 5  # Espaçamento entre linhas
                else:
                    wrapped_lines = wrap_text(line, font_regular, explanation_width - 2 * padding)
                    for wrapped_line in wrapped_lines:
                        text_surface = font_regular.render(wrapped_line, True, text_color)
                        explanation_surface.blit(text_surface, (padding, y_offset))
                        y_offset += font_regular.get_height() + 5  # Espaçamento entre linhas

        # Desenhar uma borda ao redor da superfície de explicação
        pygame.draw.rect(explanation_surface, border_color, explanation_surface.get_rect(), width=2, border_radius=border_radius)

        # Configuração de rolagem
        scroll_y = 0
        scroll_speed = 20  # Velocidade de rolagem

        # Loop para exibir a explicação e permitir rolagem
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_DOWN:
                        scroll_y = min(scroll_y + scroll_speed, explanation_surface.get_height() - screen_height)
                    elif event.key == pygame.K_UP:
                        scroll_y = max(scroll_y - scroll_speed, 0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            # Desenhar o fundo escurecido
            dim_overlay = pygame.Surface((screen_width, screen_height))
            dim_overlay.set_alpha(150)  # Transparência
            dim_overlay.fill((0, 0, 0))
            screen.blit(dim_overlay, (0, 0))

            # Desenhar a superfície da explicação sobre a tela principal
            screen.blit(explanation_surface, (padding, -scroll_y))
            pygame.display.flip()

    except Exception as e:
        logging.error(f"Erro ao exibir explicação: {e}", exc_info=True)
        print("Erro ao exibir explicação. Verifique o log para mais detalhes.")
