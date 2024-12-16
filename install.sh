pip3 install --upgrade flask watchdog
pip3 install flask_sqlalchemy flask_migrate

ip=$(ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}')

git clone https://github.com/CarlesBalsach/FIB_AD_Flask.git

cd FIB_AD_Flask/

konsole -e bash -c "cd AppREST; ls; python3 app.py $ip;"&

cd BaseApp

flask db init
flask db migrate
flask db upgrade

python3 run.py $ip