import tkinter as tk
from tkinter import filedialog, messagebox, font
import subprocess
from PIL import ImageTk, Image
import os
import threading
import sys


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def set_output_dir():
    directory = filedialog.askdirectory(
        initialdir=os.path.expanduser("~/Desktop"))
    with open("output_dir.txt", "w") as f:
        f.write(directory)
    messagebox.showinfo(
        "Success", f"Image output directory set to {directory}")


def edit_file(filename):
    content = open_file(filename)
    new_window = tk.Toplevel(root)
    new_window.title(f"Editing {filename}")
    new_window.configure(bg='light grey')
    text_widget = tk.Text(new_window, width=60, height=20)
    text_widget.pack(padx=20, pady=20)
    text_widget.insert("1.0", content)

    def save_changes():
        new_content = text_widget.get("1.0", "end")
        save_file(filename, new_content)
        messagebox.showinfo(
            "Success", f"Changes to {filename} saved successfully!")

    save_button = tk.Button(new_window, text="Save changes", command=save_changes, font=(
        'Helvetica', '16'), bg='sky blue', activebackground='deep sky blue', bd=0, relief='sunken')
    save_button.pack(pady=20)


def run_script():
    script_path = 'app.py'
    threading.Thread(target=subprocess.run, args=(
        ['python', script_path], )).start()


root = tk.Tk()
root.title("ImageGenius")
root.configure(bg='white')  # white for peace and honesty
root.geometry("500x480")
root.resizable(False, False)

# Set the icon
root.iconbitmap(resource_path("art.ico"))

bg = ImageTk.PhotoImage(Image.open(resource_path("background.png")))
bg_label = tk.Label(root, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

button_font = font.Font(family='Helvetica', size=14,
                        weight='bold')  # smaller button font

button1 = tk.Button(root, text="Agent007", command=lambda: edit_file('chatbot1.txt'),
                    # red for hardiness, bravery, strength, and courage
                    bg='red', activebackground='dark red', bd=5, relief='raised',
                    fg='white',  # white text
                    height=3, width=25, font=button_font)  # further smaller button
button1.grid(row=0, column=0, padx=10, pady=10)

button2 = tk.Button(root, text="AgentX", command=lambda: edit_file('chatbot2.txt'),
                    # green for hope, joy, and love
                    bg='green', activebackground='dark green', bd=5, relief='raised',
                    fg='white',  # white text
                    height=3, width=25, font=button_font)  # further smaller button
button2.grid(row=0, column=1, padx=10, pady=10)

run_button = tk.Button(root, text="Run", command=run_script,
                       # white for peace and honesty
                       bg='white', activebackground='light grey', bd=5, relief='raised',
                       fg='black',  # black text
                       height=3, width=25, font=button_font)  # further smaller button
run_button.grid(row=1, column=0, padx=10, pady=10, )

output_dir_button = tk.Button(root, text="Save To",
                              command=set_output_dir,
                              # black for determination and defeat of enemies
                              bg='black', activebackground='grey', bd=5, relief='raised',
                              fg='white',  # white text
                              height=3, width=25, font=button_font)  # further smaller button
output_dir_button.grid(row=1, column=1, padx=10, pady=10,)

quit_button = tk.Button(root, text="Stop Program", command=root.quit,
                        # dark grey for neutral quit operation
                        bg='#A00000', activebackground='grey', bd=5, relief='raised',
                        fg='white',  # white text
                        height=3, width=25, font=button_font)  # further smaller button
quit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10,)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
