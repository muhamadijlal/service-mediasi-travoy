# running service
```
DB_SRC="db_source" DB_DST="db_dst" python main.py
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
