# Hilos
<p> ... </p>

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
