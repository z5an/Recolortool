import os
import sys
import time
from PIL import Image
import tkinter as tk
from tkinter import colorchooser, filedialog
from tqdm import tqdm

# Farben für die Terminal-Ausgabe
RESET = "\033[0m"
BOLD = "\033[1m"
WHITE = "\033[97m"
GRAY = "\033[90m"
DARK_BLUE = "\033[34m"  # Dunkelblau für den Titel
DARK_RED = "\033[31m"
LIGHT_BLUE = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"  # Grüner Text (für "Fertig!" und Erfolgsmeldungen)
MAGENTA = "\033[35m"  # Magenta für "By Sean"
CYAN = "\033[36m"  # Cyan für wichtige Hinweise
ORANGE = "\033[38;5;214m"  # Orange für Warnungen

# Emojis für eine coole Ausgabe
CHECKMARK = "✅"
COPY = "📂"
WARNING = "⚠️"
COLOR_PICKER = "🎨"
FOLDER = "📁"
INFO = "ℹ️"

# Titel anzeigen mit Kasten
def print_title():
    print(f"{LIGHT_BLUE}{'=' * 60}{RESET}")
    print(f"{DARK_BLUE}{BOLD}{'RECOLOR TOOL'.center(60)}{RESET}")  # Größerer Titel in Dunkelblau
    print(f"{MAGENTA}{'By Sean'.center(60)}{RESET}")  # "By Sean" in Magenta
    print(f"{LIGHT_BLUE}{'=' * 60}{RESET}")
    print(f"{CYAN}{INFO} {YELLOW}{WARNING} Achtung!{WHITE} Bitte das Texturepack entzippen oder extrahieren!{RESET}\n")

# PNGs in einem Ordner suchen
def find_images(folder):
    png_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".png"):
                png_files.append(os.path.join(root, file))
    return png_files

# Bild einfärben
def recolor_image(image_path, color):
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"{RED}{WARNING} Fehler beim Öffnen von {image_path}: {str(e)}{RESET}")
        return None
        
    r, g, b = color
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            pr, pg, pb, a = pixels[x, y]
            new_r = int((pr / 255) * r)
            new_g = int((pg / 255) * g)
            new_b = int((pb / 255) * b)
            pixels[x, y] = (new_r, new_g, new_b, a)
    
    return img

# Hauptfunktion
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print_title()
    input(f"{CYAN}{INFO} Drücke ENTER, um fortzufahren...{RESET}")

    input_folder = "input"
    output_folder = "output"
    
    if not os.path.exists(input_folder):
        print(f"{RED}{WARNING} {INFO} Ordner 'input' nicht gefunden!{RESET}")
        sys.exit(1)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Farbauswahl über GUI
    print(f"\n{COLOR_PICKER} Wähle eine Farbe aus:")
    root = tk.Tk()
    root.withdraw()
    color_code = colorchooser.askcolor(title="Wähle eine Farbe für die Texturen")[0]
    if not color_code:
        print(f"{RED}{WARNING} {INFO} Keine Farbe gewählt. Beende...{RESET}")
        sys.exit(1)
    selected_color = tuple(map(int, color_code))

    # Texturen recoloren oder kopieren
    files = find_images(input_folder)
    total_operations = len(files)
    
    # mcdata Dateien finden
    mcdata_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".mcmeta") or file.endswith(".mcdata"):
                mcdata_files.append((root, file))
    
    total_operations += len(mcdata_files)
    print(f"\n{COLOR_PICKER} Verarbeite Dateien...")
    
    with tqdm(total=total_operations, 
             bar_format='{l_bar}{bar:30}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
             unit="Datei",
             colour='cyan') as pbar:
        
        # Bilder verarbeiten
        for file in files:
            relative_path = os.path.relpath(file, input_folder)
            output_path = os.path.join(output_folder, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            recolored_img = recolor_image(file, selected_color)
            if recolored_img is not None:
                recolored_img.save(output_path)
            pbar.update(1)

        # Metadaten kopieren
        if mcdata_files:
            for root, file in mcdata_files:
                input_mcdata_path = os.path.join(root, file)
                output_mcdata_path = os.path.join(output_folder, os.path.relpath(input_mcdata_path, input_folder))
                os.makedirs(os.path.dirname(output_mcdata_path), exist_ok=True)
                os.system(f"copy \"{input_mcdata_path}\" \"{output_mcdata_path}\"" if os.name == "nt" else f"cp \"{input_mcdata_path}\" \"{output_mcdata_path}\"")
                pbar.update(1)

    print(f"\n{GREEN}{CHECKMARK} Fertig!{RESET}")
    time.sleep(2)

if __name__ == "__main__":
    main()