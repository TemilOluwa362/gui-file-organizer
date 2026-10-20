import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import shutil
window = tk.Tk()
window.title("File Organizer")
window.geometry("500x400")
window.resizable(False, False)
chosen_folder = ""
folder_label = tk.Label(window, text="No folder chosen")
def choose_folder():
    global chosen_folder 
    chosen_folder = filedialog.askdirectory()
    folder_label.config(text=chosen_folder)

CATEGORIES = {"Images": {".jpg", ".png", ".jpeg", ".gif"},
              "Documents": {".pdf", ".docx", ".txt", ".pptx", ".ppt", ".xlsx", ".csv", ".htm", ".html"},
              "Videos": {".mp4", ".mov", ".mkv"},
              "Archives": {".zip", ".rar", ".7z"},
              "Installers": {".exe", ".msi"}
              }

def get_category(extension):
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"

browse_button = tk.Button(window, text="Browse", command=choose_folder)
browse_button.pack(fill="x", padx=10, pady=5)
folder_label.pack()
result = tk.Text(window, height=15, width=60)
result.pack()

def preview():
    if chosen_folder == "":
        result.insert("end", "Please select a folder.")
        return
    result.delete("1.0", "end")
    folder = Path(chosen_folder)
    for item in folder.iterdir():
        if not item.is_file():
            continue
        if item.suffix.lower() == "" or item.name.startswith("~") or item.suffix.lower() == ".crdownload" or item.name.lower() == "desktop.ini":
            continue
        category = get_category(item.suffix.lower())
        result.insert("end", f"{item.name} -> {category}\n")
preview_button = tk.Button(window, text="Preview", command=preview)
preview_button.pack(fill="x", padx=10, pady=5)

def organize():
    if chosen_folder == "":
        result.insert("end", "Please select a folder.")
        return
    answer = messagebox.askyesno("Confirmation", "Organize files in this folder?")
    if answer != True:
        return
    result.delete("1.0", "end")
    folder = Path(chosen_folder)
    counter = 0
    for item in folder.iterdir():
        if not item.is_file():
            continue
        if item.suffix.lower() == "" or item.name.startswith("~") or item.suffix.lower() == ".crdownload" or item.name.lower() == "desktop.ini":
            continue
        category = get_category(item.suffix.lower())
        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)
        destination_file = destination_folder / item.name
        count = 1
        while destination_file.exists():
            destination_file = destination_folder / f"{item.stem}_{count}{item.suffix}"
            count += 1
        shutil.move(str(item), str(destination_file))
        counter +=1
        result.insert("end", f"{destination_file.name} -> {category}\n")
    if counter == 0:
        result.insert("end", "No file to organize!")
    elif counter == 1:
        result.insert("end", "Moved 1 file.")
    else:
        result.insert("end", f"Moved {counter} files.")
organize_button = tk.Button(window, text="Organize", command=organize)
organize_button.pack(fill="x", padx=10, pady=5)

window.mainloop()