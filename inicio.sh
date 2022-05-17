docker rm -f pi-server
docker build -t pi-server .
docker run -d --env-file conf/CONF.env -p 44306:44306 --name pi-server pi-server
docker logs -f pi-server