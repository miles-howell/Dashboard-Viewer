
# 🗂️ Department Dashboard Viewer (Demo)

A desktop launcher for department-specific dashboards, built with Python and CustomTkinter.

This GUI application allows users to quickly view or update PowerPoint files for different departments in an organization. It includes a splash screen on first launch, intuitive upload flow, and clean modern styling suitable for internal business tools.

---

## 🚀 Features

- 🖥️ **Desktop App UI** with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- 📊 **Departmental Dashboard Launcher** for `.pptx` files
- 🆕 **Upload Panel** for updating dashboards
- 💡 **First-Launch Splash Screen**
- 🔒 Local-only demo using generic folders and sample content
- 🌐 Functions well with network locations like a shared file server (change the dashboards directory)
- 📦  Can be easily packaged into a deployable .exe for cross-network usage (PyInstaller)

---

## 📁 Folder Structure

```
├── dashboards/         # Demo PowerPoint files (placeholder)
├── img/                # App icon, logo, and checkmark
├── main.py             # Launchable application
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Requirements

- Python 3.8+
- Packages in `requirements.txt` (install with `pip install -r requirements.txt`)

---

## 📷 Screenshots

![image](https://github.com/user-attachments/assets/dec2e8c4-a655-4dda-84b3-5f0b4a0795df)
![image](https://github.com/user-attachments/assets/2df60582-d18b-469c-aa99-0960f243fde0)


---

## 🧪 How to Use

```bash
# Clone the repository
git clone https://github.com/yourusername/department-dashboard-viewer.git
cd department-dashboard-viewer

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py

```

---

## 📦 Packaging

Use PyInstaller to build an executable:
```bash
pyinstaller main.py --windowed --icon=img/favicon.ico --add-data "img;img" --add-data "dashboards;dashboards"
```

---

## 🧠 About This Demo

This version is safe for public distribution. All department names and file paths are generic and use local resources only.

Contact miles@plannedpixel.com for Commercial usage.

For questions or collaboration opportunities, feel free to reach out!

---

📁 **Demo created by Miles Howell**
