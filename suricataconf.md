# Configuración de Suricata en Ubuntu 

Distributor ID: Ubuntu
Description:    Ubuntu 24.04.1 LTS
Release:        24.04
Codename:       noble

![ids2](/img/suricatita.png)

# Instalación de Suricata

```bash
sudo apt update
sudo add-apt-repository ppa:oisf/suricata-stable
# press enter
sudo apt install suricata -y
sudo systemctl restart suricata
```
# Configuración de Suricata
para configurar Suricata, abre el archivo de configuración en el siguiente directorio:
```bash
sudonano /etc/suricata/suricata.yaml
```
Con `ctrl+w`, buscamos `eht0` para configurar nuestra interface de red ya que esta es la que viene por defecto y la cambiaremos a la que tenemos.

Volvemos a usar `ctrl+w` y buscamos `HOME_NET` y cambiamos la IP de la red a la que estamos monitorizando.Podemos utilizar el comando `ip a` para obtener la IP de nuestra interfaz de red.

De nuevo, volvemos a usar `ctrl+w` y buscamos `/var/log/suricata/` y podemos cambiar el directorio donde se guardarán los logs de Suricata.En mi caso vamos a dejarlo en `/var/log/suricata/`.

Guardamos los cambios y actualizamos Suricata.
```bash
sudo suricata-update
```

# Configuración de Reglas Personalizadas
Las reglas se encuentran en el archivo `usr/share/suricata/rules/`. Estas reglas podemos cargarlas  en Suricata para detectar tráfico específico.Por tanto vamos a crear nuestras propias reglas y luego cargarlas en Suricata.Importante utilizar la extensión `.rules` para que Suricata pueda leer las reglas.

```bash	
sudo nano usr/share/suricata/rules/misreglas.rules
```
Aquí podemos agregar reglas personalizadas para detectar tráfico específico. Por ejemplo, 

```bash
alert icmp any any -> any any (msg:"[+] OJO Ping detectado"; itype:8; sid:1000001; rev:1;)
```

Para cargar la regla en suricata, ejecutamos el siguiente comando:
```bash
sudo nano /etc/suricata/suricata.yaml
```
`Ctrl+w` y buscamos `rules-files` para cambair la ruta donde se cargan las reglas y la regla que queremos cargar.

```bash
default-rule-path: /usr/share/suricata/rules
rules-files:
  - misreglas.rules
```
Guardamos los cambios y reiniciamos Suricata.
```bash
sudo systemctl restart suricata
```

# 🎯Logs
Para ver los logs de Suricata, puedes usar los los siguientes comandos:
```bash
sudo tail -f /var/log/suricata/fast.log #final del archivo
sudo cat /var/log/suricata/suricata.log
```

# :page_with_curl: Añadir nuevas reglas personalizadas
```bash	
alert tcp any any -> any 80 (msg:"[+] OJO TRAFICO HTTP detectado"; sid:1000002; rev:1;)
```
```bash		
alert tcp any any -> any 22 (msg:"[+] OJO TRAFICO SSH detectado"; sid:1000003; rev:1;)
```


