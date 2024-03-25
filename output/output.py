import tkinter as tk
import customtkinter as ctk
import serial

# Function to read text from TXT file
def read_txt():
    filename="output/output.txt"
    try:
        with open(filename, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")

font_name = "Calibri"

window = ctk.CTk() 
window.geometry("700x700")
window.resizable(False, False)
window.title("Output")

pors_vyber_frame = ctk.CTkFrame(master=window, width=680, height=680)
pors_vyber_frame.place(x=10, y=10)

hlavnaVysvetlivka=ctk.CTkTextbox(master=pors_vyber_frame, width=660, height= 660, font = (font_name, 13))
hlavnaVysvetlivka.place(x= 10, y=10)

text=str(read_txt())
if text is not None:
    hlavnaVysvetlivka.insert("1.0", text)


if __name__ == '__main__':
    window.mainloop()

    