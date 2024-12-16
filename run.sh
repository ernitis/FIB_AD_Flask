usage=$'Incorrect usage. \nRun "./run.sh [s]" or "./run.sh [server]" to run the server with your current IP \nOR\nRun "./run.sh [c]" or "./run.sh [client]" to run a client instance.\nOR\nRun "./run.sh" to run both instances at the same time.'

init_app() {
    ip=$(ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}')
    pip3 install --upgrade flask watchdog
    pip3 install flask_sqlalchemy flask_migrate
}

init_client() {
    cd BaseApp

    flask db init
    flask db migrate
    flask db upgrade

    python3 run.py $ip
}

if [ $# -ge 2 ]
then 
    echo "$usage"
else
    ip=$(ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}')
    if [ $# -eq 1 ]
    then
        args=("$@")
        if test "${args[0]}" = "s" || test "${args[0]}" = "server" 
        then
            init_app
            cd AppREST
            python3 app.py $ip
        elif test "${args[0]}" = "c" || test "${args[0]}" = "client"
        then
            init_app
            init_client
        else
            echo "$usage"
        fi
    elif [ $# -eq 0 ]
    then
        init_app
        konsole -e bash -c "cd AppREST; python3 app.py $ip;"&
        init_client
    fi
fi