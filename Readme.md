# Instalar sistema en memoria sd para RPI

* Instalar "imager" en computadora escritorio si no está instalado `cd conf ; sudo apt install imager_1.7.2_amd64.deb` en computadora de escritorio
* Abrir el programa `tecla win + Imager` click en logo raspberry
* en OS elegir "Rasbery pi OS lite de 64 bits" sin entorno gráfico. NO TOCAR WRITE AHORA!!
* Elegir la memoria SD.  NO TOCAR WRITE AUN!!
* Tocar la rueda para configurar y configurar HOSTNAME, SSH, LAN etc.
* Recien ahora tocar en WRITE
* Expulsar la sd y ponerla en el RPI, enchufarlo.
* Si lo queremos configurar manualmente (o porque tocamos WRITE antes de tiempo):
    * Conectar a una televisión o algo con teclado
    * hacer `sudo raspi-config`
        * crear usuario y password ej: usuario: pi, password: raspberry
        * Habilitar ssh

# Acceder a red por ssh
* si seteamos el HOSTNAME, hacer `ping raspberrypi.local` o el hostname que hayamos puesto, sino:
    * `sudo chmod +x scanNetwork.sh`
    * Buscar rango de la red local `ip addr | grep wlp2s0 | grep inet`
    * Copiar el primer grupo de 3 números ej: `192.168.1` y pegarlo en scanNetwork
    * Se puede Ejecutar `./scanNetwork.sh` con el RPI apagado y luego de encenderlo y esperar 1 minuto, el que se agregue es el RPI
    * Alguna de las IPs devueltas en el comando de `./scanNetwork` es el RPI, hacer `ssh <el usuario que  configuramos>@192.168.1.<cambiar este numero>` Hasta que entremos.
 
# Docker y Tunnel ssh para conectarse desde afuera de la red sin port forwarding 
* instalamos Telebit en el RPI `curl https://get.telebit.io/ | bash`
* Seguimos las instrucciones para emparejar
    * si nos equivocamos de mail, hacer `nano /home/pi/.config/telebit/telebitd.yml`, cambiar el mail y tirar de nuevo el comando del principio
* Eso nos va a dar una dirección para acceder desde afuera de la red ej: "light-panda-16.telebit.io" "https://light-panda-16.telebit.io/"

* `sudo apt update`
* `sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release`
* `curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`
* `echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
* `sudo apt list update`
* `sudo apt update`
* `sudo apt-get install -y git docker-ce docker-ce-cli containerd.io docker-compose-plugin` 

# Instalar proyecto 

# Magnéticos

* se conectan en serie 

Si todo está cerrado el circuito está cerrado y no pasa nada
Si algo esta abierto, no cierra el circuito y suena alarma  

puerta ------ ventana ----- ventana-->
| 
 ------------------------------------>