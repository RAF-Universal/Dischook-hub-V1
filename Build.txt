import os
import platform
import subprocess
from pathlib import Path

# Fonction pour obtenir le chemin des dossiers "Documents" et "Downloads" en fonction de la langue du système
def get_user_folders():
    system = platform.system()

    if system == "Windows":
        documents_folder = os.path.join(Path.home(), "Documents")
        downloads_folder = os.path.join(Path.home(), "Downloads")
    elif system == "Linux" or system == "Darwin":  # Pour Linux et macOS
        documents_folder = os.path.join(Path.home(), "Documents")
        downloads_folder = os.path.join(Path.home(), "Downloads")
    else:
        documents_folder = None
        downloads_folder = None

    return documents_folder, downloads_folder

# Fonction pour rechercher le fichier "Script.txt" dans les répertoires standard
def find_script_file():
    documents_folder, downloads_folder = get_user_folders()

    # Chemin cible : DiscHook-Hub V1/other
    target_path = os.path.join("DiscHook-Hub V1", "other")
    
    if documents_folder:
        doc_script_path = os.path.join(documents_folder, target_path, "Script.txt")
        if os.path.exists(doc_script_path):
            return doc_script_path
    
    if downloads_folder:
        down_script_path = os.path.join(downloads_folder, target_path, "Script.txt")
        if os.path.exists(down_script_path):
            return down_script_path
    
    return None

# Fonction pour sauvegarder le fichier sous forme d'un fichier .py dans le répertoire courant
def save_as_py_file(script_txt_path):
    # Obtenir le répertoire où le script est exécuté
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Construire le nouveau chemin pour le fichier .py dans ce répertoire
    new_file_name = "Dischook Menu.py"
    new_file_path = os.path.join(current_directory, new_file_name)
    
    try:
        with open(script_txt_path, 'r', encoding='utf-8') as src_file:
            content = src_file.read()

        # Écriture du contenu dans un nouveau fichier avec l'extension .py
        with open(new_file_path, 'w', encoding='utf-8') as dest_file:
            dest_file.write(content)

        print(f'Le fichier a été sauvegardé en tant que "{new_file_name}" dans {current_directory}.')
        print("Build, Finish successfully.")
    
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier : {e}")

# Fonction pour installer les bibliothèques nécessaires
def install_packages():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyfiglet', 'colorama', 'requests'])
        print("Les bibliothèques ont été installées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation des bibliothèques : {e}")

# Installer les bibliothèques nécessaires
install_packages()

# Chemin complet du fichier "Script.txt"
script_txt_path = find_script_file()

# Sauvegarder le fichier sous .py si trouvé
if script_txt_path:
    save_as_py_file(script_txt_path)
else:
    print('Le fichier "Script.txt" est introuvable dans les répertoires standard.')

# Maintenir la fenêtre ouverte jusqu'à ce que l'utilisateur appuie sur Entrée
input("Appuyez sur Entrée pour quitter...")

