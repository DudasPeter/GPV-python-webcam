import os
import cv2
import tkinter as tk
from tkinter import simpledialog, filedialog
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Tlačidlo na odfotenie
        self.capture_button = tk.Button(window, text="Odfotiť", width=15, command=self.capture_photo)
        self.capture_button.pack(pady=10)

        # Vytvorenie videa (webkamera)
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Nemôžem otvoriť kameru")
            self.window.quit()

        # Vytvorenie Canvas pre zobrazenie kamery
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        # Načítanie videa
        self.update_video()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_video(self):
        # Načítanie rámu z webkamery
        ret, frame = self.cap.read()
        if ret:
            # Konverzia obrazu na RGB a následná konverzia na Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            self.photo = ImageTk.PhotoImage(image=image)

            # Zobrazenie obrazu na plátne
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Opakuje sa každých 10 ms
        self.window.after(10, self.update_video)

    def capture_photo(self):
        print("Fotka zachytená!")
        filename = self.ask_filename()  # Funkcia na zadanie názvu súboru
        if filename:  # Ak používateľ nezruší zadanie názvu
            folder_path = self.ask_folder()  # Funkcia na výber priečinka
            file_path = os.path.join(folder_path, filename)  # Vytvorí úplnú cestu k súboru

            # Načítanie rámu z webkamery
            ret, frame = self.cap.read()
            if ret:
                if cv2.imwrite(file_path, frame):  # Uloženie súboru
                    print(f"Obrázok uložený ako {file_path}")
                else:
                    print("Chyba pri ukladaní obrázka!")
        else:
            print("Zadanie názvu bolo zrušené, pokračujem v zobrazení kamery.")

    def ask_filename(self):
        # Zobrazí dialóg na zadanie názvu súboru
        filename = simpledialog.askstring("Zadaj názov súboru", "Zadaj názov pre uložený obrázok (s príponou .jpg):")
        if filename:
            # Ak nebolo zadané prípona, pridáme ju
            if not filename.endswith('.jpg'):
                filename += '.jpg'
            return filename
        else:
            return None  # Ak používateľ zruší zadanie názvu, vrátime None

    def ask_folder(self):
        # Zobrazí dialóg na výber priečinka
        folder_path = filedialog.askdirectory(title="Vyber priečinok pre uloženie fotky")
        if folder_path:
            return folder_path
        else:
            return os.getcwd()  # Ak nie je vybraný priečinok, použije sa aktuálny priečinok

    def on_closing(self):
        # Uvoľní kameru pri zatváraní okna
        print("Ukončujem kameru...")
        self.cap.release()
        self.window.quit()


# Spustenie aplikácie
root = tk.Tk()
app = CameraApp(root, "Kamera s tlačidlom na odfotenie")
root.mainloop()
