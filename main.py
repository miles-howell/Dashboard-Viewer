
import os
import sys
import subprocess
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Optional: detect prewarm mode to exit early
if "/prewarm" in sys.argv:
    import tkinter as tk  # force GUI libs to initialize
    root = tk.Tk()
    root.withdraw()  # don't show a window
    root.update_idletasks()
    root.destroy()
    sys.exit()

APP_NAME = "DashboardsApp"
LAUNCH_FLAG = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), f"{APP_NAME}_first_launch.flag")

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

DASHBOARD_FOLDER = os.path.join(os.getcwd(), "dashboards")
LOGO_PATH = resource_path("img/logo.png")
ICON_PATH = resource_path("img/favicon.ico")
CHECKMARK_PATH = resource_path("img/checkmark.png")

DASHBOARDS = {
    "Human Resources": "HR.pptx",
    "Finance": "Finance.pptx",
    "Sales": "Sales.pptx",
    "Operations": "Operations.pptx",
    "Marketing": "Marketing.pptx",
    "IT Support": "IT_Support.pptx",
    "Customer Service": "Customer_Service.pptx",
    "Legal": "Legal.pptx",
    "R&D": "Research_Development.pptx",
    "Executive": "Executive.pptx"
}

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.visited = set()

        try:
            self.iconbitmap(ICON_PATH)
        except Exception as e:
            print(f"Failed to set app icon: {e}")

        self.title("Department Dashboards")
        self.geometry("800x600")
        self.minsize(600, 400)
        self.configure(padx=20, pady=20)

        try:
            check_img_raw = Image.open(CHECKMARK_PATH)
            check_img_resized = check_img_raw.resize((20, 20), Image.LANCZOS)
            self.check_image = ctk.CTkImage(light_image=check_img_resized, dark_image=check_img_resized)
        except Exception as e:
            print(f"Failed to load checkmark image: {e}")
            self.check_image = None

        try:
            image = Image.open(LOGO_PATH)
            image = image.resize((255, 86), Image.LANCZOS)
            self.logo_image = ctk.CTkImage(light_image=image, dark_image=image, size=(255, 86))
            self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="")
            self.logo_label.pack(pady=(0, 10))
        except Exception as e:
            print(f"Failed to load logo: {e}")

        self.title_label = ctk.CTkLabel(self, text="Department Dashboards", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(0, 20))

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True)
        self.populate_buttons()

        self.upload_button = ctk.CTkButton(
            self,
            text="Upload Dashboard",
            font=ctk.CTkFont(weight="bold"),
            height=40,
            command=self.open_upload_popup
        )
        self.upload_button.pack(pady=10)

    def populate_buttons(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        max_columns = 3
        for i in range(max_columns):
            self.grid_frame.grid_columnconfigure(i, weight=1)

        for idx, (dept, filename) in enumerate(DASHBOARDS.items()):
            row = idx // max_columns
            col = idx % max_columns

            full_path = os.path.join(DASHBOARD_FOLDER, filename)

            btn = ctk.CTkButton(
                self.grid_frame,
                text=dept,
                font=ctk.CTkFont(weight="bold"),
                height=40,
                command=lambda p=full_path, d=dept, b=None: self.open_file(p, d, b)
            )

            btn.configure(command=lambda p=full_path, d=dept, b=btn: self.open_file(p, d, b))
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    def open_file(self, path, dept_name=None, button=None):
        try:
            subprocess.run(['start', '', path], shell=True)
            if dept_name:
                self.visited.add(dept_name)
            if button and dept_name and self.check_image:
                button.configure(
                    image=self.check_image,
                    compound="right",
                    fg_color="#406882"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Could not open:\n{path}\n\n{e}")

    def open_upload_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Upload Dashboard")
        popup.geometry("400x250")
        popup.grab_set()

        label = ctk.CTkLabel(popup, text="Select Department:")
        label.pack(pady=(20, 5))

        dept_var = tk.StringVar(value=list(DASHBOARDS.keys())[0])
        dept_dropdown = ctk.CTkOptionMenu(popup, variable=dept_var, values=list(DASHBOARDS.keys()))
        dept_dropdown.pack(pady=5)

        file_label = ctk.CTkLabel(popup, text="No file selected")
        file_label.pack(pady=5)

        def choose_file():
            file_path = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx")])
            if file_path:
                file_label.configure(text=file_path)

        browse_button = ctk.CTkButton(popup, text="Browse", command=choose_file)
        browse_button.pack(pady=5)

        def upload():
            src = file_label.cget("text")
            dept = dept_var.get()
            if not os.path.isfile(src):
                messagebox.showerror("Error", "Please select a valid file.")
                return
            dest = os.path.join(DASHBOARD_FOLDER, DASHBOARDS[dept])
            try:
                shutil.copy2(src, dest)
                messagebox.showinfo("Success", f"{dept} dashboard uploaded successfully.")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Upload failed: {e}")

        upload_button = ctk.CTkButton(popup, text="Upload", command=upload)
        upload_button.pack(pady=10)

def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.configure(bg="white")
    splash.geometry("400x250")

    x = (splash.winfo_screenwidth() - 400) // 2
    y = (splash.winfo_screenheight() - 250) // 2
    splash.geometry(f"+{x}+{y}")

    try:
        logo_image = Image.open(resource_path("img/logo.png"))
        logo_image = logo_image.resize((150, 150), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(splash, image=logo_photo, bg="white")
        logo_label.image = logo_photo
        logo_label.pack(pady=(30, 10))
    except:
        pass

    label = tk.Label(splash, text="Running first-time initialization…", font=("Segoe UI", 12), bg="white")
    label.pack()
    splash.update()
    return splash

if __name__ == "__main__":
    show_loading = not os.path.exists(LAUNCH_FLAG)
    splash = None

    if show_loading:
        splash_root = tk.Tk()
        splash_root.withdraw()
        splash = show_splash()
        splash_root.after(1000, splash_root.destroy)
        splash_root.mainloop()

    app = DashboardApp()
    if splash:
        app.after(100, lambda: splash.destroy())
        try:
            with open(LAUNCH_FLAG, 'w') as f:
                f.write("launched")
        except Exception as e:
            print(f"Failed to write launch flag: {e}")
    app.mainloop()
