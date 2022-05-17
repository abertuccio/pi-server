FROM tiangolo/uwsgi-nginx-flask:python3.8

# Setting hora local y lang
# ENV TZ=America/Argentina/Buenos_Aires
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN echo 'LANG="en_US.UTF-8"' > /etc/default/locale

# RUN apt-get update && apt-get install -y rpi.gpio

# Requerimientos
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 44306

COPY ./pi-server /app