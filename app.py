import sys
import os
import shutil
import subprocess
import textwrap
import platform
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QFileDialog, QCheckBox,
    QMessageBox, QScrollArea, QGroupBox, QFrame, QMenuBar, QAction,
    QTextBrowser
)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QUrl

TEMPLATES = {
    "Python Script": "python_script",
    "Flask Web App (Flask + SQLAlchemy)": "flask_sqlalchemy",
    "FastAPI Web App": "fastapi",
    "Django Web App": "django",
    "Data Science Project (Jupyter)": "datascience",
    "Machine Learning (scikit-learn)": "ml_sklearn",
    "Tkinter Desktop App": "tkinter",
    "PyQt5 Desktop App": "pyqt5",
    "Kivy Mobile App": "kivy",
    "Pygame Project": "pygame",
    "CLI Tool (Click)": "cli_click",
}

EXTRA_FILES = ["README.md", "LICENSE", ".gitignore", "pyproject.toml", "Dockerfile", "setup.py", "Makefile"]
ADDITIONAL_LIBS = [
    "numpy", "pandas", "scipy", "scikit-learn", "matplotlib", "seaborn",
    "plotly", "polars", "requests", "beautifulsoup4", "sqlalchemy",
    "pillow", "pytest", "black", "flake8", "click", "uvicorn",
    "fastapi", "jupyter", "ipython", "PyYAML", "h5py",
    "statsmodels", "lightgbm", "xgboost", "bokeh", "altair", "plotnine",
    "geoplotlib", "river", "gensim", "nltk", "spacy", "langchain",
    "hydra", "dask", "duckdb", "cuPy", "scrapy", "paramiko", "lxml",
    "httpx", "typer", "sphinx", "ruff", "glom", "rich", "textual",
    "networkx", "python-igraph", "graph-tool", "pygame", "opencv",
    "manim", "scikit-image", "bokeh"
]


class AboutDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de Python Port-Scaffolder")
        self.setTextFormat(Qt.RichText)
        self.setIcon(QMessageBox.Information)
        
        about_html = """
       <h1>Python Port-Scaffolder</h1>
<hr>
<p><b>Python Port-Scaffolder</b> es una herramienta para generar proyectos Python con estructuras profesionales preconfiguradas. Soporta múltiples tipos de proyectos como scripts, apps web (Flask, Django, FastAPI), aplicaciones de escritorio (Tkinter, PyQt5), ciencia de datos, machine learning, entre otros.</p>

<p>Este software está disponible de forma <b>gratuita</b> bajo los nombres de <b>Luigi Adducci</b>. No se permite su modificación ni redistribución alterada. Su distribución oficial y autorizada es solamente bajo su versión original y gratuita.</p>

<p>Para consultas o contacto, escribir a: <i>luigiadduccidev@gmail.com</i></p>
<hr>
<p>Este proyecto es de código abierto y está disponible en <a href="https://github.com/LuigiValentino/Python-Port-Scaffolder">GitHub</a>.</p>
<p><b>¡Gracias por usar esta herramienta!</b> Tu apoyo hace posible el desarrollo de soluciones libres para programadores.</p>

<hr>
<p>Python {py_version} | Qt {qt_version} | {os_info}</p>
<p>©2025 Python Port-Scaffolder | Luigi Adducci</p>

        """.format(
            py_version=platform.python_version(),
            qt_version=QApplication.instance().applicationVersion(),
            os_info=f"{platform.system()} {platform.release()}"
        )
        self.setText(about_html)
        self.setStandardButtons(QMessageBox.Ok)


class Scaffolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Port-Scaffolder")
        self.setMinimumSize(850, 700)
        self.setWindowIcon(QIcon("icon.ico"))
        self._init_ui()
        self.apply_light_theme()


    def apply_light_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(150, 150, 150))
        QApplication.setPalette(palette)
        QApplication.setStyle("Fusion")

    def _init_ui(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        menubar = QMenuBar()
        help_menu = menubar.addMenu("Ayuda")
        
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        
        self.setMenuBar(menubar)

        config_group = QGroupBox("Configuración del Proyecto")
        config_layout = QVBoxLayout()
        config_layout.setSpacing(10)
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Tipo de proyecto:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(TEMPLATES.keys())
        self.type_combo.setMinimumHeight(30)
        type_layout.addWidget(self.type_combo, 1)
        config_layout.addLayout(type_layout)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nombre del proyecto:"))
        self.name_edit = QLineEdit()
        self.name_edit.setMinimumHeight(30)
        self.name_edit.setPlaceholderText("my_project")
        name_layout.addWidget(self.name_edit, 1)
        config_layout.addLayout(name_layout)

        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Carpeta destino:"))
        self.dest_edit = QLineEdit()
        self.dest_edit.setMinimumHeight(30)
        self.dest_edit.setPlaceholderText("Selecciona una carpeta...")
        dest_btn = QPushButton("...")
        dest_btn.setFixedSize(40, 30)
        dest_btn.clicked.connect(self.browse_dest)
        dest_layout.addWidget(self.dest_edit, 1)
        dest_layout.addWidget(dest_btn)
        config_layout.addLayout(dest_layout)

        env_layout = QHBoxLayout()
        self.venv_chk = QCheckBox("Crear entorno virtual (venv)")
        self.venv_chk.setChecked(True)
        env_layout.addWidget(self.venv_chk)
        self.req_chk = QCheckBox("Crear requirements.txt")
        self.req_chk.setChecked(True)
        env_layout.addWidget(self.req_chk)
        self.git_chk = QCheckBox("Inicializar repositorio Git")
        self.git_chk.setChecked(True)
        env_layout.addWidget(self.git_chk)
        config_layout.addLayout(env_layout)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        bottom_layout = QHBoxLayout()
        files_group = QGroupBox("Archivos Extras")
        files_layout = QVBoxLayout()
        files_layout.setSpacing(5)
        
        self.file_checks = []
        for fname in EXTRA_FILES:
            chk = QCheckBox(fname)
            chk.setChecked(True)
            files_layout.addWidget(chk)
            self.file_checks.append(chk)
            
        files_group.setLayout(files_layout)
        bottom_layout.addWidget(files_group, 1)

        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        bottom_layout.addWidget(separator)

        libs_group = QGroupBox("Librerías Adicionales")
        libs_layout = QVBoxLayout()
        libs_layout.setSpacing(5)
        
        self.lib_checks = []
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(5)
        
        col_layout = QHBoxLayout()
        left_col = QVBoxLayout()
        right_col = QVBoxLayout()
        
        half = len(ADDITIONAL_LIBS) // 2
        for i, lib in enumerate(ADDITIONAL_LIBS):
            chk = QCheckBox(lib)
            chk.setChecked(False)
            self.lib_checks.append(chk)
            if i < half:
                left_col.addWidget(chk)
            else:
                right_col.addWidget(chk)
                
        col_layout.addLayout(left_col)
        col_layout.addLayout(right_col)
        scroll_layout.addLayout(col_layout)
        
        scroll.setWidget(scroll_widget)
        libs_layout.addWidget(scroll)
        libs_group.setLayout(libs_layout)
        bottom_layout.addWidget(libs_group, 2)
        
        layout.addLayout(bottom_layout, 1)

        gen_btn = QPushButton("Generar Proyecto")
        gen_btn.setMinimumHeight(40)
        gen_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1e6ec8;
            }
            QPushButton:pressed {
                background-color: #1a5ca0;
            }
        """)
        gen_btn.clicked.connect(self.generate_project)
        layout.addWidget(gen_btn)

        self.setCentralWidget(central)

    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()


    def browse_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder:
            self.dest_edit.setText(folder)

    def create_project_structure(self, target_path, project_type):
        """Crea la estructura del proyecto dinámicamente sin usar plantillas físicas"""
        os.makedirs(target_path, exist_ok=True)
        
        os.makedirs(os.path.join(target_path, "src"), exist_ok=True)
        os.makedirs(os.path.join(target_path, "tests"), exist_ok=True)
        os.makedirs(os.path.join(target_path, "docs"), exist_ok=True)
        
        if project_type == "Python Script":
            with open(os.path.join(target_path, "src", "main.py"), "w") as f:
                f.write('#!/usr/bin/env python3\nprint("Hello, World!")\n')
                
        elif project_type == "Flask Web App (Flask + SQLAlchemy)":
            os.makedirs(os.path.join(target_path, "src", "templates"), exist_ok=True)
            os.makedirs(os.path.join(target_path, "src", "static", "css"), exist_ok=True)
            os.makedirs(os.path.join(target_path, "src", "static", "js"), exist_ok=True)
            os.makedirs(os.path.join(target_path, "src", "models"), exist_ok=True)
            
            with open(os.path.join(target_path, "src", "app.py"), "w") as f:
                f.write(textwrap.dedent('''\
                from flask import Flask, render_template
                from flask_sqlalchemy import SQLAlchemy
                
                app = Flask(__name__)
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
                db = SQLAlchemy(app)
                
                class User(db.Model):
                    id = db.Column(db.Integer, primary_key=True)
                    username = db.Column(db.String(80), unique=True, nullable=False)
                    email = db.Column(db.String(120), unique=True, nullable=False)
                
                @app.route('/')
                def home():
                    return render_template('index.html')
                
                if __name__ == '__main__':
                    app.run(debug=True)
                '''))
            
            with open(os.path.join(target_path, "src", "templates", "index.html"), "w") as f:
                f.write(textwrap.dedent('''\
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Flask App</title>
                    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
                </head>
                <body>
                    <h1>Welcome to your Flask App!</h1>
                    <p>This is a generated Flask application with SQLAlchemy support.</p>
                </body>
                </html>
                '''))
                
            with open(os.path.join(target_path, "src", "static", "css", "style.css"), "w") as f:
                f.write("/* Add your CSS styles here */")
                
        elif project_type == "FastAPI Web App":
            with open(os.path.join(target_path, "src", "main.py"), "w") as f:
                f.write(textwrap.dedent('''\
                from fastapi import FastAPI
                
                app = FastAPI()
                
                @app.get("/")
                async def root():
                    return {"message": "Hello World"}
                
                @app.get("/items/{item_id}")
                async def read_item(item_id: int):
                    return {"item_id": item_id}
                '''))
                
        elif project_type == "Django Web App":
            python_cmd = sys.executable
            subprocess.run([python_cmd, "-m", "django", "startproject", os.path.basename(target_path), target_path])
            
        elif project_type == "PyQt5 Desktop App":
            with open(os.path.join(target_path, "src", "main.py"), "w") as f:
                f.write(textwrap.dedent('''\
                import sys
                from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
                
                class MainWindow(QMainWindow):
                    def __init__(self):
                        super().__init__()
                        self.setWindowTitle("PyQt5 App")
                        self.setGeometry(100, 100, 400, 300)
                        
                        self.label = QLabel("Hello, PyQt5!", self)
                        self.label.move(150, 100)
                        
                        self.button = QPushButton("Click Me", self)
                        self.button.move(150, 150)
                        self.button.clicked.connect(self.on_button_click)
                
                    def on_button_click(self):
                        self.label.setText("Button Clicked!")
                
                if __name__ == "__main__":
                    app = QApplication(sys.argv)
                    window = MainWindow()
                    window.show()
                    sys.exit(app.exec_())
                '''))
                
        elif project_type == "Data Science Project (Jupyter)":
            with open(os.path.join(target_path, "src", "analysis.ipynb"), "w") as f:
                f.write('{"cells": [{"cell_type": "code","execution_count": null,"metadata": {},"outputs": [],"source": ["# Your data analysis code here"]}],"metadata": {"kernelspec": {"display_name": "Python 3","language": "python","name": "python3"},"language_info": {"codemirror_mode": {"name": "ipython","version": 3},"file_extension": ".py","mimetype": "text/x-python","name": "python","nbconvert_exporter": "python","pygments_lexer": "ipython3","version": "3.8.5"}},"nbformat": 4,"nbformat_minor": 4}')
            with open(os.path.join(target_path, "src", "utils.py"), "w") as f:
                f.write("# Utility functions for data processing\n")
            with open(os.path.join(target_path, "src", "data_loader.py"), "w") as f:
                f.write("# Functions for loading and preprocessing data\n")
                
        elif project_type == "Machine Learning (scikit-learn)":
            with open(os.path.join(target_path, "src", "train.py"), "w") as f:
                f.write(textwrap.dedent('''\
                from sklearn.datasets import load_iris
                from sklearn.model_selection import train_test_split
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.metrics import accuracy_score
                import joblib
                
                # Load data
                data = load_iris()
                X, y = data.data, data.target
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # Train model
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                
                # Evaluate
                predictions = model.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)
                print(f"Model Accuracy: {accuracy:.2f}")
                
                # Save model
                joblib.dump(model, 'model.pkl')
                '''))
                
        elif project_type == "Tkinter Desktop App":
            with open(os.path.join(target_path, "src", "main.py"), "w") as f:
                f.write(textwrap.dedent('''\
                import tkinter as tk
                from tkinter import messagebox
                
                class App(tk.Tk):
                    def __init__(self):
                        super().__init__()
                        self.title("Tkinter App")
                        self.geometry("300x200")
                        
                        self.label = tk.Label(self, text="Hello, Tkinter!")
                        self.label.pack(pady=20)
                        
                        self.button = tk.Button(self, text="Click Me", command=self.on_button_click)
                        self.button.pack()
                
                    def on_button_click(self):
                        messagebox.showinfo("Info", "Button clicked!")
                
                if __name__ == "__main__":
                    app = App()
                    app.mainloop()
                '''))
                
        elif project_type == "Kivy Mobile App":
            with open(os.path.join(target_path, "src", "main.py"), "w") as f:
                f.write(textwrap.dedent('''\
                from kivy.app import App
                from kivy.uix.button import Button
                from kivy.uix.boxlayout import BoxLayout
                
                class MyApp(App):
                    def build(self):
                        layout = BoxLayout(orientation='vertical')
                        btn = Button(text='Hello Kivy', size_hint=(0.5, 0.5),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5})
                        layout.add_widget(btn)
                        return layout
                
                if __name__ == '__main__':
                    MyApp().run()
                '''))
                
        elif project_type == "Pygame Project":
            with open(os.path.join(target_path, "src", "main.py"), "w") as f:
                f.write(textwrap.dedent('''\
                import pygame
                import sys
                
                # Initialize pygame
                pygame.init()
                
                # Screen dimensions
                WIDTH, HEIGHT = 800, 600
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Pygame Project")
                
                # Colors
                WHITE = (255, 255, 255)
                RED = (255, 0, 0)
                
                # Game loop
                clock = pygame.time.Clock()
                running = True
                
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    
                    # Fill the screen with white
                    screen.fill(WHITE)
                    
                    # Draw a red circle
                    pygame.draw.circle(screen, RED, (WIDTH//2, HEIGHT//2), 50)
                    
                    # Update the display
                    pygame.display.flip()
                    
                    # Cap the frame rate
                    clock.tick(60)
                
                pygame.quit()
                sys.exit()
                '''))
                
        elif project_type == "CLI Tool (Click)":
            with open(os.path.join(target_path, "src", "cli.py"), "w") as f:
                f.write(textwrap.dedent('''\
                import click
                
                @click.group()
                def cli():
                    """Command Line Interface Tool"""
                    pass
                
                @cli.command()
                @click.argument('name')
                def hello(name):
                    """Print a greeting"""
                    click.echo(f"Hello, {name}!")
                
                if __name__ == '__main__':
                    cli()
                '''))
                
        elif project_type == "Minimal CLI Tool (Typer)":
            with open(os.path.join(target_path, "src", "cli.py"), "w") as f:
                f.write(textwrap.dedent('''\
                import typer
                
                app = typer.Typer()
                
                @app.command()
                def hello(name: str):
                    typer.echo(f"Hello, {name}")
                
                if __name__ == "__main__":
                    app()
                '''))
                
        else:
            with open(os.path.join(target_path, "src", "main.py"), "w") as f:
                f.write(f"# {project_type} Project\n\nprint('Hello, World!')")
                
        readme_content = f"# {os.path.basename(target_path)}\n\n" + \
                         "## Project Description\n\n" + \
                         f"This is a {project_type} project generated with Python Port-Scaffolder.\n\n" + \
                         "## Getting Started\n\n" + \
                         "### Prerequisites\n\n" + \
                         "- Python 3.8+\n\n" + \
                         "### Installation\n\n" + \
                         "```bash\npip install -r requirements.txt\n```\n\n" + \
                         "### Usage\n\n" + \
                         "```bash\npython src/main.py\n```\n"
                         
        with open(os.path.join(target_path, "README.md"), "w") as f:
            f.write(readme_content)
            
        gitignore_content = textwrap.dedent('''\
        # Byte-compiled / optimized / DLL files
        __pycache__/
        *.py[cod]
        
        # Virtual environment
        venv/
        
        # IDE files
        .vscode/
        .idea/
        
        # Logs and databases
        *.log
        *.sqlite3
        
        # OS generated files
        .DS_Store
        Thumbs.db
        
        # Build artifacts
        build/
        dist/
        *.egg-info/
        ''')
        
        with open(os.path.join(target_path, ".gitignore"), "w") as f:
            f.write(gitignore_content)

    def generate_project(self):
        project_type = self.type_combo.currentText()
        name = self.name_edit.text().strip()
        dest = self.dest_edit.text().strip()
        create_venv = self.venv_chk.isChecked()
        create_req = self.req_chk.isChecked()
        init_git = self.git_chk.isChecked()

        if not name:
            QMessageBox.warning(self, "Error", "Debes ingresar un nombre para el proyecto.")
            return
            
        if not dest:
            QMessageBox.warning(self, "Error", "Debes seleccionar una carpeta destino.")
            return

        target_path = os.path.join(dest, name)
        
        if os.path.exists(target_path):
            reply = QMessageBox.question(
                self, "Carpeta Existente", 
                f"La carpeta '{name}' ya existe. ¿Deseas sobrescribirla?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
            shutil.rmtree(target_path)

        try:
            self.create_project_structure(target_path, project_type)
            
            python_cmd = sys.executable
            if create_venv:
                venv_path = os.path.join(target_path, "venv")
                subprocess.run([python_cmd, "-m", "venv", venv_path], check=True)
                
                if os.name == 'nt':
                    python_cmd = os.path.join(venv_path, "Scripts", "python.exe")
                else:
                    python_cmd = os.path.join(venv_path, "bin", "python")
            
            libs = [chk.text() for chk in self.lib_checks if chk.isChecked()]
            if create_req:
                req_path = os.path.join(target_path, "requirements.txt")
                with open(req_path, "w") as req_file:
                    if project_type == "Flask Web App (Flask + SQLAlchemy)":
                        req_file.write("flask\nflask_sqlalchemy\n")
                    elif project_type == "FastAPI Web App":
                        req_file.write("fastapi\nuvicorn\n")
                    elif project_type == "Django Web App":
                        req_file.write("django\n")
                    elif project_type == "Data Science Project (Jupyter)":
                        req_file.write("jupyter\npandas\nnumpy\nmatplotlib\n")
                    elif project_type == "Machine Learning (scikit-learn)":
                        req_file.write("scikit-learn\npandas\nnumpy\nmatplotlib\n")
                    elif project_type == "PyQt5 Desktop App":
                        req_file.write("pyqt5\n")
                    elif project_type == "Kivy Mobile App":
                        req_file.write("kivy\n")
                    elif project_type == "Pygame Project":
                        req_file.write("pygame\n")
                    elif project_type == "CLI Tool (Click)":
                        req_file.write("click\n")
                    elif project_type == "Minimal CLI Tool (Typer)":
                        req_file.write("typer\n")
                    
                    for lib in libs:
                        req_file.write(f"{lib}\n")
            
            for chk in self.file_checks:
                if chk.isChecked():
                    fname = chk.text()
                    fpath = os.path.join(target_path, fname)
                    
                    if not os.path.exists(fpath):
                        if fname == "LICENSE":
                            with open(fpath, "w") as f:
                                f.write("MIT License\n\nCopyright (c) [year] [fullname]\n")
                        elif fname == "pyproject.toml":
                            with open(fpath, "w") as f:
                                f.write("[build-system]\nrequires = [\"setuptools\"]\nbuild-backend = \"setuptools.build_meta\"\n")
                        elif fname == "setup.py":
                            with open(fpath, "w") as f:
                                f.write(textwrap.dedent('''\
                                from setuptools import setup, find_packages
                                
                                setup(
                                    name='{}',
                                    version='0.1.0',
                                    packages=find_packages(),
                                    install_requires=[],
                                )
                                '''.format(name)))
                        elif fname == "Dockerfile":
                            with open(fpath, "w") as f:
                                f.write(textwrap.dedent('''\
                                FROM python:3.9-slim
                                
                                WORKDIR /app
                                
                                COPY requirements.txt .
                                RUN pip install --no-cache-dir -r requirements.txt
                                
                                COPY . .
                                
                                CMD ["python", "src/main.py"]
                                '''))
                        elif fname == "Makefile":
                            with open(fpath, "w") as f:
                                f.write(textwrap.dedent('''\
                                .PHONY: run test clean
                                
                                run:
                                \tpython src/main.py
                                
                                test:
                                \tpytest tests/
                                
                                clean:
                                \trm -rf __pycache__ .pytest_cache
                                '''))
                        else:
                            open(fpath, 'a').close()
            
            if init_git:
                try:
                    subprocess.run(["git", "init", target_path], check=True)
                except Exception:
                    QMessageBox.warning(self, "Advertencia", "Git no está instalado. No se pudo inicializar el repositorio.")
            
            if create_req and create_venv:
                try:
                    subprocess.run([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  cwd=target_path, check=True)
                except Exception as e:
                    QMessageBox.warning(self, "Advertencia", 
                                      f"No se pudieron instalar las dependencias: {str(e)}")
            
            QMessageBox.information(
                self, 
                "Proyecto Generado", 
                f"Proyecto '{name}' ({project_type}) generado exitosamente en:\n{target_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"No se pudo generar el proyecto: {str(e)}\n\nDetalles: {type(e).__name__}"
            )
            if os.path.exists(target_path):
                shutil.rmtree(target_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")
    
    win = Scaffolder()
    win.show()
    sys.exit(app.exec_())