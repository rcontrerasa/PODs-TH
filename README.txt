El ejecutable solicita la contraseña del usuario SSH al ejecutarse.
Para cargar un laboratorio se necesitan los archivos de configuracion ISP.txt;R1.txt;R2.txt;R3.txt;DLS1.txt;DLS2.txt;ALS1.txt
Estos estan ubicados en la carpeta de la instalacion en el directorio Configs
Nota: en caso de que un dispositivo no lleve una confiuracion este debe incluir de todas formas el archivo vacio.

                                                              ***Tampermonkey***

Esta extensión es fundamental para ejecutar un script dentro de la página del Access Server, permitiendo la activación de los dispositivos y la correcta carga de configuraciones.
Iniciar sesión en el Access Server (CCNA o CCNP) y acceder a la webshell del primer puerto. El enlace debería tener el siguiente formato: https://172.16.0.13x/?form=webshell&port=1
Instalar la extensión Tampermonkey desde este enlace https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo
Administrar extensiones accediendo a las extensiones del navegador respectivo (chrome://extensions/?id=dhdgffkkebhmkfjojejmpbldmpobfkfo)
Habilitar "Modo de desarrollador" y "Permitir el acceso a las URL del archivo"
(Opcional): "Fijar en la barra de herramientas"
Importa el archivo Script_Tampermonkey-CCNx.js en options > utils o en este enlace (chrome-extension://dhdgffkkebhmkfjojejmpbldmpobfkfo/options.html#nav=utils)
Activar el script y recargar la página; El script se ejecutará automáticamente.
Mantener presionada la tecla "Enter" para activar las terminales.
