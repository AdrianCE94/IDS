# IDS (Intrusion Detection System)

## ¿Qué es un IDS?

Un IDS es un sistema de detección de intrusiones. Es un programa que detecta posibles ataques en un sistema, como una intrusión de datos, una intrusión de servicios, una intrusión de red, etc.

## ¿Cómo funciona un IDS?

Un IDS funciona analizando los datos que se envían a través de la red, y detectando posibles ataques. Esto puede hacerse de varias maneras, como analizar el tráfico de red, analizar los paquetes de datos, o analizar el contenido de los archivos.

## ¿Qué tipos de ataques se detectan?

Los IDS detectan diferentes tipos de ataques, como:

- Ataques de intrusión de datos: esto incluye ataques como la inyección de SQL, la inyección de código, la inyección de archivos, entre otros.
- Ataques de intrusión de servicios: esto incluye ataques como la inyección de código en los servicios, la inyección de archivos, entre otros.
- Ataques de intrusión de red: esto incluye ataques como la inyección de tráfico, la inyección de paquetes de datos, entre otros.

## ¿Cómo se implementa un IDS?

Los IDS se implementan de varias maneras, como:

- Analizando el tráfico de red: esto se hace analizando los paquetes de datos que se envían a través de la red, y detectando posibles ataques.
- Analizando los paquetes de datos: esto se hace analizando los paquetes de datos que se envían a través de la red, y detectando posibles ataques.
- Analizando el contenido de los archivos: esto se hace analizando el contenido de los archivos que se encuentran en el sistema, y detectando posibles ataques.

## Snort vs Suricata

### Snort
<p align="center">
  <img src="/img/snort.png" alt="suricata" width="300">
</p>

**Snort** es un Sistema de Detección y Prevención de Intrusos (IDS/IPS) basado en firmas, desarrollado por Cisco. Se usa para analizar paquetes de red en tiempo real y detectar amenazas mediante reglas personalizadas. Es ampliamente utilizado en redes pequeñas y medianas debido a su facilidad de uso.
### Suricata
<p align="center">
  <img src="/img/suricata.png" alt="suricata" width="250">
</p>
Suricata es un IDS/IPS de código abierto desarrollado por Open Information Security Foundation (OISF). Se diferencia de Snort por su capacidad multihilo, análisis profundo de paquetes (DPI) y compatibilidad con múltiples protocolos. Es ideal para redes con alto tráfico y para integración con herramientas de análisis como Elasticsearch y Kibana.

## Diferencias entre Snort y Suricata
<p align="center">
  <img src="/img/versus.png" alt="versus">
</p>


| Característica  | **Snort**  | **Suricata**  |
|---------------|------------|--------------|
| **Tipo** | IDS/IPS basado en firmas | IDS/IPS con firmas y análisis profundo (DPI) |
| **Procesamiento** | Monohilo (1 hilo por instancia) | Multihilo (usa todos los núcleos disponibles) |
| **Velocidad** | Menos eficiente en alto tráfico | Más rápido y escalable |
| **Reglas** | Propias, pero menos flexibles | Compatible con reglas de Snort y más personalizables |
| **Análisis de protocolos** | TCP, UDP, ICMP | TCP, UDP, ICMP, HTTP, DNS, TLS, SSH, SMB, etc. |
| **Formato de logs** | Texto plano (`fast.log`) | JSON (compatible con SIEM como ElasticSearch) |
| **Facilidad de instalación** | Más sencilla y rápida | Más compleja pero potente |
| **Curva de aprendizaje** | Más fácil para principiantes | Requiere más conocimientos |
| **Uso recomendado** | Redes pequeñas o medianas | Redes grandes y entornos empresariales |
| **Requerimientos de hardware** | Menos exigente | Más consumo de CPU/RAM |

**Conclusión:**  
- **Snort** es ideal para redes pequeñas y medianas donde se necesite una implementación rápida y sencilla.  
- **Suricata** es mejor para entornos empresariales con alto tráfico y necesidad de análisis avanzado.  
