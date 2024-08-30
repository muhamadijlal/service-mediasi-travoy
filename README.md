# running service (local)
DB_SRC can input multiple value

```
DB_SRC="db_source_1,db_source_2,db_source_3" DB_DST="db_dst" python main.py
```

# running service (docker)
```
docker run --restart=always -v /etc/localtime:/etc/localtime --name your_service_name -e DB_SRC="db_source_1,db_source_2,db_source_3" -e DB_DST="db_dst" -dit username_docker/images:tag
```
