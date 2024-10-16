import pygame
import logging

def generate_recommendations(mean_value, ideal_value, pareto_80_20, std_dev, future_projection, skewness=0):
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

        # Recomendações com base na análise de assimetria
        if abs(skewness) > 1:
            recommendations.append("Os dados apresentam alta assimetria. Considere transformar os dados ou ajustar sua análise para acomodar esse fator.")

        return recommendations

    except Exception as e:
        logging.error(f"Erro ao gerar recomendações: {e}", exc_info=True)
        print(f"Erro ao gerar recomendações: {e}")
        return ["Não foi possível gerar recomendações devido a um erro nos dados fornecidos."]

def explain_results(screen):
    try:
        # Definir o texto da explicação
        explanation = (
            "Como Avaliar os Resultados:\n\n"
            "Média:\n"
            "Pode indicar o número médio de visualizações, taxa média de abertura, etc.\n\n"
            "Maior Valor:\n"
            "Pode indicar o pico de visualizações ou a maior taxa de engajamento registrada.\n\n"
            "Menor Valor:\n"
            "Pode indicar o menor número de visualizações ou a menor taxa de abertura.\n\n"
            "Valor Ideal (Proporção Áurea):\n"
            "Um valor teórico obtido multiplicando a média pela Proporção Áurea (1.618)."
            "Pode servir como uma meta ideal para alcançar nos KPI's analisados.\n\n"
            "Pareto 80/20:\n"
            "Corresponde ao percentil 80 dos dados. Indica que 80% dos resultados estão abaixo deste valor. "
            "Útil para identificar os principais dados que geraram a maior parte do tráfego ou engajamento.\n\n"
            "Desvio Padrão:\n"
            "Mede a dispersão dos dados em relação à média. Um desvio padrão alto indica grande variabilidade, "
            "enquanto um desvio padrão baixo indica consistência nos resultados.\n\n"
            "Projeção Futura:\n"
            "Estimativa do próximo valor com base na tendência atual dos dados. Pode ajudar a prever o desempenho "
            "futuro em termos de visualizações, engajamento, etc.\n\n"
            "Simulação de Monte Carlo:\n"
            "Método estatístico que utiliza a aleatoriedade para estimar a incerteza nos resultados futuros. "
            "A simulação gera uma distribuição de possíveis projeções futuras, permitindo entender a gama "
            "de resultados possíveis e suas probabilidades.\n\n"
            "Exemplo Prático:\n"
            "Ao analisar a taxa de engajamento em campanhas de comunicação, a Simulação de Monte Carlo pode ajudar a "
            "prever a probabilidade de alcançar metas de engajamento, considerando a variabilidade histórica dos dados."
        )

        # Definir fonte e cores
        font = pygame.font.Font(None, 16)
        background_color = (0, 0, 0)  # Preto
        text_color = (248, 248, 242)  # Cor do texto (mesma da borda dos botões)
        border_color = (248, 248, 242)  # Cor da borda
        border_radius = 15  # Raio dos cantos arredondados

        # Criar uma superfície para exibir o texto com margem
        screen_width, screen_height = screen.get_size()
        padding = 20  # Espaçamento interno
        explanation_width = screen_width - 2 * padding
        explanation_height = screen_height - 2 * padding
        explanation_surface = pygame.Surface((explanation_width, explanation_height))
        explanation_surface.fill(background_color)

        # Dividir o texto em linhas
        lines = []
        for paragraph in explanation.split('\n\n'):
            for line in paragraph.split('\n'):
                # Quebra de linha automática se a linha for muito longa
                words = line.split(' ')
                line_buffer = ''
                for word in words:
                    test_line = line_buffer + word + ' '
                    text_width, _ = font.size(test_line)
                    if text_width < explanation_width - 2 * padding:
                        line_buffer = test_line
                    else:
                        lines.append(line_buffer)
                        line_buffer = word + ' '
                lines.append(line_buffer)
            lines.append('')  # Linha em branco entre parágrafos

        # Renderizar cada linha de texto
        y_offset = padding
        for line in lines:
            text_surface = font.render(line, True, text_color)
            explanation_surface.blit(text_surface, (padding, y_offset))
            y_offset += font.get_height() + 5  # Espaçamento entre linhas

        # Desenhar uma borda ao redor da superfície de explicação
        pygame.draw.rect(explanation_surface, border_color, explanation_surface.get_rect(), width=2, border_radius=border_radius)

        # Posicionar a superfície no centro da tela
        explanation_rect = explanation_surface.get_rect(center=(screen_width // 2, screen_height // 2))

        # Loop para exibir a explicação e aguardar o usuário fechar
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            # Desenhar o fundo escurecido
            dim_overlay = pygame.Surface((screen_width, screen_height))
            dim_overlay.set_alpha(150)  # Transparência
            dim_overlay.fill((0, 0, 0))
            screen.blit(dim_overlay, (0, 0))

            # Desenhar a superfície da explicação sobre a tela principal
            screen.blit(explanation_surface, explanation_rect)
            pygame.display.flip()

    except Exception as e:
        logging.error(f"Erro ao exibir explicação: {e}", exc_info=True)
        print("Erro ao exibir explicação. Verifique o log para mais detalhes.")
