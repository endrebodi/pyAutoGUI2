import time
import tkinter as tk
from tkinter import ttk, filedialog
import os
import webbrowser
import pyautogui
import tkinter.messagebox as messagebox


def documentation_window():
    documentation = tk.Toplevel(root)
    documentation.title("Documentation")
    documentation.geometry("340x240")

    documentation_frame = tk.Frame(documentation)
    documentation_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    twitter_link = tk.Label(documentation_frame, text="PyAutoGUI2", cursor="hand2", fg="blue")
    twitter_link.pack(pady=5)
    twitter_link.bind("<Button-1>", lambda e: webbrowser.open("https://pyautogui2.com"))

    github_link = tk.Label(documentation_frame, text="PyAutoGUI", cursor="hand2", fg="blue")
    github_link.pack(pady=5)
    github_link.bind("<Button-1>", lambda e: webbrowser.open("https://pyautogui.readthedocs.io/en/latest/quickstart.html"))

    documentation.geometry("+%d+%d" % (root.winfo_rootx() + 220, root.winfo_rooty() + 100))


def developer_window():
    developer = tk.Toplevel(root)
    developer.title("Developer")
    developer.geometry("340x240")

    developer_frame = tk.Frame(developer)
    developer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label = tk.Label(developer_frame, text="Created by Endre Bodi,\nbased on PyAutoGUI by Al Sweigart.")
    label.pack(pady=10)

    github_link = tk.Label(developer_frame, text="GitHub", cursor="hand2", fg="blue")
    github_link.pack(pady=5)
    github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/endrebodi"))

    twitter_link = tk.Label(developer_frame, text="Twitter", cursor="hand2", fg="blue")
    twitter_link.pack(pady=5)
    twitter_link.bind("<Button-1>", lambda e: webbrowser.open("https://twitter.com/endrebodi"))

    developer.geometry("+%d+%d" % (root.winfo_rootx() + 220, root.winfo_rooty() + 100))


def add_option():
    selected_option = dropdown_var.get()
    if selected_option == "Move cursor to coordinate":
        get_mouse_position()
    elif selected_option == "Drag cursor to coordinate":
        drag_mouse()
    elif selected_option == "Locate on screen and move cursor":
        locate_on_screen()
    elif selected_option == "Left click":
        textbox.insert(tk.END, "pyautogui.click()\n")
    elif selected_option == "Middle click":
        textbox.insert(tk.END, "pyautogui.click(button='middle')\n")
    elif selected_option == "Right click":
        textbox.insert(tk.END, "pyautogui.click(button='right')\n")
    elif selected_option == "Scroll":
        textbox.insert(tk.END, "pyautogui.scroll(-500)\n")
    elif selected_option == "Sleep":
        textbox.insert(tk.END, "time.sleep(3)\n")
    elif selected_option == "Type text":
        textbox.insert(tk.END, "pyautogui.typewrite('Replace this with your text', interval=0.2)\n")
    elif selected_option == "Copy":
        textbox.insert(tk.END, "pyautogui.hotkey('ctrl', 'c')\n")
    elif selected_option == "Paste":
        textbox.insert(tk.END, "pyautogui.hotkey('ctrl', 'v')\n")
    else:
        textbox.insert(tk.END, f"{selected_option}\n")


def get_mouse_position():
    time.sleep(5)
    cursor_position = pyautogui.position()
    cursor_position_x = cursor_position[0]
    cursor_position_y = cursor_position[1]
    textbox.insert(tk.END, f"pyautogui.moveTo({cursor_position_x},{cursor_position_y}, 0.2)\n")


def locate_on_screen():
    # Check if script is saved and folder exists
    global folder_name_without_extension
    folder = f"{folder_name_without_extension}_images"
    if not os.path.exists(folder):
        messagebox.showwarning("Warning", "You must save the script before running the locate on screen function.")
    else:
        textbox.insert(tk.END, f"screenshot = os.path.join('{folder}', 'screenshot.png')\n")
        textbox.insert(tk.END, "x, y = pyautogui.locateCenterOnScreen(screenshot)\n")
        textbox.insert(tk.END, "pyautogui.moveTo(x, y, 0.2)\n")


def drag_mouse():
    time.sleep(5)
    cursor_position = pyautogui.position()
    cursor_position_x = cursor_position[0]
    cursor_position_y = cursor_position[1]
    textbox.insert(tk.END, f"pyautogui.dragTo({cursor_position_x},{cursor_position_y}, 0.2)\n")


def copy_text():
    try:
        selected_text = textbox.get(textbox.index(tk.SEL_FIRST), textbox.index(tk.SEL_LAST))
        root.clipboard_clear()
        root.clipboard_append(selected_text)
    except tk.TclError:
        pass


def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)


def new_script():
    textbox.delete("1.0", tk.END)
    current_directory = os.getcwd()
    file_path = filedialog.asksaveasfilename(initialdir=current_directory, defaultextension=".py", filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        return

    # Get the folder name without the extension
    file_name = os.path.basename(file_path)
    global folder_name_without_extension
    folder_name_without_extension = os.path.splitext(file_name)[0]

    script_folder = f"{os.path.splitext(file_path)[0]}_images"
    os.makedirs(script_folder, exist_ok=True)

    with open(file_path, "w") as file:
        file.write(textbox.get("1.0", tk.END))


def save_script():
    current_directory = os.getcwd()
    file_path = filedialog.asksaveasfilename(initialdir=current_directory, defaultextension=".py", filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        return

    # Get the file name without the extension
    file_name = os.path.basename(file_path)
    global folder_name_without_extension
    folder_name_without_extension = os.path.splitext(file_name)[0]

    script_folder = f"{os.path.splitext(file_path)[0]}_images"
    os.makedirs(script_folder, exist_ok=True)

    with open(file_path, "w") as file:
        file.write(textbox.get("1.0", tk.END))


def load_script():
    current_directory = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir=current_directory, filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        return

    # Get the file name without the extension
    file_name = os.path.basename(file_path)
    global folder_name_without_extension
    folder_name_without_extension = os.path.splitext(file_name)[0]

    with open(file_path, "r") as file:
        code = file.read()

    textbox.delete("1.0", tk.END)
    textbox.insert("1.0", code)


def run_code():
    code = textbox.get("1.0", tk.END)
    try:
        exec(code)
    except Exception as e:
        textbox.insert(tk.END, f"Error: {e}\n")


folder_name_without_extension = ""


# Create the main window
root = tk.Tk()
root.title("PyAutoGUI2")

# Set the window size to 800x600
root.geometry("800x600")

# Get the screen size
screen_width, screen_height = pyautogui.size()

# Calculate the center position of the window on the screen
x = (screen_width - 800) // 2
y = (screen_height - 600) // 2

# Set the window position to the center of the screen
root.geometry(f"+{x}+{y}")

# Set the padding and spacing for the window
root.config(padx=10, pady=10)
root.columnconfigure(0, weight=1)

# Create the top menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New script", command=new_script)
file_menu.add_command(label="Load script", command=load_script)
file_menu.add_command(label="Save script", command=save_script)
file_menu.add_command(label="Play script", command=run_code)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create the "About" menu
about_menu = tk.Menu(menu_bar, tearoff=0)
about_menu.add_command(label="Documentation", command=documentation_window)
about_menu.add_command(label="Developer", command=developer_window)
menu_bar.add_cascade(label="Help", menu=about_menu)

# Create the dropdown menu
dropdown_var = tk.StringVar(root)
options = ["Move cursor to coordinate", "Locate on screen and move cursor", "Drag cursor to coordinate", "Left click", "Middle click", "Right click", "Scroll",
           "Type text", "Copy", "Paste",
           "Sleep"]
dropdown_var.set(options[0])

dropdown_frame = tk.Frame(root)
dropdown_frame.pack(fill=tk.X, pady=0)

# Use ttk.Combobox instead of OptionMenu
dropdown_menu = ttk.Combobox(dropdown_frame, textvariable=dropdown_var, values=options, state="readonly")
dropdown_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Create the "add" button
add_button = tk.Button(root, text="Add", command=add_option)
add_button.pack(fill=tk.X, pady=10)

# Create the textbox
textbox_frame = tk.Frame(root)
textbox_frame.pack(fill=tk.BOTH, expand=True)

textbox = tk.Text(textbox_frame, wrap=tk.WORD)
textbox.pack(fill=tk.BOTH, expand=True)

# Create a context menu for copying text
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Copy", command=lambda: copy_text())

# Bind the right-click event to the textbox
textbox.bind("<Button-3>", show_context_menu)

# Start the main event loop
root.mainloop()
