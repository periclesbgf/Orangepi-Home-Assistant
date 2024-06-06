import sys
import matplotlib.pyplot as plt
import numpy as np
from button import Button
import threading
import sys
import numpy as np
from button import Button
from helper_function import (
    get_local_ip, initialize_mqtt_client, list_devices, list_output_devices, predict_mic, EDEN_EVENT
)
from mqtt.response_handler import (
    LUMINARIA, LUZ, VALVULA, PORTA, BOMBA_DE_AGUA, handler, mqtt_publish,
    MQTT_TOPIC_LUMINARIA, MQTT_TOPIC_LUZ, MQTT_TOPIC_VALVULA, MQTT_TOPIC_PORTA, MQTT_TOPIC_BOMBA
    )

import pygame

pygame_menu = pygame
pygame_menu.init()


current_language_index = 0
current_resolution_index = 1
Fullscreen = 1
#screen_resolution = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)  #CASO VÁ COLOCAR FULL SCREEN, SETAR VARIÁVEL FULLSCREN PARA 0
screen_resolution = pygame.display.set_mode((1024, 600))
pygame.display.set_caption("Eden")
#pygame.mouse.set_visible(False)

BG = pygame.image.load("assets/fundoedendeverdade.png")
edenlogo = pygame.image.load('assets/edenlogo.png')
Settings = pygame.image.load('assets/settings.png')
Devices = pygame.image.load('assets/devices_image.png')

def get_font(size):
    return pygame.font.Font("assets/Gully-Bold.otf", size)

def draw_horizontal_line(color):
    pygame.draw.line(screen_resolution, color, (0, screen_resolution.get_height() / 1.3), (screen_resolution.get_width(), screen_resolution.get_height() / 1.3), 5)

def check_selection_resolution(mouse_pos, y_offset_start, num_items):
    y_offset = y_offset_start
    for i in range(num_items):
        # Coordenadas atualizadas da caixa de seleção
        checkbox_x = screen_resolution.get_width() / 2 - 150
        checkbox_y = y_offset
        checkbox_rect = pygame.Rect(checkbox_x, checkbox_y, 20, 20)
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
        checkbox_rect = pygame.Rect(checkbox_x, checkbox_y, 20, 20)
        if checkbox_rect.collidepoint(mouse_pos):
            return i
        y_offset += 40
    return -1


# Adicione uma variável global para rastrear o estado do botão on/off
on_off_state = False
on_off_state_luminaria = False
on_off_state_bomba_de_agua = False
on_off_state_porta = False
on_off_state_luz = False
on_off_state_valvula = False

def draw_device_button(x, y, text, state):
    button_width, button_height = 250, 80  # Tamanho ajustado dos botões
    button_rect = pygame.Rect(x, y, button_width, button_height)
    on_color = (53, 198, 88)  # Cor do botão quando está ligado
    off_color = (18, 18, 18)  # Cor do botão quando está desligado
    pygame.draw.rect(screen_resolution, on_color if state else off_color, button_rect)
    button_text = get_font(20).render(text, True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen_resolution.blit(button_text, text_rect)

def toggle_on_off_button_luminaria():
    global on_off_state_luminaria
    on_off_state_luminaria = not on_off_state_luminaria

    if on_off_state_luminaria:
        command = 'on'
    else:
        command = 'off'
    mqtt_publish(command, MQTT_TOPIC_LUMINARIA)

def toggle_on_off_button_luz():
    global on_off_state_luz
    # Alterna o estado do botão da luz
    on_off_state_luz = not on_off_state_luz

    if on_off_state_luz:
        command = 'on_light'
    else:
        command = 'off_light'
    mqtt_publish(command, MQTT_TOPIC_LUZ)

def toggle_on_off_button_bomba_de_agua():
    global on_off_state_bomba_de_agua
    # Alterna o estado do botão do bomba_de_agua
    on_off_state_bomba_de_agua = not on_off_state_bomba_de_agua

    if on_off_state_bomba_de_agua:
        command = '1'
    else:
        command = '0'
    mqtt_publish(command, MQTT_TOPIC_BOMBA)

def toggle_on_off_button_valvula():
    global on_off_state_valvula
    # Alterna o estado do botão do termômetro
    on_off_state_valvula = not on_off_state_valvula

    if on_off_state_valvula:
        command = '1'
    else:
        command = '0'
    mqtt_publish(command, MQTT_TOPIC_VALVULA)

def toggle_on_off_button_porta():
    global on_off_state_porta
    # Alterna o estado do botão do porta
    on_off_state_porta = not on_off_state_porta

    if on_off_state_porta:
        command = '11111111111111111111'
    else:
        command = '00000000000000000000'
    mqtt_publish(command, MQTT_TOPIC_PORTA)

def draw_notification(screen_resolution, message, current_language_index):
    # Cria uma superfície para a notificação
    notification_surface = pygame.Surface((500, 170))
    notification_surface.fill((18, 18, 18))

    # Renderiza o texto
    font = get_font(20)
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(250, 50))
    notification_surface.blit(text_surface, text_rect)

    # Desenha o botão "Sair"
    button_rect = pygame.Rect(200, 100, 100, 50)
    pygame.draw.rect(notification_surface, (191, 91, 14), button_rect)
    if(current_language_index == 0):
        button_text_surface = font.render("Sim", True, (255, 255, 255))
    elif(current_language_index == 1):
        button_text_surface = font.render("Yes", True, (255, 255, 255))
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)
    notification_surface.blit(button_text_surface, button_text_rect)

    # Define a posição da notificação no canto superior esquerdo da tela
    notification_position = (20, 20)  # Pequeno deslocamento para não ficar colado no canto
    notification_rect = notification_surface.get_rect(topleft=notification_position)

    # Desenha a notificação na tela
    screen_resolution.blit(notification_surface, notification_rect)

    return button_rect.move(notification_rect.topleft)  # Retorna a posição real do botão na tela

def main_menu(current_language_index, current_resolution_index, Fullscreen):
    line_color = pygame.Color('white')
    color_timer = 0
    show_notification = False
    notification_start_time = 0
    notification_duration = 10000  # duração da notificação em segundos
    button_rect = None

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen_resolution.blit(BG, (0, 0))
        screen_resolution.blit(edenlogo, pygame.Rect(300, 60, 100, 50))

        draw_horizontal_line(line_color)
        if(current_language_index == 0):
            DISPOSITIVOS_BUTTON = Button(image=pygame.image.load("assets/button_dispositivos.png"), pos=(screen_resolution.get_width() * 0.50, screen_resolution.get_height() / 2.3), 
                                text_input="", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
            CONFIG_BUTTON = Button(image=pygame.image.load("assets/button_config.png"), pos=(screen_resolution.get_width() * 0.40, screen_resolution.get_height() / 1.125), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")  # Ícone de engrenagem, sem texto
            HISTORY_BUTTON = Button(image=pygame.image.load("assets/button_historico.png"), pos=(screen_resolution.get_width() * 0.50, screen_resolution.get_height() / 1.6), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White") 
            QUIT_BUTTON = Button(image=pygame.image.load("assets/button_sair.png"), pos=(screen_resolution.get_width() * 0.60, screen_resolution.get_height() / 1.125), 
                                text_input="", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        elif(current_language_index == 1):
            DISPOSITIVOS_BUTTON = Button(image=pygame.image.load("assets/button_devices.png"), pos=(screen_resolution.get_width() * 0.50, screen_resolution.get_height() / 2.3), 
                                text_input="", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
            CONFIG_BUTTON = Button(image=pygame.image.load("assets/button_config.png"), pos=(screen_resolution.get_width() * 0.40, screen_resolution.get_height() / 1.125), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")  # Ícone de engrenagem, sem texto
            HISTORY_BUTTON = Button(image=pygame.image.load("assets/button_chat_history.png"), pos=(screen_resolution.get_width() * 0.50, screen_resolution.get_height() / 1.6), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White") 
            QUIT_BUTTON = Button(image=pygame.image.load("assets/button_sair.png"), pos=(screen_resolution.get_width() * 0.60, screen_resolution.get_height() / 1.125), 
                                text_input="", font=get_font(45), base_color="#d7fcd4", hovering_color="White")


        for button in [DISPOSITIVOS_BUTTON, CONFIG_BUTTON, QUIT_BUTTON, HISTORY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen_resolution)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == EDEN_EVENT:
                line_color = pygame_menu.Color('BLUE')
                color_timer = pygame_menu.time.get_ticks()
            if event.type == LUMINARIA:
                toggle_on_off_button_luminaria()
                show_notification = True
                notification_start_time = pygame.time.get_ticks()
            if event.type == LUZ:
                toggle_on_off_button_luz()
                show_notification = True
                notification_start_time = pygame.time.get_ticks()
            if event.type == BOMBA_DE_AGUA:
                toggle_on_off_button_bomba_de_agua()
                show_notification = True
                notification_start_time = pygame.time.get_ticks()
            if event.type == PORTA:
                toggle_on_off_button_porta()
                show_notification = True
                notification_start_time = pygame.time.get_ticks()
            if event.type == VALVULA:
                toggle_on_off_button_valvula()
                show_notification = True
                notification_start_time = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_notification and button_rect and button_rect.collidepoint(event.pos):
                    play(current_language_index, current_resolution_index, Fullscreen)
                if DISPOSITIVOS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(current_language_index, current_resolution_index, Fullscreen)
                if CONFIG_BUTTON.checkForInput(MENU_MOUSE_POS):
                    config(screen_resolution, current_language_index, current_resolution_index, Fullscreen)
                if HISTORY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    history(current_language_index, current_resolution_index, Fullscreen)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        if show_notification:
            current_time = pygame.time.get_ticks()
            if current_time - notification_start_time < notification_duration:
                if(current_language_index == 0):
                    button_rect = draw_notification(screen_resolution, "Dispositivo ativado! Deseja conferir?", current_language_index)
                elif(current_language_index == 1):
                    button_rect = draw_notification(screen_resolution, "Device activated! Do you wish to confirm?", current_language_index)
            else:
                show_notification = False  # Oculta a notificação após a duração especificada

        if pygame.time.get_ticks() - color_timer >= 4000:
            line_color = pygame.Color('white')

        pygame.display.update()

def play(current_language_index, current_resolution_index, Fullscreen):
    line_color = pygame.Color('white')
    color_timer = 0

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen_resolution.fill("#F2F1F1")

        if current_language_index == 0:
            screen_resolution.blit(Devices, pygame.Rect(300, 35, 100, 50))
        else:
            screen_resolution.blit(Devices, pygame.Rect(350, 35, 100, 50))

        draw_horizontal_line(line_color)

        # Definindo a posição central dos botões
        button_x = screen_resolution.get_width() / 2 - 200  # Ajuste para centralizar horizontalmente
        button_y_start = screen_resolution.get_height() / 2 - 180  # Ajuste para centralizar verticalmente e espaço entre os botões

        if (current_language_index == 0):

            LUMINARIA_BUTTON_TEXT = "Luminária"
            BOMBA_BUTTON_TEXT = "Bomba de água"
            PORTA_BUTTON_TEXT = "Porta"
            LUZ_BUTTON_TEXT = "Luz"
            VALVULA_BUTTON_TEXT = "Válvula"

            PLAY_TEXT = get_font(55).render("Dispositivos", True, "#1A1A1A")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(screen_resolution.get_width() / 1.9, screen_resolution.get_height() / 11))
            screen_resolution.blit(PLAY_TEXT, PLAY_RECT)


            PLAY_BACK = Button(image=pygame.image.load("assets/button_voltar.png"), pos=(screen_resolution.get_width() / 7.5, screen_resolution.get_height() / 1.1), 
                                text_input="", font=get_font(75), base_color="Black", hovering_color="Green")

        elif (current_language_index == 1):

            LUMINARIA_BUTTON_TEXT = "Lamp"
            BOMBA_BUTTON_TEXT = "Water Pump"
            PORTA_BUTTON_TEXT = "Door"
            LUZ_BUTTON_TEXT = "Light"
            VALVULA_BUTTON_TEXT = "Valve"

            PLAY_TEXT = get_font(55).render("Devices", True, "#1A1A1A")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(screen_resolution.get_width() / 1.9, screen_resolution.get_height() / 11))
            screen_resolution.blit(PLAY_TEXT, PLAY_RECT)

            PLAY_BACK = Button(image=pygame.image.load("assets/button_back.png"), pos=(screen_resolution.get_width() / 7.5, screen_resolution.get_height() / 1.1), 
                                text_input="", font=get_font(75), base_color="Black", hovering_color="Green")

        horizontal_spacing = 50
        vertical_spacing = 30

        button_positions = [
            (screen_resolution.get_width() / 2 - 1.5 * (235 + horizontal_spacing), 200),  # Luminária
            (screen_resolution.get_width() / 2 - 0.5 * (205 + horizontal_spacing), 200),  # Bomba de água
            (screen_resolution.get_width() / 2 + 0.5 * (300 + horizontal_spacing), 200),  # Porta
            (screen_resolution.get_width() / 2 - 1 * (250 + horizontal_spacing / 2), 200 + 80 + vertical_spacing),  # Luz
            (screen_resolution.get_width() / 2 + 1 * (5 + horizontal_spacing / 2), 200 + 80 + vertical_spacing)   # Válvula
        ]

        draw_device_button(*button_positions[0], LUMINARIA_BUTTON_TEXT, on_off_state_luminaria)
        draw_device_button(*button_positions[1], BOMBA_BUTTON_TEXT, on_off_state_bomba_de_agua)
        draw_device_button(*button_positions[2], PORTA_BUTTON_TEXT, on_off_state_porta)
        draw_device_button(*button_positions[3], LUZ_BUTTON_TEXT, on_off_state_luz)
        draw_device_button(*button_positions[4], VALVULA_BUTTON_TEXT, on_off_state_valvula)

        for button in [PLAY_BACK]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(screen_resolution)

        for event in pygame.event.get():
            if event.type == EDEN_EVENT:
                line_color = pygame_menu.Color('BLUE')
                color_timer = pygame_menu.time.get_ticks()
            if event.type == LUMINARIA:
                toggle_on_off_button_luminaria()
            if event.type == LUZ:
                toggle_on_off_button_luz()
            if event.type == BOMBA_DE_AGUA:
                toggle_on_off_button_bomba_de_agua()
            if event.type == PORTA:
                toggle_on_off_button_porta()
            if event.type == VALVULA:
                toggle_on_off_button_valvula()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu(current_language_index, current_resolution_index, Fullscreen)
                if pygame.Rect(*button_positions[0], 250, 80).collidepoint(event.pos):
                    toggle_on_off_button_luminaria()
                elif pygame.Rect(*button_positions[1], 250, 80).collidepoint(event.pos):
                    toggle_on_off_button_bomba_de_agua()
                elif pygame.Rect(*button_positions[2], 250, 80).collidepoint(event.pos):
                    toggle_on_off_button_porta()
                elif pygame.Rect(*button_positions[3], 250, 80).collidepoint(event.pos):
                    toggle_on_off_button_luz()
                elif pygame.Rect(*button_positions[4], 250, 80).collidepoint(event.pos):
                    toggle_on_off_button_valvula()

        pygame.display.update()

        if pygame.time.get_ticks() - color_timer >= 4000:
            line_color = pygame.Color('white')

        pygame.display.update()

def config(screen_resolution, current_language_index, current_resolution_index, Fullscreen):

    dropdown_open_resolution = False
    dropdown_open_language = False

    resolutions = [(800, 600), (1024, 600), (1280, 720), "Fullscreen"]
    languages = ["Português (BR)", "English"]

    selected_resolution = resolutions[current_resolution_index]
    selected_language = languages[current_language_index]

    font = get_font(30)

    while True:

        CONFIG_MOUSE_POS = pygame.mouse.get_pos()

        screen_resolution.fill("#F2F1F1")

        if current_language_index == 0:
            screen_resolution.blit(Settings, pygame.Rect(300, 60, 100, 50))
        else:
            screen_resolution.blit(Settings, pygame.Rect(380, 60, 100, 50))

        # Texto de Configurações
        config_texts = {
            0: ("Configurações", "Resolução", "Idioma", "Voltar"),
            1: ("Settings", "Resolution", "Language", "Back")
        }
        current_texts = config_texts[current_language_index]

        CONFIG_TEXT = get_font(55).render(current_texts[0], True, "#1A1A1A")
        CONFIG_RECT = CONFIG_TEXT.get_rect(center=(screen_resolution.get_width() / 1.8, screen_resolution.get_height() / 8))
        screen_resolution.blit(CONFIG_TEXT, CONFIG_RECT)

        LANGUAGE_TEXT = get_font(20).render(current_texts[1], True, "#1A1A1A")
        LANGUAGE_RECT = LANGUAGE_TEXT.get_rect(center=(screen_resolution.get_width() / 6.5, screen_resolution.get_height() / 3.6))
        screen_resolution.blit(LANGUAGE_TEXT, LANGUAGE_RECT)

        LANGUAGE_TEXT = get_font(20).render(current_texts[2], True, "#1A1A1A")
        LANGUAGE_RECT = LANGUAGE_TEXT.get_rect(center=(screen_resolution.get_width() / 1.55, screen_resolution.get_height() / 3.6))
        screen_resolution.blit(LANGUAGE_TEXT, LANGUAGE_RECT)

        # Dropdown de Resolução
        resolution_rect = pygame.Rect(screen_resolution.get_width() / 4 - 150, screen_resolution.get_height() * 0.3, 300, 50)
        pygame.draw.rect(screen_resolution, (169, 169, 169), resolution_rect)
        if Fullscreen:
            res_text = font.render("Tela Cheia" if current_language_index == 0 else "Fullscreen", True, (0, 0, 0))
        else:
            Fullscreen = 0
            res_text = font.render(f"{selected_resolution[0]} x {selected_resolution[1]}", True, (0, 0, 0))
        res_text_rect = res_text.get_rect(center=(resolution_rect.centerx, resolution_rect.centery))
        screen_resolution.blit(res_text, res_text_rect)

        # Dropdown de Idioma
        language_rect = pygame.Rect(screen_resolution.get_width() * 3 / 4 - 150, screen_resolution.get_height() * 0.3, 300, 50)
        pygame.draw.rect(screen_resolution, (169, 169, 169), language_rect)
        lang_text = font.render(selected_language, True, (0, 0, 0))
        lang_text_rect = lang_text.get_rect(center=(language_rect.centerx, language_rect.centery))
        screen_resolution.blit(lang_text, lang_text_rect)

        # Botão Voltar
        if current_language_index == 0:
            CONFIG_BACK = Button(image=pygame.image.load("assets/button_voltar.png"), pos=(screen_resolution.get_width() / 7.5, screen_resolution.get_height() * 0.9), 
                                text_input="", font=get_font(75), base_color="Black", hovering_color="White")
            CONFIG_BACK.changeColor(CONFIG_MOUSE_POS)
            CONFIG_BACK.update(screen_resolution)
        else:
            CONFIG_BACK = Button(image=pygame.image.load("assets/button_back.png"), pos=(screen_resolution.get_width() / 7.5, screen_resolution.get_height() * 0.9), 
                                text_input="", font=get_font(75), base_color="Black", hovering_color="White")
            CONFIG_BACK.changeColor(CONFIG_MOUSE_POS)
            CONFIG_BACK.update(screen_resolution)

        # Desenhar as opções de resolução no dropdown se aberto
        if dropdown_open_resolution:
            for i, res in enumerate(resolutions):
                option_rect = pygame.Rect(resolution_rect.x, resolution_rect.y + (i + 1) * resolution_rect.height, resolution_rect.width, resolution_rect.height)
                pygame.draw.rect(screen_resolution, (211, 211, 211), option_rect)
                if res == "Fullscreen":
                    option_text = font.render("Tela Cheia" if current_language_index == 0 else "Fullscreen", True, (0, 0, 0))
                else:
                    option_text = font.render(f"{res[0]} x {res[1]}", True, (0, 0, 0))
                option_text_rect = option_text.get_rect(center=(option_rect.centerx, option_rect.centery))
                screen_resolution.blit(option_text, option_text_rect)

        # Desenhar as opções de idioma no dropdown se aberto
        if dropdown_open_language:
            for i, lang in enumerate(languages):
                option_rect = pygame.Rect(language_rect.x, language_rect.y + (i + 1) * language_rect.height, language_rect.width, language_rect.height)
                pygame.draw.rect(screen_resolution, (211, 211, 211), option_rect)
                option_text = font.render(lang, True, (0, 0, 0))
                option_text_rect = option_text.get_rect(center=(option_rect.centerx, option_rect.centery))
                screen_resolution.blit(option_text, option_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONFIG_BACK.checkForInput(CONFIG_MOUSE_POS):
                    main_menu(current_language_index, current_resolution_index, Fullscreen)
                if resolution_rect.collidepoint(event.pos):
                    dropdown_open_resolution = not dropdown_open_resolution
                    dropdown_open_language = False
                elif language_rect.collidepoint(event.pos):
                    dropdown_open_language = not dropdown_open_language
                    dropdown_open_resolution = False
                else:
                    if dropdown_open_resolution:
                        for i, res in enumerate(resolutions):
                            option_rect = pygame.Rect(resolution_rect.x, resolution_rect.y + (i + 1) * resolution_rect.height, resolution_rect.width, resolution_rect.height)
                            if option_rect.collidepoint(event.pos):
                                selected_resolution = res
                                current_resolution_index = i
                                dropdown_open_resolution = False
                                if res == "Fullscreen":
                                    Fullscreen = 1
                                    screen_resolution = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)
                                else:
                                    Fullscreen = 0
                                    screen_resolution = pygame.display.set_mode(res)
                                break
                    if dropdown_open_language:
                        for i, lang in enumerate(languages):
                            option_rect = pygame.Rect(language_rect.x, language_rect.y + (i + 1) * language_rect.height, language_rect.width, language_rect.height)
                            if option_rect.collidepoint(event.pos):
                                selected_language = lang
                                current_language_index = i
                                dropdown_open_language = False
                                break

        pygame.display.update()

def history(current_language_index, current_resolution_index, Fullscreen):

    Data_historico = pygame.image.load('assets/7_junho_data.png')
    Historico_exemplo = pygame.image.load('assets/historico_eden_exemplo.png')

    while True:
        SPEC1_MOUSE_POS = pygame.mouse.get_pos()

        screen_resolution.fill("#F2F1F1")

        screen_resolution.blit(Data_historico, pygame.Rect(38, 150, 100, 50))
        screen_resolution.blit(Historico_exemplo, pygame.Rect(320, 200, 100, 50))

        if current_language_index == 0:
            SPEC1_TEXT = get_font(35).render("Histórico do Chat", True, "#1A1A1A")
            SPEC1_RECT = SPEC1_TEXT.get_rect(center=(screen_resolution.get_width() / 6.2, screen_resolution.get_height() / 8))
            screen_resolution.blit(SPEC1_TEXT, SPEC1_RECT)

            SPEC1_BACK = Button(image=pygame.image.load("assets/button_voltar.png"), pos=(screen_resolution.get_width() / 7.5, screen_resolution.get_height() / 1.1), 
                                text_input="", font=get_font(75), base_color="Black", hovering_color="Green")

            SPEC1_BACK.changeColor(SPEC1_MOUSE_POS)
            SPEC1_BACK.update(screen_resolution)

        elif current_language_index == 1:
            SPEC1_TEXT = get_font(35).render("Chat History", True, "#1A1A1A")
            SPEC1_RECT = SPEC1_TEXT.get_rect(center=(screen_resolution.get_width() / 6.2, screen_resolution.get_height() / 8))
            screen_resolution.blit(SPEC1_TEXT, SPEC1_RECT)

            SPEC1_BACK = Button(image=pygame.image.load("assets/button_back.png"), pos=(screen_resolution.get_width() / 7.5, screen_resolution.get_height() * 0.9), 
                                text_input="", font=get_font(75), base_color="Black", hovering_color="White")

            SPEC1_BACK.changeColor(SPEC1_MOUSE_POS)
            SPEC1_BACK.update(screen_resolution)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SPEC1_BACK.checkForInput(SPEC1_MOUSE_POS):
                    main_menu(current_language_index, current_resolution_index, Fullscreen)

        pygame.display.update()


if __name__ == "__main__":

    SERVER_IP = get_local_ip()
    print(f"O IP do servidor foi definido para {SERVER_IP}")

    client = initialize_mqtt_client()
    client.loop_start()

    # Exemplo de uso
    list_devices()
    list_output_devices()

    # Cria e inicia a thread para rodar a função predict_mic
    mic_thread = threading.Thread(target=predict_mic, args=(pygame_menu,))
    mic_thread.daemon = True
    mic_thread.start()

    main_menu(current_language_index, current_resolution_index, Fullscreen)