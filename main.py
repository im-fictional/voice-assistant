import eel
from commands import commands, phrases_of_assistant

import requests
import webbrowser
from bs4 import BeautifulSoup

import pygame
from gtts import gTTS
from io import BytesIO
import speech_recognition as sr

import time
from datetime import datetime

import pyautogui
import pyperclip

import random

import os
import platform

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

@eel.expose
def stella_assistant():

    # ФУНКЦІЯ ОЗВУЧУВАННЯ АСИСТЕНТА
    LNG2 = 'uk'
    pygame.init()

    def speak_engine(text):
        print(text)

        obj = gTTS(text=text, lang=LNG2, slow=False)
        fp = BytesIO()
        obj.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    
    # ФУНКЦІЯ ПОШУКУ ІНФОРМАЦІЇ В ІНТЕРНЕТІ
    def google_search(query):
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)

    
    # ФУНКЦІЯ ВІДКРИТТЯ САЙТІВ
    def info_search(task):
        search_url = f"https://www.google.com/search?q={task}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('div', class_='yuRUbf')

        if first_result:
            link = first_result.find('a')['href']
            link_text = first_result.get_text()
            print(f"Перше посилання: {link_text}")
            webbrowser.open(link)

        else:
            print("Не вдалося знайти результатів.")

    
    # ФУНКЦІЯ ВІДКРИТТЯ ПРОГРАМ
    def open_program(program_name):
        print(f"Запускаю: {program_name}")
        pyautogui.hotkey('win', 's')  # Відкрити пошук через Win
        time.sleep(1)  # Дати час для відкриття пошуку
        pyautogui.write(program_name, interval=0.1)  # Ввести назву програми
        pyautogui.press('enter')  # Натиснути Enter для запуску програми


    # ФУНКЦІЯ РЕГУЛЮВАННЯ ГУЧНОСТІ
    def set_volume(level):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        print(f"Гучність встановлена на {level}%")
    

    # ФУНКЦІЯ СТВОРЕННЯ ТЕКСТОВОГО ДОКУМЕНТА НА РОБОЧОМУ СТОЛІ
    def create_empty_text_file_on_desktop(filename):
        def get_desktop_path():
            if os.name == 'nt':  # Windows
                return os.path.join(os.environ['USERPROFILE'], 'Desktop')
            else:  # MacOS, Linux
                return os.path.join(os.path.expanduser('~'), 'Desktop')

        desktop_path = get_desktop_path()
        file_path = os.path.join(desktop_path, filename)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                pass  # Create an empty file
            print(f"Created an empty file '{filename}' on the desktop.")
            speak_engine(random.choice(phrases_of_assistant["text_document"]))

        except FileExistsError:
            print(f"File '{filename}' already exists on the desktop.")
            speak_engine(f"Текстовий документ з такою назвою вже існує.")

        except Exception as e:
            print(f"An error occurred while creating file '{filename}': {e}")
            speak_engine(f"Сталась невідома помилка.")


    # ФУНКЦІЯ СТВОРЕННЯ ПАПКИ НА РОБОЧОМУ СТОЛІ
    def create_folder_on_desktop(foldername):
        def get_desktop_path():
            if os.name == 'nt':  # Windows
                return os.path.join(os.environ['USERPROFILE'], 'Desktop')
            else:  # MacOS, Linux
                return os.path.join(os.path.expanduser('~'), 'Desktop')

        desktop_path = get_desktop_path()
        folder_path = os.path.join(desktop_path, foldername)

        try:
            os.mkdir(folder_path)
            print(f"Folder '{foldername}' created on the desktop.")
            speak_engine(random.choice(phrases_of_assistant["folder_complete"]))

        except FileExistsError:
            print(f"Folder '{foldername}' already exists on the desktop.")
            speak_engine(f"Текстовий документ з такою назвою вже існує.")

        except Exception as e:
            print(f"An error occurred while creating folder '{foldername}': {e}")
            speak_engine(f"Сталась невідома помилка.")


    # ФУНКЦІЯ ВИМКНЕННЯ ПРИСТРОЮ
    def shutdown_computer():
        system_name = platform.system()
        if system_name == "Windows":
            #
            os.system("shutdown /s /t 0")
        elif system_name == "Linux" or system_name == "Darwin":
            #
            os.system("shutdown -h now")
        else:
            print(f"Unsupported operating system: {system_name}")


    # ФУНКЦІЯ ПЕРЕЗАПУСКУ ПРИСТРОЮ
    def restart_computer():
        system_name = platform.system()
        if system_name == "Windows":
            os.system("shutdown /r /t 0")
        elif system_name == "Linux" or system_name == "Darwin":
            os.system("shutdown -r now")
        else:
            print(f"Unsupported operating system: {system_name}")


    # ФУНКЦІЯ РЕЖИМУ СНУ
    def sleep_computer():
        system_name = platform.system()
        if system_name == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif system_name == "Linux":
            os.system("systemctl suspend")
        elif system_name == "Darwin":
            os.system("pmset sleepnow")
        else:
            print(f"Unsupported operating system: {system_name}")

    
    # ФУНКЦІЯ ДРУКУ ТЕКСТУ
    def paste_text(text):
        # Копіюємо текст у буфер обміну
        pyperclip.copy(text)
        # Очікуємо, щоб текст був скопійований у буфер обміну
        time.sleep(1)
        # Перемикаємо фокус на відповідне вікно (за необхідності)
        # pyautogui.click(x, y)  # Натискаємо на вікно, куди вставляється текст
        # Очікуємо трохи перед вставкою
        time.sleep(1)
        # Використовуємо pyautogui для вставки тексту
        pyautogui.hotkey('ctrl', 'v')
        # Додаткова затримка після вставки
        time.sleep(1)





    # ФУНКЦІЯ ПЕРЕВІРКИ ТА ЗАПУСКУ КОМАНД
    def process_command(command):
        # ВІДКРИТТЯ САЙТІВ
        if any(cmd in command for cmd in commands["open_info"]):
            speak_engine(random.choice(phrases_of_assistant["perform"]))
            search_query = command.replace(commands["open_info"][0], "").strip()
            
            print(f"Відкриваю: {search_query}")
            speak_engine(random.choice(phrases_of_assistant["open"]) + " " + search_query)
            
            info_search(search_query)


        # ПОШУК В ІНТЕРНЕТІ
        elif any(cmd in command for cmd in commands["search"]):
            speak_engine(random.choice(phrases_of_assistant["perform"]))
            search_query = command.replace(commands["search"][0], "").strip()
            
            print(f"Шукаю в Google: {search_query}")
            speak_engine(random.choice(phrases_of_assistant["looking_for"]) + " " + search_query)
            
            google_search(search_query)


        # ЗАПУСК ПРОГРАМ
        elif any(cmd in command for cmd in commands["run_the_program"]):
            speak_engine(random.choice(phrases_of_assistant["perform"]))
            program_name = command.replace(commands["run_the_program"][0], "").strip()
            
            print(f"Запускаю: {program_name}")
            speak_engine(random.choice(phrases_of_assistant["launch"]) + " " + program_name)

            open_program(program_name)


        # ВИМКНЕННЯ АСИСТЕНТА
        elif any(cmd in command for cmd in commands["stop"]):
            print("Програма зупинена користувачем.")
            speak_engine(random.choice(phrases_of_assistant["finishing_my_work"]))
            return "stop"
        

        # КОТРА ГОДИНА
        elif any(cmd in command for cmd in commands["time_pc"]):
            # Отримання поточного часу
            current_time = datetime.now().strftime('%H:%M')
            speak_engine(f'Зараз: {current_time}')


        # РЕГУЛЮВАННЯ ГУЧНОСТІ
        elif any(cmd in command for cmd in commands["volume"]):
            program_name = command.replace(commands["run_the_program"][0], "").strip()
            try:
                if "всю" in program_name:
                    speak_engine(random.choice(phrases_of_assistant["perform"]))
                    set_volume(100)
                    speak_engine("Встановлена гучність 100%")

                elif "сто" in program_name:
                    speak_engine(random.choice(phrases_of_assistant["perform"]))
                    set_volume(100)
                    speak_engine("Встановлена гучність 100%")

                elif "мінімум" in program_name:
                    speak_engine(random.choice(phrases_of_assistant["perform"]))
                    set_volume(0)
                    speak_engine("Встановлена гучність 0%")
                
                elif "нуль" in program_name:
                    speak_engine(random.choice(phrases_of_assistant["perform"]))
                    set_volume(0)
                    speak_engine("Встановлена гучність 0%")

                elif program_name[-1] == "на":
                    pass
                
                else:
                    speak_engine(random.choice(phrases_of_assistant["perform"]))
                    level = int(program_name.split()[-1])
                    if 0 <= level <= 100:
                        set_volume(level)
                        speak_engine(f"Встановлена гучність {level}%")

                    else:
                        print("Рівень гучності повинен бути від 0 до 100.")

            except ValueError:
                print("Не вдалося розпізнати рівень гучності. Будь ласка, скажіть рівень гучності від 0 до 100.")
                speak_engine("Не вдалося розпізнати рівень гучності.")


        # СТВОРЕННЯ ТЕКСТОВОГО ДОКУМЕНТА
        elif any(cmd in command for cmd in commands["create_text_document"]):
            speak_engine(random.choice(phrases_of_assistant["perform"]))
            filename = "empty_example.txt"
            create_empty_text_file_on_desktop(filename)


        # СТВОРЕННЯ ПАПКИ
        elif any(cmd in command for cmd in commands["create_folder"]):
            speak_engine(random.choice(phrases_of_assistant["perform"]))
            foldername = "NewFolder"
            create_folder_on_desktop(foldername)


        # ВИМКНЕННЯ ПРИСТРОЮ
        elif any(cmd in command for cmd in commands["completion_of_work"]):
            speak_engine(random.choice(phrases_of_assistant["shutdown_complete"]))
            shutdown_computer()


        # ПЕРЕЗАПУСК ПРИСТРОЮ
        elif any(cmd in command for cmd in commands["reboot_pc"]):
            speak_engine(random.choice(phrases_of_assistant["reboot_complete"]))
            restart_computer()


        # РЕЖИМ СНУ
        elif any(cmd in command for cmd in commands["sleep_mode_pc"]):
            speak_engine(random.choice(phrases_of_assistant["sleep_mode_complete"]))
            sleep_computer()

        
        # ДРУК ТЕКСТУ
        elif any(cmd in command for cmd in commands["write_right_now"]):
            text_to_paste = command.replace(commands["write_right_now"][0], "").strip()
            print(f"Вставляю: {text_to_paste}")
            speak_engine(random.choice(phrases_of_assistant["perform"]))
            paste_text(text_to_paste)
        
        else:
            print("Невідома команда. Спробуйте ще раз.")
        return None
    

    # ПРОСЛУХОВУВАННЯ МІКРОФОНУ
    def recognize_speech_from_microphone():
        speak_engine("Cлухаю!")
        recognizer = sr.Recognizer()
        listening_mode = False
        last_activation_time = 0

        while True:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)

                try:
                    print("Очікування голосової команди...")
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
                    command = recognizer.recognize_google(audio, language="uk-UA").lower()
                    print(f"Ви сказали: {command}")

                    current_time = time.time()

                    if any(assistant_name in command for assistant_name in commands["assistant"]):
                        print("Слухаю!")

                        for assistant_name in commands["assistant"]:
                            if assistant_name in command:
                                command = command.replace(assistant_name, "").strip()  # Видалити ім'я з команди
                                break
                        
                        last_activation_time = current_time
                        listening_mode = True
                        
                        print(f"Команда після видалення тригера: {command}")
                        
                        # Обробка команди одразу після видалення тригера
                        result = process_command(command)
                        if result == "stop":
                            break

                        last_activation_time = current_time  # Обнулити таймер після успішної команди
                        continue  # Продовжити слухати наступну команду

                    if listening_mode:
                        if current_time - last_activation_time > 60:
                            listening_mode = False
                            print("Режим команд деактивовано.")
                        else:
                            result = process_command(command)
                            if result == "stop":
                                break
                            last_activation_time = current_time  # Обнулити таймер після успішної команди

                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"Помилка сервісу розпізнавання мови: {e}")
                    break
                except KeyboardInterrupt:
                    print("Програма зупинена користувачем.")
                    break

    if __name__ == "__main__":
        recognize_speech_from_microphone()
        


eel.init('web')
eel.start('main.html', size=(490,780))