import pyfiglet
import os
import platform
import requests
from colorama import init, Fore
import time

# Initialisation de colorama pour la gestion des couleurs
init(autoreset=True)

# Fonction pour redimensionner la fenêtre de la console
def resize_console(width, height):
    if platform.system() == "Windows":
        os.system(f"mode con: cols={width} lines={height}")
    else:
        os.system(f"printf '\e[8;{height};{width}t'")

# Fonction pour effacer l'écran
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction pour afficher le texte de démarrage
def display_startup_text():
    clear_console()  # Efface l'écran avant d'afficher le texte
    ascii_art = pyfiglet.figlet_format("Dischook Hub", font="slant")  # Créer le texte ASCII
    lines = ascii_art.splitlines()
    max_length = max(len(line) for line in lines)

    # Créer une ligne d'encadrement inférieure
    frame_line = "─" * (max_length + 2)  # +2 pour les espaces de chaque côté

    # Afficher les lignes du texte
    for line in lines:
        print(Fore.RED + line.center(max_length))  # Centrer le texte
    print(Fore.RED + frame_line)  # Ligne inférieure

    # Espacer le titre du prompt
    print("\n" * 2)  # Deux lignes d'espace

# Redimensionner la fenêtre de la console
resize_console(80, 15)

# Afficher le texte de démarrage
display_startup_text()

# Variables pour stocker l'URL de la webhook et les messages envoyés
webhook_url = None
messages_sent = []
is_sending = False
last_message_time = time.time()

# Historique des commandes
command_history = []
history_index = -1

# Afficher le prompt de commande initialement
command_prompt = Fore.WHITE + "Enter your command: "
print(command_prompt, end="", flush=True)

# Boucle pour maintenir la fenêtre ouverte
while True:
    try:
        command = input()  # Demander la commande

        # Effacer le prompt précédent
        print("\r" + " " * len(command_prompt), end="", flush=True)  # Effacer le prompt

        # Gérer l'historique des commandes
        if command == "!undo":
            if history_index > 0:
                history_index -= 1
                command = command_history[history_index]
            else:
                print(Fore.RED + "No command to undo.")
                print(command_prompt, end="", flush=True)
                continue
        else:
            command_history.append(command)
            history_index = len(command_history)

        # Effacer l'écran après chaque commande
        clear_console()

        # Réafficher le titre
        display_startup_text()

        # Vérifier si la commande est "!restart"
        if command.lower() == "!restart":
            display_startup_text()  # Affiche le texte de démarrage à nouveau
            webhook_url = None  # Réinitialise la webhook
            print(command_prompt, end="", flush=True)
            continue  # Recommence la boucle pour demander une nouvelle commande

        # Vérifier si la commande est une URL de webhook Discord
        if command.startswith("https://discord.com/api/webhooks/"):
            webhook_url = command
            is_sending = True
            print(Fore.CYAN + "Webhook URL saved.")
            print(command_prompt, end="", flush=True)
            continue  # Retourne au début de la boucle

        # Vérifier si la commande est "!webhook"
        elif command.lower() == "!webhook":
            url_to_display = webhook_url if webhook_url else "Nothing"
            print(Fore.GREEN + f"Current webhook: {url_to_display}")
            print(command_prompt, end="", flush=True)
            continue  # Retourne au début de la boucle

        # Vérifier si la commande est "stop"
        elif command.lower() == "stop":
            webhook_url = None
            is_sending = False
            print(Fore.RED + "Message sending has been stopped.")
            print(command_prompt, end="", flush=True)
            continue  # Retourne au début de la boucle

        # Vérifier si la commande est "!spam"
        elif command.lower().startswith("!spam "):
            parts = command.split(' ', 2)
            if len(parts) < 3:
                print(Fore.RED + "Usage: !spam [Number of messages] [Message]")
                print(command_prompt, end="", flush=True)
                continue

            try:
                number_of_messages = int(parts[1])
                spam_message = parts[2].strip('"')

                for _ in range(number_of_messages):
                    if webhook_url:
                        try:
                            data = {"content": spam_message}
                            response = requests.post(webhook_url, json=data)

                            if response.status_code == 204:
                                messages_sent.append(spam_message)
                                print(Fore.GREEN + "Message sent successfully.")
                            else:
                                print(Fore.RED + f"Error sending message: {response.status_code}")
                        except Exception as e:
                            print(Fore.RED + f"An error occurred: {e}")
                    else:
                        print(Fore.RED + "Webhook not defined, unable to send the message.")

                print(command_prompt, end="", flush=True)
                continue  # Retourne au début de la boucle

            except ValueError:
                print(Fore.RED + "The number of messages must be an integer.")
                print(command_prompt, end="", flush=True)

        # Envoi du message à la webhook si elle est définie et que l'envoi est activé
        elif is_sending and webhook_url:
            current_time = time.time()

            if current_time - last_message_time < 1:
                # Empêcher d'envoyer trop de messages en peu de temps
                print(Fore.RED + "Too many messages sent quickly. Please wait a second.")
                time.sleep(1)
                print(command_prompt, end="", flush=True)
                continue

            # Envoi d'un message à la webhook
            try:
                data = {"content": command}
                response = requests.post(webhook_url, json=data)

                if response.status_code == 204:
                    messages_sent.append(command)
                    print(Fore.GREEN + "Message sent successfully.")
                else:
                    print(Fore.RED + f"Error sending message: {response.status_code}")

            except Exception as e:
                print(Fore.RED + f"An error occurred: {e}")

            last_message_time = current_time
        else:
            print(Fore.RED + "Unrecognized command or webhook not defined.")
            print(command_prompt, end="", flush=True)

    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")