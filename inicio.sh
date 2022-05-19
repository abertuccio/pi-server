docker rm -f pi-server
docker build -t pi-server .
docker run --privileged -d --env-file conf/CONF.env -p 44306:44306 -v $(pwd)/pi-server:/app --name pi-server pi-server
docker logs -f pi-server
# ../telebit http 44306