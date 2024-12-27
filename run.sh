#!/bin/bash
usage=$'Incorrect usage.
Run "./run.sh s [rest_ip]" or "./run.sh server [rest_ip]" to run the server with your current IP
    -If client_ip is not specified, client_ip = interface_ip
OR
Run "./run.sh c [client_ip] [rest_ip]" or "./run.sh client [client_ip]" to run a client instance.
    -If client_ip is specified and rest_ip is not, rest_ip = client_ip
    -If client_ip is not specified, client_ip = rest_ip = interface_ip
OR
Run "./run.sh [client_ip] [rest_ip]" to run both instances at the same time.
    -If client_ip is specified and rest_ip is not, rest_ip = client_ip
    -If client_ip is not specified, client_ip = rest_ip = interface_ip
    '
int_ip=$(ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}')
rest_ip=$int_ip

init_client() {
    cd BaseApp

    flask db migrate
    flask db upgrade
}

if [ $# -ge 4 ]
then 
    echo "$usage"
else
    if [ $# -eq 0 ]
    then
        konsole -e bash -c "cd AppREST; python3 app.py $int_ip;"&
        init_client
        python3 run.py $int_ip
    elif [ $# -eq 1 ]
    then
        args=("$@")
        if test "${args[0]}" = "s" || test "${args[0]}" = "server" 
        then
            cd AppREST
            python3 app.py $int_ip
        elif test "${args[0]}" = "c" || test "${args[0]}" = "client"
        then
            init_client
            python3 run.py $int_ip
        else
            echo "$usage"
        fi
    elif [ $# -eq 2 ]
    then
        args=("$@")
        if test "${args[0]}" = "s" || test "${args[0]}" = "server" 
        then
            ip=${args[1]}
            cd AppREST
            python3 app.py $ip
        elif test "${args[0]}" = "c" || test "${args[0]}" = "client"
        then
            ip=${args[1]}
            init_client
            python3 run.py $ip
        else
            ip=${args[0]}
            rest_ip=${args[1]}
            konsole -e bash -c "cd AppREST; python3 app.py $rest_ip;"&
            init_client
            python3 run.py $ip $rest_ip
        fi
    elif [ $# -eq 3 ]
    then
        args=("$@")
        if test "${args[0]}" = "s" || test "${args[0]}" = "server" 
        then
            echo "$usage"
        elif test "${args[0]}" = "c" || test "${args[0]}" = "client"
        then
            ip=${args[1]}
            rest_ip=${args[2]}
            init_client
            python3 run.py $ip $rest_ip
        else
            echo "$usage"
        fi
    fi
fi