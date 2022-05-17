docker rm -f pi-server
docker build -t pi-server .
docker run --privileged -d --env-file conf/CONF.env -p 80:80 --name pi-server pi-server
docker logs -f pi-server