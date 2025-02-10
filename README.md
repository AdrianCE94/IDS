# IDS (Intrusion Detection System)

## ¿Qué es un IDS?

<table>
  <tr>
    <td>
      <img src="/img/schema.png" alt="Esquema IDS" width="500">
    </td>
    <td>
    Un IDS es un sistema de detección de intrusiones. Es un programa que detecta posibles ataques en un sistema, como una intrusión de datos, una intrusión de servicios, una intrusión de red, etc.
    </td>
  </tr>
</table>




## ¿Cómo funciona un IDS?

El funcionamiento de estas herramientas se basa en el análisis  del tráfico de red, el cual al entrar al analizador es comparado con firmas de ataques conocidos, o comportamientos sospechosos, como puede ser el escaneo de puertos, paquetes malformados, etc. El IDS no solo analiza qué tipo de tráfico es, sino que también revisa el contenido y su comportamiento.

Normalmente esta herramienta se integra con un firewall. El detector de intrusos es incapaz de detener los ataques por sí solo, excepto los que trabajan conjuntamente en un dispositivo de puerta de enlace con funcionalidad de firewall, convirtiéndose en una herramienta muy poderosa ya que se une la inteligencia del IDS y el poder de bloqueo del firewall, al ser el punto donde forzosamente deben pasar los paquetes y pueden ser bloqueados antes de penetrar en la red.

Los IDS suelen disponer de una base de datos de “firmas” de ataques conocidos.

Dichas firmas permiten al IDS distinguir entre el uso normal del PC y el uso fraudulento, y/o entre el tráfico normal de la red y el tráfico que puede ser resultado de un ataque o intento del mismo.

## ¿Qué tipos de ataques se detectan?

Los IDS detectan diferentes tipos de ataques, como:

- Ataques de intrusión de datos: esto incluye ataques como la inyección de SQL, la inyección de código, la inyección de archivos, entre otros.
- Ataques de intrusión de servicios: esto incluye ataques como la inyección de código en los servicios, la inyección de archivos, entre otros.
- Ataques de intrusión de red: esto incluye ataques como la inyección de tráfico, la inyección de paquetes de datos, entre otros.

<p align="center">
  <img src="/img/ids.png" alt="ids" width="450
</p>

## Snort vs Suricata

### **Snort**

> [!NOTE]
> :books: Documentación de Snort: [https://www.snort.org/](https://www.snort.org/)

<p align="center">
  <img src="/img/snort.png" alt="snort" width="300">
</p>

**Snort** es un Sistema de Detección y Prevención de Intrusos (IDS/IPS) basado en firmas, desarrollado por Cisco. Se usa para analizar paquetes de red en tiempo real y detectar amenazas mediante reglas personalizadas. Es ampliamente utilizado en redes pequeñas y medianas debido a su facilidad de uso.

### **Suricata**

> [!NOTE]
> :books: Documentación de Suricata: [https://suricata.io/](https://suricata.io/)

<p align="center">
  <img src="/img/suricata.png" alt="suricata" width="250">
</p>

**Suricata** es un IDS/IPS de código abierto desarrollado por Open Information Security Foundation (OISF). Se diferencia de Snort por su capacidad multihilo, análisis profundo de paquetes (DPI) y compatibilidad con múltiples protocolos. Es ideal para redes con alto tráfico y para integración con herramientas de análisis como Elasticsearch y Kibana.

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

 🛠 **Snort** es ideal para redes pequeñas y medianas donde se necesite una implementación rápida y sencilla.  
🚀**Suricata** es mejor para entornos empresariales con alto tráfico y necesidad de análisis avanzado.  


# Configuración
[Como configurar SNORT](snortconf.md)

[Como configurar SURICATA](suricataconf.md)