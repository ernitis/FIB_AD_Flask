# FIB_AD_Flask
A Flask Simple App to showcase Flask usability for students in the AD course

# Step by Step Install

Clone the Repository
git clone https://github.com/CarlesBalsach/FIB_AD_Flask.git

# Install missing packages
pip install --upgrade flask
pip install flask_sqlalchemy
pip install flask_sqlalchemy
pip install --upgrade watchdog

# Initialize DB
flask db init
flask db migrate
flask db upgrade

# Run Both Apps in different terminals
# Base App
cd BaseApp
python3 run.py

# AppREST
cd AppREST
python3 app.py