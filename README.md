# running service (local)
DB_SRC can input multiple value
```
DB_SRC="db_source_1,db_source_2,db_source_3" DB_DST="db_dst" python main.py
```

# running service (docker)
```
docker run --restart=always -v /etc/localtime:/etc/localtime --name your_service_name -e DB_SRC="db_source" -e DB_DST="db_dst" -dit username_docker/images:tag
```

path config : database/config.py </br>
rename file config.example to config.py </br>
</br>
</br>
</br>
fill in according to the database connection </br>

leave the database field blank
```
def loadConf():
    return {
        "host": "host",
        "port": "port",
        "user": "user",
        "password": "password",
        "database": "",
    }
```
