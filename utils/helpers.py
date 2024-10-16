import pygame
import logging
import os

def draw_button(screen, text, x, y, w, h, color, text_color, font):
    pygame.draw.rect(screen, color, (x, y, w, h))
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(button_text, text_rect)

def load_logo(screen_width):
    try:
        # Definindo o caminho absoluto para o logo
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do script
        logo_path = os.path.join(current_dir, '..', '..', 'assets', 'logo.png')  # Caminho absoluto para o logo

        # Verifica se o arquivo existe
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"O arquivo {logo_path} não foi encontrado.")

        # Carrega o logo
        logo_image = pygame.image.load(logo_path)

        # Redimensiona a imagem para caber nas dimensões máximas
        max_logo_width = 600
        max_logo_height = 200
        image_width, image_height = logo_image.get_size()
        scaling_factor = min(max_logo_width / image_width, max_logo_height / image_height)
        new_width = int(image_width * scaling_factor)
        new_height = int(image_height * scaling_factor)
        logo_image = pygame.transform.scale(logo_image, (new_width, new_height))
        logo_rect = logo_image.get_rect()
        logo_rect.centerx = screen_width // 2
        return logo_image, logo_rect
    except FileNotFoundError as e:
        logging.error(f"Erro ao carregar a imagem: {e}")
        print(f"Erro ao carregar a imagem: {e}")
        return None, None
    except pygame.error as e:
        logging.error(f"Erro no Pygame ao carregar a imagem: {e}")
        print(f"Erro no Pygame ao carregar a imagem: {e}")
        return None, None
    except Exception as e:
        logging.error(f"Erro desconhecido ao carregar a imagem: {e}")
        print(f"Erro desconhecido ao carregar a imagem: {e}")
        return None, None