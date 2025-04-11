import os
import cv2
import tkinter as tk
from tkinter import simpledialog, filedialog

def capture_photo():
    print("Spúšťam kameru...")
    # Spustenie kamery
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Nemôžem otvoriť kameru")
        return

    # Vytvorenie okna pre zobrazenie kamery
    cv2.namedWindow("Webkamera")

    print("Kamera otvorená. Stlač 'q' na zachytenie fotky, 'ESC' na ukončenie.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Chyba pri čítaní rámu")
            break
        
        # Zobrazenie náhľadu z kamery
        cv2.imshow("Webkamera", frame)

        # Stlačením 'q' sa foto odfotí
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Stlačenie 'q' urobí fotku
            print("Fotka zachytená!")
            filename = ask_filename()  # Funkcia na zadanie názvu súboru
            folder_path = ask_folder()  # Funkcia na výber priečinka
            file_path = os.path.join(folder_path, filename)  # Vytvorí úplnú cestu k súboru
            cv2.imwrite(file_path, frame)  # Uloženie súboru
            print(f"Obrázok uložený ako {file_path}")
            # Po uložení sa opäť prepne focus na okno kamery
            cv2.setWindowProperty("Webkamera", cv2.WND_PROP_TOPMOST, 1)
        
        # Stlačením 'ESC' ukončíš aplikáciu
        elif key == 27:  # 'ESC' klávesa (ASCII 27) ukončí skript
            print("Ukončujem kameru...")
            break

    # Uvoľnenie kamery a zavretie okien
    cap.release()
    cv2.destroyAllWindows()

# Funkcia na zobrazenie dialógu pre zadanie názvu súboru
def ask_filename():
    # Vytvorenie základného okna
    root = tk.Tk()
    root.withdraw()  # Skryje hlavné okno

    # Otvorí dialógové okno na zadanie názvu súboru
    filename = simpledialog.askstring("Zadaj názov súboru", "Zadaj názov pre uložený obrázok (s príponou .jpg):")
    if filename:
        # Ak nebolo zadané prípona, pridáme ju
        if not filename.endswith('.jpg'):
            filename += '.jpg'
        return filename
    else:
        return 'image.jpg'  # Default názov súboru

# Funkcia na výber priečinka
def ask_folder():
    # Vytvorenie základného okna
    root = tk.Tk()
    root.withdraw()  # Skryje hlavné okno

    # Otvorí dialógové okno na výber priečinka
    folder_path = filedialog.askdirectory(title="Vyber priečinok pre uloženie fotky")
    
    if folder_path:
        return folder_path
    else:
        return os.getcwd()  # Ak nie je vybraný priečinok, použije sa aktuálny priečinok

# Spustenie skriptu
capture_photo()
