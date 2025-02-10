# Configuración de Suricata en Ubuntu 

Distributor ID: Ubuntu
Description:    Ubuntu 24.04.1 LTS
Release:        24.04
Codename:       noble

 <img src="/img/suricatita.png" alt="ids2" width="600">

# Instalación de Suricata

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:oisf/suricata-stable
# press enter
sudo apt install suricata -y
sudo systemctl restart suricata
```
# Configuración de Suricata
para configurar Suricata, abre el archivo de configuración en el siguiente directorio:
```bash
sudo nano /etc/suricata/suricata.yaml
```
Con `ctrl+w`, buscamos `eth0` para configurar nuestra interface de red ya que esta es la que viene por defecto y la cambiaremos a la que tenemos.

Volvemos a usar `ctrl+w` y buscamos `HOME_NET` y cambiamos la IP de la red a la que estamos monitorizando.Podemos utilizar el comando `ip a` para obtener la IP de nuestra interfaz de red.

De nuevo, volvemos a usar `ctrl+w` y buscamos `/var/log/suricata/` y podemos cambiar el directorio donde se guardarán los logs de Suricata. En mi caso vamos a dejarlo en `/var/log/suricata/`.

Guardamos los cambios y actualizamos Suricata.
```bash
sudo suricata-update
```

# Configuración de Reglas Personalizadas
Las reglas se encuentran en el archivo `/usr/share/suricata/rules/`. Estas reglas podemos cargarlas  en Suricata para detectar tráfico específico.Por tanto vamos a crear nuestras propias reglas y luego cargarlas en Suricata. Importante utilizar la extensión `.rules` para que Suricata pueda leer las reglas.

```bash	
sudo nano /usr/share/suricata/rules/misreglas.rules
```
Aquí podemos agregar reglas personalizadas para detectar tráfico específico. Por ejemplo, 

```bash
alert icmp any any -> any any (msg:"[+] OJO Ping detectado"; itype:8; sid:1000001; rev:1;)
```

Para cargar la regla en suricata, ejecutamos el siguiente comando:
```bash
sudo nano /etc/suricata/suricata.yaml
```
`Ctrl+w` y buscamos `default-rule-path:` para cambiar la ruta donde se cargan las reglas y la regla que queremos cargar.

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

```bash		
alert tcp any any -> any 21 (msg:"[+] OJO TRAFICO FTP detectado"; sid:1000004; rev:1;)
```

Si queremos un area determinada de nuestro servidor web por ejemplo,
```bash			
cd /var/www/html
sudo mkdir admin
cd admin
echo "<html><h1>Bienvenido a la administración de nuestro servidor, estas visitando un directorio que no debes visitar, seras detectado por el IDS</h1></html>" | sudo tee /var/www/html/admin/index.html > /dev/null
```

```bash		
alert http any any -> any 80 (msg:"[+] OJO ACCESO A CONTENIDO PRIVADO "; content:"/admin"; http_uri; sid:1000005; rev:1;)
```

```bash
alert tls any any -> any any (msg:"[+] Acceso a sitio no autorizado"; tls.sni; content:"facebook"; sid:1000006; rev:1;)
```

```bash
alert tcp any any -> any any (msg:"[+] OJO TE ESTAN VIENDO LOS PUERTOS"; flags:S; threshold: type both, track by_src, count 20, seconds 3; sid:1000007; rev:1;)
```

```bash
alert tcp any any -> any 22 (msg:"[+] OJO Múltiples intentos de acceso SSH detectados"; flow:to_server, established; content:"Failed password"; sid:1000008; rev:1;)
```

# Comprobar Suricata
Simplemente basta con hacer ping ip_servidor, acceso a algun cotenido del servidor web , acceso por ssh, acceso por ftp, y ver si aparecen los logs de Suricata.

Para probar el acceso a un sitio no autorizado que el sysadmin quiere controlar, en la rule con el id 1000006, podemos probar con curl -k dominio-vetado.com si no tenemos entorno gráfico o directamente buscarlo en el navegador. Imaginemos que queremos controlar que nuestros usuarios no visiten redes sociales, podriamos crear otro fichero dominios-vetados.rules y agregariamos por ejemplo:

```bash
alert tls any any -> any any (msg:"[+] Acceso a Facebook detectado"; tls.sni; content:"facebook.com"; sid:2000001; rev:1;)
alert tls any any -> any any (msg:"[+] Acceso a Twitter detectado"; tls.sni; content:"twitter.com"; sid:2000002; rev:1;)
alert tls any any -> any any (msg:"[+] Acceso a TikTok detectado"; tls.sni; content:"tiktok.com"; sid:2000003; rev:1;)
```
y Actualizar Suricata para que use este archivo En `/etc/suricata/suricata.yaml`, busca la sección rule-files: y agrega la nueva regla:

```bash
default-rule-path: /usr/share/suricata/rules
rules-files:
  - misreglas.rules
  - dominios-prohibidos.rules
```
Para nmap podemos usar el siguiente comando:
```bash
sudo nmap -p- -sS -sCV -T4 -Pn -n -vvv ip_servidor
```

>[!NOTE]
>Desde el punto de vista de la ciberseguridad, Suricata es una herramienta que se utiliza para detectar posibles ataques,pero si usamos bien nmap podemos optimizarlo para saltarnos esta norma y no ser detectados. 

```bash
sudo nmap -sS -Pn -T1 --scan-delay 500ms --max-retries 1 --max-scan-delay 1000ms -f -p- ip_servidor
```

Aqui maximizamos el tiempo de escaneo y la cantidad de intentos de conexión y reducimos el ruido de nmap. Nos va a ir mas lento el escaneo, pero vamos a ser indetectables para Suricata.


Despues de añadir todas las reglas, recuerda que debes Guardamos los cambios y reiniciar Suricata.
```bash
sudo systemctl restart suricata
```
Puedes utilizar el fichero `misreglas.rules` y el fichero de configuración de suricata `ricata.yaml` que se encuentra en este repositorio para probar y securizar tu repositorio

# Script para automatizar el monitoreo

Para automatizar el monitoreo de Suricata, podemos crear un script que se ejecutará automáticamente en segundo plano con un servicio  en systemd. Este script se encargará de guardar los logs de Suricata en un directorio específico cada día y también de generar un informe de alertas para enviarlo por telegram.

- ventajas de python para automatizar el monitoreo de Suricata:

✅ Código más limpio: sin tantos comandos Bash.
✅ Menos dependencias: No necesita awk, cat, curl, ni eval.
✅ Manejo de errores mejorado: si el archivo no existe, Python no falla.
✅ Más seguro: evita posibles problemas con eval en Bash.

- **¿Systemd o Cron?**

---
| Método  | ¿Cuándo usarlo? | Ventajas | Desventajas |
|---------|----------------|----------|-------------|
| **systemd** | Para ejecutar el script constantemente en segundo plano | Se reinicia automáticamente si falla, inicia al encender el sistema | Configuración más técnica |
| **cron** | Para ejecutar el script cada cierto tiempo (ej. cada minuto) | Fácil de configurar | No es en tiempo real, no reinicia si falla |

---

📌 Explicación del flujo del script

📜 Script

Si hay una nueva alerta en fast.log, el script genera Alerta.txt y lo manda por Telegram.
Si no hay cambios en fast.log, el script simplemente sigue monitoreando en espera de nuevas alertas.

```python
import os
import requests
from datetime import datetime

# 📌 Configuración
LOG_FILE = "/var/log/suricata/fast.log"
MENSAJE_LOG = "/var/log/suricata/Alerta.txt"
BACKUP_DIR = "/var/log/suricata/copias_fast"

TELEGRAM_BOT_TOKEN = "Escribe-tu-token"
CHAT_ID = "Escribe-tu-chat-id"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

def obtener_ultimas_alertas():
    """Lee el contenido del log de Suricata"""
    try:
        with open(LOG_FILE, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def enviar_alerta(mensaje):
    """Envía el mensaje a Telegram"""
    with open(MENSAJE_LOG, "w") as f:
        f.writelines(mensaje)

    with open(MENSAJE_LOG, "rb") as file:
        requests.post(TELEGRAM_URL, data={"chat_id": CHAT_ID, "caption": "🚨 Nuevas alertas de Suricata"}, files={"document": file})

def hacer_backup():
    """Copia el log y lo limpia"""
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.system(f"cp {LOG_FILE} {BACKUP_DIR}/copia.{fecha_actual}")
    open(LOG_FILE, "w").close()  # Limpiar el log después del backup

def main():
    alertas = obtener_ultimas_alertas()
    if alertas:
        enviar_alerta(alertas)
        hacer_backup()
        print("✅ Alerta enviada y log respaldado.")
    else:
        print("🔍 No hay nuevas alertas.")

if __name__ == "__main__":
    main()
```