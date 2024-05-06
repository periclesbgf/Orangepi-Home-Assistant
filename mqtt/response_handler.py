from utils.constants import MQTT_TOPIC

# def handler(text):
#     filepath, prompt_output = send_prompt(text)
#     text_lower = prompt_output.lower()
#     if text_lower in ['ligar a luminária', 'ligar luminária','ligue a luminária','ligue luminária', 'ligar luminaria']:
#         command = 'on'
#         mqtt_publish(command, MQTT_TOPIC)
#     elif text_lower in ['desligar a luminária', 'desligar luminária','apagar luminária', 'desligar luminaria', 'desligue a luminária', 'desligue luminária']:
#         command = 'off'
#         mqtt_publish(command, MQTT_TOPIC)
#     elif text_lower in ["tocar musica", "tocar música", "tocar um som", "tocar som"]:
#         pass
#         #send_wav_file_over_tcp(wav_file_path, ESP32_TCP_SERVER_IP, ESP32_TCP_SERVER_PORT_FOR)
#     elif text_lower in ["ligar luz", "ligar a luz", "ligar luz.", "ligue luz.", "ligar a luz"]:
#         command = 'on_light'
#         mqtt_publish(command, "led/debug")
#     elif text_lower in ["desligar luz", "desligar a luz", "desligar luz.", "desligue luz."]:
#         command = 'off_light'
#         mqtt_publish(command, "led/debug")
#     elif text_lower in ["ligar valvula", "ligar a valvula", "ligar valvula.", "ligue valvula."]:
#         command = "1"
#         mqtt_publish(command, "sala11/valvula")
#     elif text_lower in ["desligar valvula", "desligar a valvula", "desligar valvula.", "desligue valvula."]:
#         command = "0"
#         mqtt_publish(command, "sala11/valvula")
#     elif text_lower in ["travar porta", "travar a porta", "travar porta.", "trave porta."]:
#         command = "11111111111111111111"
#         mqtt_publish(command, "esp32/open_door")
#     elif text_lower in ["destravar porta", "destravar a porta", "destravar porta.", "destrave porta."]:
#         command = "00000000000000000000"
#         mqtt_publish(command, "esp32/open_door")
#     elif text_lower in ["ligar bomba de água", "ligar bomba de agua", "ligar bomba de água.", "ligue bomba de água."]:
#         command = "1"
#         mqtt_publish(command, "sala11/bomba")
#     elif text_lower in ["desligar bomba de água", "desligar bomba de agua", "desligar bomba de água.", "desligue bomba de água."]:
#         command = "0"
#         mqtt_publish(command, "sala11/bomba")
#     # else:
#     #     send_wav_file_over_tcp(filepath, ESP32_TCP_SERVER_IP, ESP32_TCP_SERVER_PORT_FOR)
