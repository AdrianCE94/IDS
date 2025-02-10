# Configuración de Snort en Ubuntu
![ids](/img/ids.png)

> [!TIP]
>Las reglas personalizadas para snort se encuentran en el archivo `local.rules` de este repositorio.Puedes usar el archivo para probar las reglas antes de añadirlas a la configuración.


## Instalación de Snort


```bash
sudo apt update
```
```bash
sudo apt install snort -y
```
> [!WARNING]
> Durante la instalación, te pedirá configurar la IP de la máquina. Puedes ingresar la IP privada de la instancia o el rango de red en el que estará monitoreando tráfico.

Si no lo introduces en este paso, puedes editarlo más tarde en la configuración

```bash
sudo nano /etc/snort/snort.conf

# Configura tu red
ipvar HOME_NET [192.168.1.0/24]  # Ajusta a tu rango de red
ipvar EXTERNAL_NET !$HOME_NET
```

## Configuración de Reglas
Edita el archivo de reglas locales de Snort:

```bash
sudo nano /etc/snort/rules/local.rules
```
Aquí puedes agregar reglas personalizadas para detectar tráfico específico. Por ejemplo, 

```bash
# FTP
alert tcp any any -> any 21 (msg:"Intento de acceso FTP detectado"; sid:1000001; rev:1;)

# ICMP
alert icmp any any -> any any (msg:"ICMP Ping detectado"; itype:8; sid:1000002; rev:1;)

# SSH
alert tcp any any -> any 22 (msg:"Intento de acceso SSH detectado"; flags:S; sid:1000003; rev:1;)

# HTTP (Apache)
alert tcp any any -> $HOME_NET 80 (msg:"Acceso HTTP detectado en Apache"; sid:1000004; rev:1;)

# Nmap
alert tcp any any -> any any (msg:"Posible escaneo de Nmap detectado"; flags:S; threshold:type threshold, track by_src, count 10, seconds 30; sid:1000005; rev:1;)
```

Para validar la sintaxis de las reglas añadidas puedes ejecutar el siguiente comando:

```bash
sudo snort -T -c /etc/snort/snort.conf
```

## Ejecución de Snort en modo Monitor

Para ejecutar Snort en modo monitor, ejecuta el siguiente comando:
```bash
sudo snort -A console -q -c /etc/snort/snort.conf -i eth0
```
📌 Nota: Reemplaza eth0 con el nombre del adaptador de red que corresponda. (`ip a`)

## Logs
Para ver los logs de Snort, puedes usar los los siguientes comandos:
```bash
sudo tail -f /var/log/snort/alert #final del archivo
sudo cat /var/log/snort/alert
```

## 🎯 Configurar logs personalizados

```bash
sudo nano /etc/snort/snort.conf
```
Busca la línea:
`var LOG_DIR /var/log/snort`
y cámbiala si deseas otro directorio.


# Como Probar Snort

Una vez que hayas configurado Snort, puedes probar su funcionadad con un ataque de intrusión de red. Para ello, puedes usar las siguientes sentencias en la terminal:

> [!NOTE]
> NO LO OLVIDES REINICIAR EL SERVICIO, `sudo systemctl restart snort`

## En otra terminal o máquina
```bash	
ping <IP-de-tu-máquina-con-snort>
```
## Instala nmap si no lo tienes y haz un escaneo
```bash	
sudo apt install nmap
nmap <IP-de-tu-máquina-con-snort>
```
## Intenta conectarte varias veces con una contraseña incorrecta
```bash	
ssh usuario@<IP-de-tu-máquina-con-snort>
```	
## Captura las alertas
```bash
sudo snort -A console -q -c /etc/snort/snort.conf -i eth0
sudo cat /var/log/snort/alert
```
# TRUCO
Cuando ejecutas Snort en modo monitor se queda en primer plano. Hay varias formas de manejarlo:

- **Ejecutar en segundo plano usando &:**
    ```bash
    sudo snort -A console -q -c /etc/snort/snort.conf -i eth0 &
    ```
- **Instalar screen**
  ```bash
  sudo apt install screen
  ```
   Crear una nueva sesión
  ```bash
  screen -S snort
  ```
  Ejecutar Snort
  ```bash
  sudo snort -A console -q -c /etc/snort/snort.conf -i eth0
  ````
  Despegar la sesión: Presiona Ctrl+A y luego D
  Para volver a la sesión:
  ```bash
  screen -r snort 
  ```

- **Crear un servicio**
 
```bash
sudo nano /etc/systemd/system/snort-ids.service
```
```bash
[Unit]
Description=Snort IDS Custom Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/snort -A console -q -c /etc/snort/snort.conf -i enX0
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable snort-ids
sudo systemctl start snort-ids
sudo systemctl status snort-ids
 ```
