import os
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class LogoGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess the character")
        self.master.configure(bg="#000000")
        self.logo_folder = "logos"
        self.logos = self.load_logos()
        self.used_logos = []
        self.create_widgets()
        self.shuffle_logos()
        self.center_window()
        self.master.geometry("800x600")

    def load_logos(self):
        logos = []
        for file in os.listdir(self.logo_folder):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                logos.append(file)
        return logos

    def shuffle_logos(self):
        random.shuffle(self.logos)
        self.next_logo()

    def next_logo(self):
        if self.logos:
            self.current_logo = self.logos.pop()
            self.used_logos.append(self.current_logo)
            self.current_logo_path = os.path.join(self.logo_folder, self.current_logo)
            self.show_logo()
        else:
            self.show_game_over()

    def resize_image(self, image_path, max_size=(600, 400)):
        original_image = Image.open(image_path)
        original_width, original_height = original_image.size
        ratio = min(max_size[0] / original_width, max_size[1] / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        resampling_method = getattr(Image, 'LANCZOS', getattr(Image, 'ANTIALIAS', 'antialias'))
        resized_image = original_image.resize(new_size, resampling_method)
        return ImageTk.PhotoImage(resized_image)

    def show_logo(self):
        try:
            logo_image = self.resize_image(self.current_logo_path)
            self.logo_label.config(image=logo_image)
            self.logo_label.image = logo_image
        except tk.TclError:
            self.next_logo()

    def show_game_over(self):
        game_status = "You won! All logos identified." if self.used_logos else "All logos used. Try again!"
        self.game_over_label = tk.Label(self.master, text=game_status, font=("Helvetica", 24), bg="#000000", fg="#00FF00")  # Neon green
        self.game_over_label.pack(pady=10)
        self.restart_button = tk.Button(self.master, text="Restart Game", command=self.restart_game, bg="#0000FF", fg="#000000")  # Neon blue with black text
        self.restart_button.pack(pady=10)
        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED, bg="#000000", fg="#FF00FF")  # Neon pink
        self.load_button.config(state=tk.DISABLED, bg="#000000", fg="#FF00FF")  # Neon pink

    def check_guess(self):
        user_guess = self.answer_entry.get().lower()
        if user_guess == self.current_logo.split('.')[0].lower():
            self.next_logo()
            self.answer_entry.delete(0, tk.END)
        else:
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.insert(0, "Incorrect Guess. Try again!")

    def create_widgets(self):
        self.frame = tk.Frame(self.master, bg="#000000")
        self.frame.pack(pady=10)
        self.logo_label = tk.Label(self.frame, bg="#000000")
        self.logo_label.pack(pady=10)
        self.answer_label = tk.Label(self.frame, text="Your Guess:", bg="#000000", fg="#00FFFF")  # Neon cyan
        self.answer_label.pack()
        self.answer_entry = tk.Entry(self.frame)
        self.answer_entry.pack()
        self.submit_button = tk.Button(self.frame, text="Submit Guess", command=self.check_guess, bg="#FFD700", fg="#000000")  # Gold with black text
        self.submit_button.pack(pady=10)
        self.load_button = tk.Button(self.frame, text="Load More Logos", command=self.load_more_logos, bg="#FF00FF", fg="#000000")  # Neon pink with black text
        self.load_button.pack(pady=10)

    def load_more_logos(self):
        additional_logos = filedialog.askopenfilenames(
            initialdir=os.getcwd(),
            title="Select Logo Files",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*"))
        )
        if additional_logos:
            self.logos.extend(additional_logos)
            self.shuffle_logos()
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.insert(0, "New logos loaded. Guess the next logo!")

    def restart_game(self):
        if hasattr(self, 'game_over_label'):
            self.game_over_label.pack_forget()
        if hasattr(self, 'restart_button'):
            self.restart_button.pack_forget()
        self.logos.extend(self.used_logos)
        self.used_logos = []
        self.shuffle_logos()
        self.answer_entry.delete(0, tk.END)
        self.logo_label.config(image=None, text="")
        self.answer_entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.load_button.config(state=tk.NORMAL)

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 800  # Set an initial width
        window_height = 600  # Set an initial height
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#000000")  # Set overall background color to black
    game = LogoGuessingGame(root)
    root.mainloop()
