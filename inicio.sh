docker rm -f pi-server
docker build -t pi-server .
HASH_EMPAREJAMIENTO=$(echo -n $(date +"%T.%N") | sha256sum)
echo '{"_default": {"1": {"debe_sonar_alarma": true, "status_alarma": "INTENTO_ARMADO_FALLIDO"}}}' > /home/pi/pi-server/pi-server/db/status.json
echo '{"_default": {"1": {"usuario": "bertu","password": "otoño2011","token": false,"tiempo": null},"2": {"usuario": "rou","password": "otoño2011","token": false,"tiempo": null}}}' > /home/pi/pi-server/pi-server/db/usuarios.json
docker run --privileged -d -e HASH_EMPAREJAMIENTO=$(HASH_EMPAREJAMIENTO) --env-file conf/CONF.env -p 44306:44306 -v $(pwd)/pi-server:/app --name pi-server pi-server
docker logs -f pi-server
# ../telebit http 44306