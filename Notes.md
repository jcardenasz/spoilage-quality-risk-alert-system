APRENDIZAJES HASTA EL MOMENTO:
1. Divide y venceras: Es mucho mejor comenzar por hacer pocas cosas de la mano de claude code e ir permitiendo mayor libertad a la herramienta que pedir de un solo prompt que realice las cosas y esperar a que funcionen. Si se pide todo el proyecto en un prompt es realmente dificil entender el código que realiza y es aún más complicado debuggearlo para llegar a buen fin.

2. Conocer cada paso del proceso y sus necesidades. Desde conocer cada parte del problema y cada fase de desarrollo hasta definir exactamente cuales son las entradas y salidas de cada parte, estandar de datos y transmisión, entre otros.

3. Leí en un foro de reddit que Claude code funciona mejor en Linux que en Windows, por lo que lo utilizo en la consola de linux que proporciona WSL.

ACCIONES REALIZADAS:

1. Pedí todo de una vez a Claude y no entendí, no logré hacer que funcionara.
2. Comencé por comenzar viendo cómo funciona n8n y seguí un paso a paso que claude dió.
3. Volví atrás a realizar una tabla de qué recursos se almacenan junto a sus factores óptimos de almacenamiento
4. Redefinir las variables de los recursos a analizar. Retiré el supplier incident y moisture dentro de cada paquete.
5. Definí la ruta de acción del proceso (con un diagrama de flujo) y luego analicé y definí los thresholds de los riesgos, para que luego el agente de IA pueda tener el prompt indicado.
6. Comencé con la realización de la función generadora de batches y me di cuenta que claude code con estos tokens gratis genera errores y le cuesta mucho corregirlos. Llegué al límite de modelos gratis del día, es frustrante.
7. Dado el formato de los datos generados por el simulador, se decide cambiar de usar una base de datos como AIRTABLE, por MongoDB, debido a que el estilo es muy similar a un documento de mongo.
8. Crear un paso a mano en el workflow de n8n para leer los datos de la base de datos de mongo para luego insertar cada batch en un programa que preprocesa los datos para que el Agente de IA tenga información más precisa.