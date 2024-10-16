import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from analysis.data_import import import_file
from analysis.data_analysis import analyze_data
from visualization.plots import visualize_results
from visualization.reports import download_results
from analysis.recommendations import explain_results
from utils.helpers import draw_button, load_logo
import logging

# Configuração de logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_app():
    # Inicialização do pygame
    pygame.init()

    # Configurações da tela
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Análise de Dados - DecisionMaker")

    # Cores
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)

    # Fonte
    font = pygame.font.Font(None, 36)

    # Dimensões e posição do botão
    button_width = 350  # Aumentar a largura do botão de 250 para 350
    button_height = 50
    center_x = (screen_width - button_width) // 2

    # Carregar e redimensionar a imagem do logo
    logo_image, logo_rect = load_logo(screen_width)

    # Verificar se o logo foi carregado com sucesso
    if logo_image and logo_rect:
        # Ajustar a posição do logo
        logo_rect.top = 50  # Posição vertical do logotipo

        # Obter a altura do logotipo
        logo_height = logo_rect.height
    else:
        logo_height = 0
        # Definir logo_rect como um Rect vazio para evitar erros
        logo_rect = pygame.Rect(0, 0, 0, 0)

    # Definir uma margem entre o logotipo e o primeiro botão
    margem = 20

    # Calcular a posição vertical do primeiro botão
    primeiro_botao_y = logo_rect.top + logo_height + margem

    # Atualizar as posições dos botões
    button_y_positions = [
        primeiro_botao_y,
        primeiro_botao_y + 70,  # Espaçamento de 70 pixels entre os botões
        primeiro_botao_y + 140,
        primeiro_botao_y + 210
    ]

    running = True
    file_path = None
    results = None

    while running:
        screen.fill(black)

        # Exibir imagem do logo
        if logo_image and logo_rect:
            screen.blit(logo_image, logo_rect)

        # Renderizar botões com função personalizada
        draw_button(screen, "Importar Arquivo", center_x, button_y_positions[0],
                    button_width, button_height, green, black, font)  # Texto preto
        if results:
            draw_button(screen, "Visualizar Resultado", center_x, button_y_positions[1],
                        button_width, button_height, green, black, font)  # Texto preto
            draw_button(screen, "Baixar Resultado", center_x, button_y_positions[2],
                        button_width, button_height, green, black, font)  # Texto preto
            draw_button(screen, "Como Avaliar os Resultados", center_x, button_y_positions[3],
                        button_width, button_height, green, black, font)  # Texto preto

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Verificar se os botões foram clicados
                if center_x <= mouse_x <= center_x + button_width:
                    if button_y_positions[0] <= mouse_y <= button_y_positions[0] + button_height:
                        file_path = import_file()
                        if file_path:
                            results = analyze_data(file_path)
                    elif results and button_y_positions[1] <= mouse_y <= button_y_positions[1] + button_height:
                        visualize_results(results)
                    elif results and button_y_positions[2] <= mouse_y <= button_y_positions[2] + button_height:
                        download_results(results, file_path)
                    elif results and button_y_positions[3] <= mouse_y <= button_y_positions[3] + button_height:
                        explain_results()

    pygame.quit()
