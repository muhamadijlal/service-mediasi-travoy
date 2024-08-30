# running service (local)
DB_SRC can input multiple value
```
IP_SRC="your_ip_source" PORT_SRC="your_port_source" USER_SRC="your_username_source" PASS_SRC="your_pass_src" DB_SRC="db_source_1,db_source_2,db_source_3" IP_DST="your_ip_destination" PORT_DST="your_port_destination" USER_DST="your_username_destination" PASS_DST="your_pass_destination" DB_DST="db_dst" python main.py
```

# running service (docker)
```
docker run --restart=always -v /etc/localtime:/etc/localtime --name your_service_name -e DB_SRC="db_source" -e IP_SRC="your_ip_source" -e PORT_SRC="your_port_source" -e USER_SRC="your_username_source" -e PASS_SRC="your_pass_src" -e DB_SRC="db_source_1,db_source_2,db_source_3" -e IP_DST="your_ip_destination" -e PORT_DST="your_port_destination" -e USER_DST="your_username_destination" -e PASS_DST="your_pass_destination" -e DB_DST="db_dst" -dit username_docker/images:tag
```
