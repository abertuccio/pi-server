docker rm -f pi-server
docker build -t pi-server .
HASH_EMPAREJAMIENTO=$(echo -n $(date +"%T.%N") | sha256sum)
docker run --privileged -d -e HASH_EMPAREJAMIENTO=$(HASH_EMPAREJAMIENTO) --env-file conf/CONF.env -p 44306:44306 -v $(pwd)/pi-server:/app --name pi-server pi-server
docker logs -f pi-server
# ../telebit http 44306