import pygame
import logging
import os

# Caminho para a fonte Open Sans
FONT_PATH = os.path.join('C:/Users/GabrielRocca/source/repos/games/decision-maker/assets/fonts/Open_Sans/static', 'OpenSans-Regular.ttf')


def generate_recommendations(mean_value, ideal_value, tension_value, pareto_80_20, std_dev, future_projection, cagr=None, skewness=0, coef_var=None):
    """
    Gera recomendações baseadas nas métricas fornecidas.

    Parâmetros:
    - mean_value (float): Média das visualizações.
    - ideal_value (float): Valor ideal calculado (Proporção Áurea).
    - tension_value (float): Valor de tensão calculado.
    - pareto_80_20 (float): Valor baseado na análise Pareto 80/20.
    - std_dev (float): Desvio padrão das visualizações.
    - future_projection (float): Projeção futura das visualizações.
    - cagr (float, opcional): Taxa de Crescimento Anual Composta.
    - skewness (float, opcional): Assimetria dos dados.
    - coef_var (float, opcional): Coeficiente de variação.

    Retorna:
    - recommendations (list): Lista de recomendações.
    """
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
    """
    Exibe explicações detalhadas sobre as métricas utilizando pygame.

    Parâmetros:
    - screen (pygame.Surface): Superfície do pygame onde o texto será exibido.
    """
    try:
        # Definir o texto da explicação
        explanation = ( 
            "**Como Avaliar os Resultados:**\n\n"
            "**Média:**\n"
            "Pode indicar o número médio de visualizações, taxa média de abertura, etc. Comparar a média entre diferentes períodos pode ajudar a entender a tendência geral de crescimento ou queda no desempenho. Um valor alto indica bom desempenho, enquanto um valor baixo pode sugerir necessidade de melhorias.\n\n"
            "**Mediana:**\n"
            "A mediana representa o valor central dos dados ordenados. Ela é útil para evitar distorções causadas por valores extremos. Se a mediana for próxima da média, os dados são relativamente simétricos; se houver grande diferença, pode indicar a presença de outliers.\n\n"
            "**Maior Valor:**\n"
            "Indica o pico de visualizações ou a maior taxa de engajamento registrada. Um valor alto é geralmente positivo, mostrando um momento de sucesso. Analise este valor para identificar o que levou a tal desempenho e replicar as boas práticas.\n\n"
            "**Menor Valor:**\n"
            "Indica o valor mais baixo observado, como o menor número de visualizações. Um valor baixo pode sinalizar períodos ou campanhas menos eficazes. Identificar os motivos ajuda a evitar repetir esses problemas.\n\n"
            "**Valor Ideal (Fibonacci):**\n"
            "Valor teórico obtido multiplicando a média pela Proporção Áurea (1.618). Serve como uma meta ambiciosa, mas realista, a ser alcançada. Se o valor atual estiver próximo do valor ideal, isso sugere bom desempenho em relação ao potencial teórico.\n\n"
            "**Valor de Tensão:**\n"
            "Representa um limite inferior crítico, abaixo do qual o desempenho é preocupante. Se a projeção futura estiver abaixo do valor de tensão, isso indica que é necessário agir rapidamente para evitar consequências negativas.\n\n"
            "**Pareto 80/20:**\n"
            "Corresponde ao percentil 80 dos dados. Indica que 80% dos resultados estão abaixo deste valor. É útil para entender onde concentrar esforços — os 20% principais tendem a gerar a maior parte dos resultados.\n\n"
            "**Desvio Padrão:**\n"
            "Mede a dispersão dos dados em relação à média. Um desvio padrão alto indica grande variabilidade, o que pode ser sinal de inconsistência nos resultados. Um desvio padrão baixo sugere resultados mais previsíveis e consistentes.\n\n"
            "**Coeficiente de Variação:**\n"
            "Mede a variabilidade relativa dos dados. Um coeficiente de variação alto indica alta volatilidade, sugerindo incerteza. Valores baixos indicam maior consistência. É útil comparar campanhas para ver qual foi mais estável.\n\n"
            "**Projeção Futura:**\n"
            "Estimativa do valor futuro com base nas tendências atuais. Valores altos indicam um crescimento esperado, enquanto valores baixos podem sugerir necessidade de mudanças estratégicas.\n\n"
            "**CAGR (Taxa de Crescimento Composta):**\n"
            "Mede o crescimento médio anual composto ao longo do tempo. Um CAGR alto é indicativo de crescimento constante, enquanto um valor baixo pode significar estagnação ou declínio.\n\n"
            "**Média da Simulação de Monte Carlo:**\n"
            "A média dos resultados da simulação de Monte Carlo representa uma previsão centralizada do desempenho futuro, levando em consideração a incerteza. Valores próximos à média indicam consistência, enquanto desvios grandes sugerem cenários variados.\n\n"
            "**Desvio Padrão da Simulação Monte Carlo:**\n"
            "Indica a variabilidade dos resultados simulados. Um desvio padrão alto sugere um futuro mais incerto, enquanto um valor baixo indica previsões mais consistentes.\n\n"
            "**Recomendações:**\n"
            "Baseadas nas métricas analisadas, como investir mais em áreas com projeção alta, ou padronizar processos em caso de alta variabilidade. Boas recomendações ajudam a maximizar resultados e minimizar riscos.\n\n"
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
        logging.error(f"Erro ao exibir resultados: {e}", exc_info=True)
        print(f"Erro ao exibir resultados: {e}")