# Docker Setup Script Generator

A Flask-based web application that generates a Bash script to install Docker Engine on Ubuntu and pull multiple container images specified by the user.

---

## Prerequisites

- Python 3.7 or higher  
- Flask library  
- An Ubuntu-based system (or compatible) for running the generated script  
- Git (for cloning the repository)

---

## Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/ananth-2022/auto-script-generation-for-servers.git
   cd auto-script-generation-for-servers
   ```

2. (Optional) Create and activate a virtual environment (use ```python3``` on mac/linux  
   ```bash
   python -m venv venv
   ```
3. Activate venv (make sure to deactivate when you are done)
   ```bash
   # on mac/linux
   source venv/bin/activate
   # on windows cmd
   venv\Scripts\activate.bat
   # on windows powershell
   .\venv\Scripts\Activate.ps1
   # to deactivate on mac/linux/powershell
   deactivate
   # to deactivate on cmd
   venv\Scripts\deactivate.bat
   ``` 

4. Install Python dependencies  
   ```bash
   pip install Flask
   ```

---

## Usage

1. Start the Flask application  
   ```bash
   python app.py
   ```
2. Open your browser and navigate to  
   ```
   http://127.0.0:5000
   ```
3. Add the containers you want to the list
4. Click **Download script** to retrieve the generated Bash script.  
5. Transfer `setup.sh` to your Ubuntu server, make it executable, and run it:  
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

---

## Project Structure

- **app.py**  
  Flask application handling user input and script generation.

- **templates/index.html**  
  Frontend form for listing desired Docker images.

- **setup.sh** (generated)  
  Bash script that installs Docker Engine and pulls the specified images.

---
