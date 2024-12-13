
# FIB_AD_Flask

A simple Flask app to showcase Flask usability for students in the AD course.

## Step-by-Step Installation

### Step 1: Install Required Packages
```bash
pip3 install --upgrade flask watchdog
pip3 install flask_sqlalchemy flask_migrate
```

### Step 2: Clone the Repository
```bash
git clone https://github.com/CarlesBalsach/FIB_AD_Flask.git
```

### Step 3: Navigate to the Base App Directory
```bash
cd FIB_AD_Flask/BaseApp
```

### Step 4: Initialize the Database
```bash
flask db init
flask db migrate
flask db upgrade
```

### Step 5: Run Both Applications in Separate Terminals

#### Terminal 1: Run the Base App
```bash
python3 run.py
```

#### Terminal 2: Run the AppREST
```bash
cd AppREST
python3 app.py
```

#### Optional: VSCode Extensions
Recommended Extensions to facilitate Development
**Python Extensions (Editor & Debug):**
- Python by Microsoft
- Python Debugger by Microsoft
- Pylance by Microsoft

**SQL Lite Extension (View and Edit)**
- SQLite3 Editor by yy0931
