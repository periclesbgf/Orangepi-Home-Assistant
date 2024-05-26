from ..main import pygame_menu
import sys
import matplotlib.pyplot as plt
import numpy as np
from button import Button


current_language_index = 0
Fullscreen = 0
current_resolution_index = 3
resolutions = [(640, 480), (800, 600), (1024, 600), (1280, 720), (1920, 1080), "Fullscreen"]
screen_resolution = pygame_menu.display.set_mode((1024, 600), pygame_menu.FULLSCREEN)
#screen_resolution = pygame_menu.display.set_mode((1024, 600))
pygame_menu.display.set_caption("Eden")
pygame_menu.mouse.set_visible(False)

BG = pygame_menu.image.load("assets/fundoeden2.png")

def get_font(size): 
    return pygame_menu.font.Font("assets/LucidaTypewriterBold.ttf", size)

def draw_horizontal_line(color):
    pygame_menu.draw.line(screen_resolution, color, (0, screen_resolution.get_height() / 1.3), (screen_resolution.get_width(), screen_resolution.get_height() / 1.3), 5)

def check_selection_resolution(mouse_pos, y_offset_start, num_items):
    y_offset = y_offset_start
    for i in range(num_items):
        # Coordenadas atualizadas da caixa de seleção
        checkbox_x = screen_resolution.get_width() / 2 - 150
        checkbox_y = y_offset
        checkbox_rect = pygame_menu.Rect(checkbox_x, checkbox_y, 20, 20)
        if checkbox_rect.collidepoint(mouse_pos):
            return i
        y_offset += 40
    return -1

def check_selection_language(mouse_pos, y_offset_start):
    y_offset = y_offset_start
    for i in range(2):
        # Coordenadas da caixa de seleção
        checkbox_x = screen_resolution.get_width() / 2 - 150
        checkbox_y = y_offset
        checkbox_rect = pygame_menu.Rect(checkbox_x, checkbox_y, 20, 20)
        if checkbox_rect.collidepoint(mouse_pos):
            return i
        y_offset += 40
    return -1


    

# Adicione uma variável global para rastrear o estado do botão on/off
on_off_state = False
on_off_state_geladeira = False
on_off_state_cafeteira = False
on_off_state_chuveiro = False
on_off_state_termometro = False
on_off_state_sensor = False

def draw_on_off_button(x, y, state):
    # Define as coordenadas e o tamanho do botão
    button_rect = pygame_menu.Rect(x, y, 70, 35)
    # Determina a cor com base no estado atual
    button_color = (0, 255, 0) if state else (255, 0, 0)
    # Desenha o botão
    pygame_menu.draw.rect(screen_resolution, button_color, button_rect)
    # Adiciona o texto "ON" ou "OFF" ao botão
    font = get_font(30)
    text = font.render("ON" if state else "OFF", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen_resolution.blit(text, text_rect)

def toggle_on_off_button_geladeira():
    global on_off_state_geladeira
    # Alterna o estado do botão da geladeira
    on_off_state_geladeira = not on_off_state_geladeira

def toggle_on_off_button_cafeteira():
    global on_off_state_cafeteira
    # Alterna o estado do botão da cafeteira
    on_off_state_cafeteira = not on_off_state_cafeteira

def toggle_on_off_button_chuveiro():
    global on_off_state_chuveiro
    # Alterna o estado do botão do chuveiro
    on_off_state_chuveiro = not on_off_state_chuveiro

def toggle_on_off_button_termometro():
    global on_off_state_termometro
    # Alterna o estado do botão do termômetro
    on_off_state_termometro = not on_off_state_termometro

def toggle_on_off_button_sensor():
    global on_off_state_sensor
    # Alterna o estado do botão do sensor
    on_off_state_sensor = not on_off_state_sensor

def draw_notification(screen_resolution, message):
    # Cria uma superfície para a notificação
    notification_surface = pygame_menu.Surface((500, 170))
    notification_surface.fill((200, 200, 200))

    # Renderiza o texto
    font = get_font(20)
    text_surface = font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(250, 50))
    notification_surface.blit(text_surface, text_rect)

    # Desenha o botão "Sair"
    button_rect = pygame_menu.Rect(200, 100, 100, 50)
    pygame_menu.draw.rect(notification_surface, (255, 0, 0), button_rect)
    button_text_surface = font.render("Sim", True, (255, 255, 255))
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)
    notification_surface.blit(button_text_surface, button_text_rect)

    # Define a posição da notificação no canto superior esquerdo da tela
    notification_position = (20, 20)  # Pequeno deslocamento para não ficar colado no canto
    notification_rect = notification_surface.get_rect(topleft=notification_position)

    # Desenha a notificação na tela
    screen_resolution.blit(notification_surface, notification_rect)

    return button_rect.move(notification_rect.topleft)  # Retorna a posição real do botão na tela

def main_menu(current_language_index):
    line_color = pygame_menu.Color('black')
    color_timer = 0
    show_notification = False
    notification_start_time = 0
    notification_duration = 10000  # duração da notificação em segundos
    button_rect = None
    
    while True:
        MENU_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.blit(BG, (0, 0))

        MENU_TEXT = get_font(125).render("EDEN", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 4.5))

        draw_horizontal_line(line_color)
        if(current_language_index == 0):
            DISPOSITIVOS_BUTTON = Button(image=pygame_menu.image.load("assets/dispositivosrect.png"), pos=(screen_resolution.get_width() * 0.40, screen_resolution.get_height() / 2), 
                                text_input="Dispositivos", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
            CONFIG_BUTTON = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/settings.png"), (75,75)), pos=(screen_resolution.get_width() * 0.045, screen_resolution.get_height() / 1.080), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")  # Ícone de engrenagem, sem texto
            HISTORY_BUTTON = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/iconehistorico.png"), (75,75)), pos=(screen_resolution.get_width() * 0.960, screen_resolution.get_height() / 1.080), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White") 
            QUIT_BUTTON = Button(image=pygame_menu.image.load("assets/Sair.png"), pos=(screen_resolution.get_width() * 0.70, screen_resolution.get_height() / 2), 
                                text_input="Sair", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
            
        elif(current_language_index == 1):
            DISPOSITIVOS_BUTTON = Button(image=pygame_menu.image.load("assets/dispositivosrect.png"), pos=(screen_resolution.get_width() * 0.40, screen_resolution.get_height() / 2), 
                                text_input="Devices", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
            CONFIG_BUTTON = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/settings.png"), (75,75)), pos=(screen_resolution.get_width() * 0.045, screen_resolution.get_height() / 1.080), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")  # Ícone de engrenagem, sem texto
            HISTORY_BUTTON = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/iconehistorico.png"), (75,75)), pos=(screen_resolution.get_width() * 0.960, screen_resolution.get_height() / 1.080), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White") 
            QUIT_BUTTON = Button(image=pygame_menu.image.load("assets/Sair.png"), pos=(screen_resolution.get_width() * 0.70, screen_resolution.get_height() / 2), 
                                text_input="Quit", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        screen_resolution.blit(MENU_TEXT, MENU_RECT)

        for button in [DISPOSITIVOS_BUTTON, CONFIG_BUTTON, QUIT_BUTTON, HISTORY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen_resolution)
        
        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.KEYDOWN:
                if event.key == pygame_menu.K_ESCAPE:
                    pygame_menu.quit()
                    sys.exit()
                elif event.key == pygame_menu.K_1:
                    line_color = pygame_menu.Color('BLUE')
                    color_timer = pygame_menu.time.get_ticks()
                elif event.key == pygame_menu.K_2:
                    toggle_on_off_button_geladeira()
                    show_notification = True
                    notification_start_time = pygame_menu.time.get_ticks()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if show_notification and button_rect and button_rect.collidepoint(event.pos):
                    play(current_language_index)
                if DISPOSITIVOS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(current_language_index)
                if CONFIG_BUTTON.checkForInput(MENU_MOUSE_POS):
                    config(current_language_index)
                if HISTORY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    history(current_language_index)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame_menu.quit()
                    sys.exit()
        if show_notification:
            current_time = pygame_menu.time.get_ticks()
            if current_time - notification_start_time < notification_duration:
                button_rect = draw_notification(screen_resolution, "Dispositivo ativado! Deseja conferir?")
            else:
                show_notification = False  # Oculta a notificação após a duração especificada

        if pygame_menu.time.get_ticks() - color_timer >= 4000:
            line_color = pygame_menu.Color('black')

        pygame_menu.display.update()

def play(current_language_index):
    line_color = pygame_menu.Color('black')
    color_timer = 0
    
    while True:
        PLAY_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")

        draw_horizontal_line(line_color)

        # Definindo a posição central dos botões
        button_x = screen_resolution.get_width() / 2 - 200  # Ajuste para centralizar horizontalmente
        button_y_start = screen_resolution.get_height() / 2 - 180  # Ajuste para centralizar verticalmente e espaço entre os botões

        if (current_language_index == 0):

            PLAY_TEXT = get_font(75).render("Dispositivos", True, "Black")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 11))
            screen_resolution.blit(PLAY_TEXT, PLAY_RECT)
            # Desenha o botão on/off para a geladeira
            draw_on_off_button(button_x, button_y_start, on_off_state_geladeira)
            geladeira_text = get_font(40).render("Luminaria", True, (0, 0, 0))
            screen_resolution.blit(geladeira_text, (button_x + 90, button_y_start - 5))

            # Desenha o botão on/off para a cafeteira
            draw_on_off_button(button_x, button_y_start + 70, on_off_state_cafeteira)
            cafeteira_text = get_font(40).render("Bomba d'água", True, (0, 0, 0))
            screen_resolution.blit(cafeteira_text, (button_x + 90, button_y_start + 65))

            # Desenha o botão on/off para o chuveiro
            draw_on_off_button(button_x, button_y_start + 140, on_off_state_chuveiro)
            chuveiro_text = get_font(40).render("Porta", True, (0, 0, 0))
            screen_resolution.blit(chuveiro_text, (button_x + 90, button_y_start + 140))

            # Desenha o botão on/off para o termômetro
            draw_on_off_button(button_x, button_y_start + 210, on_off_state_termometro)
            termometro_text = get_font(40).render("Luz", True, (0, 0, 0))
            screen_resolution.blit(termometro_text, (button_x + 90, button_y_start + 210))

            # Desenha o botão on/off para o sensor
            draw_on_off_button(button_x, button_y_start + 280, on_off_state_sensor)
            sensor_text = get_font(40).render("Válvula", True, (0, 0, 0))
            screen_resolution.blit(sensor_text, (button_x + 90, button_y_start + 280))

            PLAY_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 1.2), 
                                text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="Green")
            
        elif (current_language_index == 1):

            PLAY_TEXT = get_font(75).render("Devices", True, "Black")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 11))
            screen_resolution.blit(PLAY_TEXT, PLAY_RECT)
            # Desenha o botão on/off para a geladeira
            draw_on_off_button(button_x, button_y_start, on_off_state_geladeira)
            geladeira_text = get_font(40).render("Fridge", True, (0, 0, 0))
            screen_resolution.blit(geladeira_text, (button_x + 90, button_y_start - 5))

            # Desenha o botão on/off para a cafeteira
            draw_on_off_button(button_x, button_y_start + 70, on_off_state_cafeteira)
            cafeteira_text = get_font(40).render("Coffee", True, (0, 0, 0))
            screen_resolution.blit(cafeteira_text, (button_x + 90, button_y_start + 65))

            # Desenha o botão on/off para o chuveiro
            draw_on_off_button(button_x, button_y_start + 140, on_off_state_chuveiro)
            chuveiro_text = get_font(40).render("Shower", True, (0, 0, 0))
            screen_resolution.blit(chuveiro_text, (button_x + 90, button_y_start + 140))

            # Desenha o botão on/off para o termômetro
            draw_on_off_button(button_x, button_y_start + 210, on_off_state_termometro)
            termometro_text = get_font(40).render("Thermometer", True, (0, 0, 0))
            screen_resolution.blit(termometro_text, (button_x + 90, button_y_start + 210))

            # Desenha o botão on/off para o sensor
            draw_on_off_button(button_x, button_y_start + 280, on_off_state_sensor)
            sensor_text = get_font(40).render("Sensor", True, (0, 0, 0))
            screen_resolution.blit(sensor_text, (button_x + 90, button_y_start + 280))

            PLAY_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 1.2), 
                                text_input="Back", font=get_font(75), base_color="Black", hovering_color="Green")
        
        SETTINGS_GELADEIRA = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/info.png"), (48,48)), pos=(screen_resolution.get_width() / 1.40, screen_resolution.get_height() / 4.3), 
                            text_input="", font=get_font(75), base_color="Black", hovering_color="Green")
        
        SETTINGS_CAFETEIRA = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/info.png"), (48,48)), pos=(screen_resolution.get_width() / 1.40, screen_resolution.get_height() / 2.80), 
                            text_input="", font=get_font(75), base_color="Black", hovering_color="Green")
        
        SETTINGS_CHUVEIRO = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/info.png"), (48,48)), pos=(screen_resolution.get_width() / 1.40, screen_resolution.get_height() / 2.1), 
                            text_input="", font=get_font(75), base_color="Black", hovering_color="Green")
        SETTINGS_TERMOMETRO = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/info.png"), (48,48)), pos=(screen_resolution.get_width() / 1.40, screen_resolution.get_height() / 1.70), 
                            text_input="", font=get_font(75), base_color="Black", hovering_color="Green")
        SETTINGS_SENSOR = Button(image=pygame_menu.transform.scale(pygame_menu.image.load("assets/info.png"), (48,48)), pos=(screen_resolution.get_width() / 1.40, screen_resolution.get_height() / 1.42), 
                            text_input="", font=get_font(75), base_color="Black", hovering_color="Green")

        for button in [PLAY_BACK, SETTINGS_GELADEIRA, SETTINGS_CAFETEIRA, SETTINGS_CHUVEIRO, SETTINGS_TERMOMETRO, SETTINGS_SENSOR]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(screen_resolution)

        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.KEYDOWN:
                if event.key == pygame_menu.K_1:
                    line_color = pygame_menu.Color('BLUE')
                    color_timer = pygame_menu.time.get_ticks()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu(current_language_index)
                if SETTINGS_GELADEIRA.checkForInput(PLAY_MOUSE_POS):
                    options(current_language_index)
                if SETTINGS_CAFETEIRA.checkForInput(PLAY_MOUSE_POS):
                    options(current_language_index)
                if SETTINGS_CHUVEIRO.checkForInput(PLAY_MOUSE_POS):
                    options(current_language_index)
                if SETTINGS_TERMOMETRO.checkForInput(PLAY_MOUSE_POS):
                    options(current_language_index)
                if SETTINGS_SENSOR.checkForInput(PLAY_MOUSE_POS):
                    options(current_language_index)
                # Verifica se o botão on/off da geladeira foi clicado
                if pygame_menu.Rect(button_x, button_y_start, 70, 35).collidepoint(event.pos):
                    toggle_on_off_button_geladeira()
                # Verifica se o botão on/off da cafeteira foi clicado
                elif pygame_menu.Rect(button_x, button_y_start + 70, 100, 50).collidepoint(event.pos):
                    toggle_on_off_button_cafeteira()
                # Verifica se o botão on/off do chuveiro foi clicado
                elif pygame_menu.Rect(button_x, button_y_start + 140, 100, 50).collidepoint(event.pos):
                    toggle_on_off_button_chuveiro()
                # Verifica se o botão on/off do termômetro foi clicado
                elif pygame_menu.Rect(button_x, button_y_start + 210, 100, 50).collidepoint(event.pos):
                    toggle_on_off_button_termometro()
                # Verifica se o botão on/off do sensor foi clicado
                elif pygame_menu.Rect(button_x, button_y_start + 280, 100, 50).collidepoint(event.pos):
                    toggle_on_off_button_sensor()

        if pygame_menu.time.get_ticks() - color_timer >= 1000:
            line_color = pygame_menu.Color('black')

        pygame_menu.display.update()

def config(current_language_index):
    while True:
        CONFIG_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")
        if(current_language_index == 0):

            CONFIG_TEXT = get_font(75).render("Configurações", True, "Black")
            CONFIG_RECT = CONFIG_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(CONFIG_TEXT, CONFIG_RECT)
            LANGUAGE_BUTTON = Button(image=None, pos=(screen_resolution.get_width() / 2.14, screen_resolution.get_height() * 0.45), 
                                text_input="Idioma", font=get_font(75), base_color="Black", hovering_color="White")
            RESOLUTION_BUTTON = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.3), 
                                    text_input="Resolução", font=get_font(75), base_color="Black", hovering_color="White")
            CONFIG_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="White")
        
        if(current_language_index == 1):

            CONFIG_TEXT = get_font(75).render("Settings", True, "Black")
            CONFIG_RECT = CONFIG_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(CONFIG_TEXT, CONFIG_RECT)
            LANGUAGE_BUTTON = Button(image=None, pos=(screen_resolution.get_width() / 2.14, screen_resolution.get_height() * 0.45), 
                                text_input="Language", font=get_font(75), base_color="Black", hovering_color="White")
            RESOLUTION_BUTTON = Button(image=None, pos=(screen_resolution.get_width() / 2.10, screen_resolution.get_height() * 0.3), 
                                    text_input="Resolution", font=get_font(75), base_color="Black", hovering_color="White")
            CONFIG_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                text_input="Back", font=get_font(75), base_color="Black", hovering_color="White")

        for button in [LANGUAGE_BUTTON, RESOLUTION_BUTTON, CONFIG_BACK]:
            button.changeColor(CONFIG_MOUSE_POS)
            button.update(screen_resolution)

        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if LANGUAGE_BUTTON.checkForInput(CONFIG_MOUSE_POS):
                    language_settings(current_language_index)
                if RESOLUTION_BUTTON.checkForInput(CONFIG_MOUSE_POS):
                    resolution_settings(screen_resolution, current_resolution_index, Fullscreen, current_language_index)
                if CONFIG_BACK.checkForInput(CONFIG_MOUSE_POS):
                    main_menu(current_language_index)  

        pygame_menu.display.update()


def volume_settings():
    while True:
        VOLUME_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")

        VOLUME_TEXT = get_font(45).render("Volume", True, "Black")
        VOLUME_RECT = VOLUME_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 3))
        screen_resolution.blit(VOLUME_TEXT, VOLUME_RECT)

        # Implementar controles de volume aqui

        VOLUME_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                             text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="White")

        VOLUME_BACK.changeColor(VOLUME_MOUSE_POS)
        VOLUME_BACK.update(screen_resolution)

        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if VOLUME_BACK.checkForInput(VOLUME_MOUSE_POS):
                    config(current_language_index)  

        pygame_menu.display.update()

def resolution_settings(screen_resolution, current_resolution_index, Fullscreen, current_language_index):
    while True:
        RESOLUTION_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")
        if(current_language_index == 0):
            CONFIG_TEXT = get_font(75).render("Configurações", True, "Black")
            CONFIG_RECT = CONFIG_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(CONFIG_TEXT, CONFIG_RECT)

            RESOLUTION_TEXT = get_font(75).render("Resolução", True, "Black")
            RESOLUTION_RECT = RESOLUTION_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.3))
            screen_resolution.blit(RESOLUTION_TEXT, RESOLUTION_RECT)

            # Botão "Voltar"
            RESOLUTION_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                    text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="White")
            RESOLUTION_BACK.changeColor(RESOLUTION_MOUSE_POS)
            RESOLUTION_BACK.update(screen_resolution)

        elif(current_language_index == 1):
            CONFIG_TEXT = get_font(75).render("Settings", True, "Black")
            CONFIG_RECT = CONFIG_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(CONFIG_TEXT, CONFIG_RECT)

            RESOLUTION_TEXT = get_font(75).render("Resolution", True, "Black")
            RESOLUTION_RECT = RESOLUTION_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.3))
            screen_resolution.blit(RESOLUTION_TEXT, RESOLUTION_RECT)

            # Botão "Voltar"
            RESOLUTION_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                    text_input="Back", font=get_font(75), base_color="Black", hovering_color="White")
            RESOLUTION_BACK.changeColor(RESOLUTION_MOUSE_POS)
            RESOLUTION_BACK.update(screen_resolution)

        font = get_font(30)
        y_offset = screen_resolution.get_height() * 0.4
        for i, res in enumerate(resolutions):
            color = (pygame_menu.Color("BLACK"))
            if res == "Fullscreen":
                res_text = font.render("Tela Cheia", True, color)
            else:
                res_text = font.render(f"{res[0]} x {res[1]}", True, color)
            
            # Coordenadas da caixa de seleção e do "x"
            checkbox_x = screen_resolution.get_width() / 2 - 150
            checkbox_y = y_offset
            x_mark_x = checkbox_x + 5
            x_mark_y = checkbox_y + 5
            
            # Caixa de seleção
            checkbox_rect = pygame_menu.Rect(checkbox_x, checkbox_y, 20, 20)
            pygame_menu.draw.rect(screen_resolution, color, checkbox_rect, 2)
            
            # Marcar caixa de seleção se for a resolução atual
            if i == current_resolution_index and Fullscreen == 0:
                pygame_menu.draw.line(screen_resolution, color, (x_mark_x, x_mark_y), (x_mark_x + 10, x_mark_y + 10), 2)
                pygame_menu.draw.line(screen_resolution, color, (x_mark_x + 10, x_mark_y), (x_mark_x, x_mark_y + 10), 2)
            if Fullscreen == 1 and res == "Fullscreen":
                pygame_menu.draw.line(screen_resolution, color, (x_mark_x, x_mark_y), (x_mark_x + 10, x_mark_y + 10), 2)
                pygame_menu.draw.line(screen_resolution, color, (x_mark_x + 10, x_mark_y), (x_mark_x, x_mark_y + 10), 2)
            
            screen_resolution.blit(res_text, (checkbox_x + 30, checkbox_y - 5))
            y_offset += 40
        

        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if RESOLUTION_BACK.checkForInput(RESOLUTION_MOUSE_POS):
                    # Retorna à tela de configurações
                    config(current_language_index)
                if event.button == 1:  # Clique com o botão esquerdo do mouse
                    mouse_pos = event.pos
                    selected_index = check_selection_resolution(mouse_pos, screen_resolution.get_height() * 0.4, len(resolutions))
                    if resolutions[selected_index] == "Fullscreen":
                        Fullscreen = 1
                        screen_resolution = pygame_menu.display.set_mode((0, 0), pygame_menu.FULLSCREEN)
                    else:
                        Fullscreen = 0
                        current_resolution_index = selected_index
                        screen_resolution = pygame_menu.display.set_mode(resolutions[current_resolution_index])
        pygame_menu.display.update()

def language_settings(current_language_index):
    while True:
        LANG_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")

        if current_language_index == 0:
            CONFIG_TEXT = get_font(75).render("Configurações", True, "Black")
            CONFIG_RECT = CONFIG_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(CONFIG_TEXT, CONFIG_RECT)
        
            LANG_TEXT = get_font(75).render("Idioma", True, "Black")
            LANG_RECT = LANG_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.3))
            screen_resolution.blit(LANG_TEXT, LANG_RECT)
            # Botão "Voltar"
            LANG_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                    text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="White")
            LANG_BACK.changeColor(LANG_MOUSE_POS)
            LANG_BACK.update(screen_resolution)

        elif current_language_index == 1:
            CONFIG_TEXT = get_font(75).render("Settings", True, "Black")
            CONFIG_RECT = CONFIG_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(CONFIG_TEXT, CONFIG_RECT)

            LANG_TEXT = get_font(75).render("Language", True, "Black")
            LANG_RECT = LANG_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.3))
            screen_resolution.blit(LANG_TEXT, LANG_RECT)

            LANG_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                    text_input="Back", font=get_font(75), base_color="Black", hovering_color="White")
            LANG_BACK.changeColor(LANG_MOUSE_POS)
            LANG_BACK.update(screen_resolution)

        font = get_font(30)
        y_offset = screen_resolution.get_height() * 0.4
        languages = ["Português (BR)", "English"]
        checkbox_areas = []
        for i, lang in enumerate(languages):
            color = (pygame_menu.Color("BLACK"))
            lang_text = font.render(lang, True, color)
            
            # Coordenadas da caixa de seleção
            checkbox_x = screen_resolution.get_width() / 2 - 150
            checkbox_y = y_offset
            
            # Caixa de seleção
            checkbox_rect = pygame_menu.Rect(checkbox_x, checkbox_y, 20, 20)
            pygame_menu.draw.rect(screen_resolution, color, checkbox_rect, 2)
            
            # Marcar caixa de seleção se for o idioma atual
            if i == current_language_index:
                pygame_menu.draw.line(screen_resolution, color, (checkbox_x + 5, checkbox_y + 5), (checkbox_x + 15, checkbox_y + 15), 2)
                pygame_menu.draw.line(screen_resolution, color, (checkbox_x + 15, checkbox_y + 5), (checkbox_x + 5, checkbox_y + 15), 2)
            
            screen_resolution.blit(lang_text, (checkbox_x + 30, checkbox_y - 5))
            y_offset += 40
            
            checkbox_areas.append(checkbox_rect)

        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if LANG_BACK.checkForInput(LANG_MOUSE_POS):
                    # Retorna à tela de configurações
                    config(current_language_index)
                if event.button == 1:  # Clique com o botão esquerdo do mouse
                    mouse_pos = event.pos
                    for i, checkbox_rect in enumerate(checkbox_areas):
                        if checkbox_rect.collidepoint(mouse_pos):
                            current_language_index = i
                            break
        
        pygame_menu.display.update()

def history(current_language_index):
    while True:
        SPEC1_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")
        if current_language_index == 0:
            SPEC1_TEXT = get_font(75).render("Histórico", True, "Black")
            SPEC1_RECT = SPEC1_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(SPEC1_TEXT, SPEC1_RECT)

            SPEC1_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                            text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="White")

            SPEC1_BACK.changeColor(SPEC1_MOUSE_POS)
            SPEC1_BACK.update(screen_resolution)

        elif current_language_index == 1:
            SPEC1_TEXT = get_font(75).render("History", True, "Black")
            SPEC1_RECT = SPEC1_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(SPEC1_TEXT, SPEC1_RECT)

            SPEC1_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                            text_input="Back", font=get_font(75), base_color="Black", hovering_color="White")

            SPEC1_BACK.changeColor(SPEC1_MOUSE_POS)
            SPEC1_BACK.update(screen_resolution)

        

        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if SPEC1_BACK.checkForInput(SPEC1_MOUSE_POS):
                    main_menu(current_language_index)  

        pygame_menu.display.update()

def especificacao1(current_language_index):
    while True:
        SPEC1_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")

        if current_language_index == 0:

            SPEC1_TEXT = get_font(45).render("Especificação 1", True, "Black")
            SPEC1_RECT = SPEC1_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 3))
            screen_resolution.blit(SPEC1_TEXT, SPEC1_RECT)

            SPEC1_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="White")

            SPEC1_BACK.changeColor(SPEC1_MOUSE_POS)
            SPEC1_BACK.update(screen_resolution)

        elif current_language_index == 1:

            SPEC1_TEXT = get_font(45).render("Details 1", True, "Black")
            SPEC1_RECT = SPEC1_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 3))
            screen_resolution.blit(SPEC1_TEXT, SPEC1_RECT)

            SPEC1_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                text_input="Back", font=get_font(75), base_color="Black", hovering_color="White")

            SPEC1_BACK.changeColor(SPEC1_MOUSE_POS)
            SPEC1_BACK.update(screen_resolution)

        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if SPEC1_BACK.checkForInput(SPEC1_MOUSE_POS):
                    options(current_language_index)  

        pygame_menu.display.update()

def especificacao2(current_language_index):
    while True:
        SPEC2_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")

        if current_language_index== 0:
            SPEC2_TEXT = get_font(45).render("Especificação 2", True, "Black")
            SPEC2_RECT = SPEC2_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 3))
            screen_resolution.blit(SPEC2_TEXT, SPEC2_RECT)

            SPEC2_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="White")

            SPEC2_BACK.changeColor(SPEC2_MOUSE_POS)
            SPEC2_BACK.update(screen_resolution)

        elif current_language_index== 1:
            SPEC2_TEXT = get_font(45).render("Details 2", True, "Black")
            SPEC2_RECT = SPEC2_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 3))
            screen_resolution.blit(SPEC2_TEXT, SPEC2_RECT)

            SPEC2_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                                text_input="Back", font=get_font(75), base_color="Black", hovering_color="White")

            SPEC2_BACK.changeColor(SPEC2_MOUSE_POS)
            SPEC2_BACK.update(screen_resolution)

        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if SPEC2_BACK.checkForInput(SPEC2_MOUSE_POS):
                    options(current_language_index)  

        pygame_menu.display.update()

def options(current_language_index):
    labels1 = ['A', 'B', 'C', 'D', 'E']
    values1 = np.random.randint(1, 100, size=len(labels1))

    plt.figure(figsize=(3, 3.5))
    plt.bar(labels1, values1, color='skyblue')
    plt.xlabel('Categorias')
    plt.ylabel('Valores')
    plt.title('Exemplo de Gráfico de Barras')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('assets/grafico1.png')

    labels2 = ['X', 'Y', 'Z', 'W']
    values2 = np.random.randint(1, 100, size=len(labels2))

    plt.figure(figsize=(3, 3.5))
    plt.bar(labels2, values2, color='lightgreen')
    plt.xlabel('Categorias')
    plt.ylabel('Valores')
    plt.title('Segundo Gráfico de Barras')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('assets/grafico2.png')

    while True:
        OPTIONS_MOUSE_POS = pygame_menu.mouse.get_pos()

        screen_resolution.fill("#FFF4EE")

        if (current_language_index == 0):
            OPTIONS_TEXT = get_font(45).render("Métricas", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                            text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)

            OPTIONS_BACK.update(screen_resolution)
        
        if (current_language_index == 1):
            OPTIONS_TEXT = get_font(45).render("Details", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_resolution.get_width() / 2, screen_resolution.get_height() / 8))
            screen_resolution.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(screen_resolution.get_width() / 2, screen_resolution.get_height() * 0.9), 
                            text_input="Back", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)

            OPTIONS_BACK.update(screen_resolution)

        grafico1_img = pygame_menu.image.load("assets/grafico1.png")
        if grafico1_img.get_rect(topleft=(screen_resolution.get_width() * 0.15, screen_resolution.get_height() * 0.2)).collidepoint(OPTIONS_MOUSE_POS):
            grafico1_img.fill((0, 255, 0, 128), special_flags=pygame_menu.BLEND_RGBA_MULT)

        screen_resolution.blit(grafico1_img, (screen_resolution.get_width() * 0.15, screen_resolution.get_height() * 0.2))

        grafico2_img = pygame_menu.image.load("assets/grafico2.png")
        if grafico2_img.get_rect(topleft=(screen_resolution.get_width() * 0.6, screen_resolution.get_height() * 0.2)).collidepoint(OPTIONS_MOUSE_POS):
            grafico2_img.fill((0, 255, 0, 128), special_flags=pygame_menu.BLEND_RGBA_MULT)

        screen_resolution.blit(grafico2_img, (screen_resolution.get_width() * 0.6, screen_resolution.get_height() * 0.2))


        for event in pygame_menu.event.get():
            if event.type == pygame_menu.QUIT:
                pygame_menu.quit()
                sys.exit()
            if event.type == pygame_menu.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    play(current_language_index)  
                if grafico1_img.get_rect(topleft=(screen_resolution.get_width() * 0.15, screen_resolution.get_height() * 0.2)).collidepoint(event.pos):
                    especificacao1(current_language_index)
                if grafico2_img.get_rect(topleft=(screen_resolution.get_width() * 0.6, screen_resolution.get_height() * 0.2)).collidepoint(event.pos):
                    especificacao2(current_language_index)

        pygame_menu.display.update()

main_menu(current_language_index)
