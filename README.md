# Hilos
<p> los hilos (threads) permiten que un programa realice varias tareas de manera concurrente sin tener que esperar a que una termine para comenzar otra. Cada hilo se encarga de una tarea específica y puede trabajar de forma independiente, lo que ayuda a aprovechar mejor el tiempo y a que el programa funcione de manera más fluida. Por ejemplo, mientras un hilo analiza información, otro puede realizar una operación diferente. Esto es útil para evitar que el programa se quede bloqueado mientras realiza tareas que pueden tardar un poco. </p>

### ¿como funciona el programa?
<p> en el programa se realizo un analizador de contraseñas, en el se solicitan las contraseñas, se revisan las caracteristicas (contenido en mayusculas, minusculas, numeros, simbolos y si es muy corta por medio de la difiultad, yaa sea debil, media o fuerte), y se determina si la contraseña es debil, media o fuerte. en el se utilizan los hilos para la concurrencia. </p>

### Funciones:

- Hilo 1: en el se verifica la longitud de la contraseña.
- Hilo 2: en el se comprueban las mayusculas y minusculas.
- Hilo 3: en el se detectan los numeros y Simbolos.
- Programa principal: en el se reunen los resultados y verifica si la contraseña es debil, media o ferte.
- Interfaz: en el se permite mostrar en una interfaz de manera ordenada, el analisis, recomendaciones, mostrar/ocultar a contraseña que se escribio, eliminar las contraseñas, etc...
- Consola: muestra el inicio de cada hilo y el resultado obtenido.

### ¿como se demuestra el uso de Hilos?
<p> al presionar el analizar contraseñas, se crearan tres hilos que ejecutan sus comprobaciones de manera concurrente. cada uno envia resultados a una cola compartida; el principal recoge esos resultados y actualiza el Tkinter, en forma segura. la pequeña pausa permite observar la actividad de los hilos. </p>

*Nota: el rpograma no imprime contraseñas, ni guarda en los archivos.*
