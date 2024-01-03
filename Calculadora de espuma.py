from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageDraw
from rectpack import newPacker
    

precios = {"D21": 46000, "D24": 59000, "D30": 79000}
precio_total = 0
espuma_restante = []
largo_inicial = 150
ancho_inicial = 190
grosor_inicial = 10
cortes = []

cantidad_espuma = largo_inicial * ancho_inicial * grosor_inicial

num_planchas = int(input("Ingresa la cantidad de cortes a calcular: "))

for i in range(num_planchas):
    print(f"\nIngresa los detalles para el corte {i + 1}:")
    largo = int(input("Ingresa el largo en cm: "))
    ancho = int(input("Ingresa el ancho en cm: "))
    grosor = float(input("Ingrese grosor en cm (entre 5 y 15): "))
    densidad = input("Ingrese la densidad (D21, D24, D30): ")
    cortes.append((largo, ancho))

    if densidad in precios:
        
        volumen = largo * ancho * grosor
        precio_volumen = precios[densidad] * (volumen / (150 * 190 * 10))
        precio_aprox = round(precio_volumen, -2)
        
        print(f"\nEl precio del corte {i + 1} es: ${precio_volumen:.2f}")
        print(f"El precio del corte {i + 1} aproximado es: ${precio_aprox:.2f}")

        precio_total += precio_volumen
        precio_total_aprox = round(precio_total, -2)

        cantidad_espuma_restante = cantidad_espuma - volumen
        espuma_restante.append(cantidad_espuma_restante)

        # Crear una imagen con fondo blanco que representa la plancha original
        imagen_plancha = Image.new("RGB", (largo_inicial, ancho_inicial), "white")
        dibujante = ImageDraw.Draw(imagen_plancha)

        dibujante.rectangle([(0, 0), (largo_inicial - 1, ancho_inicial - 1)], outline="blue", width=2)


        # Dibujar la cuadrícula que representa la plancha original
        cuadricula = 10  # Tamaño de la cuadrícula
        for i in range(0, largo_inicial, cuadricula):
            dibujante.line([(i, 0), (i, ancho_inicial)], fill="lightgrey", width=1)
        for j in range(0, ancho_inicial, cuadricula):
            dibujante.line([(0, j), (largo_inicial, j)], fill="lightgrey", width=1)

        # Dibujar el corte realizado
        dibujante.rectangle([(0, 0), (int(largo), int(ancho))], outline="red", width=2)

        # Añadir texto con las dimensiones restantes
        dimensiones_restantes = f"Restante: {largo_inicial - int(largo)}x{ancho_inicial - int(ancho)} cm"
        dibujante.text((10, 10), dimensiones_restantes, fill="black")

        # Mostrar la imagen de la plancha original con el corte realizado
        imagen_plancha.show()
       
    else:
        print("Densidad no válida")

# Crear un nuevo packer
packer = newPacker()

# Agregar los cortes al packer
for i, corte in enumerate(cortes):
    packer.add_rect(*corte, rid=i)

# Definir las dimensiones de la plancha
plancha_ancho = 150
plancha_largo = 190

# Añadir la plancha como contenedor
packer.add_bin(plancha_ancho, plancha_largo)

# Empaquetar los rectángulos en la plancha
packer.pack()

# Obtener las coordenadas y tamaños de los rectángulos colocados
coordenadas = packer.rect_list()


# Calcular el área ocupada por los cortes
###area_ocupada = sum(w * h for x, y, w, h, _ in coordenadas)
# Calcular el área restante después de los cortes
###area_restante = plancha_ancho * plancha_largo - area_ocupada



# Crear una imagen con fondo blanco que representa la plancha original
imagen_plancha = Image.new("RGB", (plancha_ancho, plancha_largo), "white")
dibujante = ImageDraw.Draw(imagen_plancha)


# Dibujar la plancha
dibujante.rectangle([(0, 0), (plancha_ancho - 1, plancha_largo - 1)], outline="blue", width=2)

# Dibujar la plancha con una cuadrícula gris
for i in range(0, plancha_ancho, 10):
    dibujante.line([(i, 0), (i, plancha_largo)], fill="lightgrey", width=1)
for j in range(0, plancha_largo, 10):
    dibujante.line([(0, j), (plancha_ancho, j)], fill="lightgrey", width=1)



# Dibujar los cortes
for corte in coordenadas:
    corte_id, x, y, ancho, largo, rotado = corte
    dibujante.rectangle([(x, y), (x + ancho, y + largo)], outline="red", width=2)

# Calcular el espacio ocupado por los cortes
espacio_ocupado_x = max(coordenadas, key=lambda x: x[0] + x[2], default=(0, 0, 0, 0))[0] + max(coordenadas, key=lambda x: x[0] + x[2], default=(0, 0, 0, 0))[2]
espacio_ocupado_y = max(coordenadas, key=lambda x: x[1] + x[3], default=(0, 0, 0, 0))[1] + max(coordenadas, key=lambda x: x[1] + x[3], default=(0, 0, 0, 0))[3]


espacio_restante_x = plancha_ancho - espacio_ocupado_x
espacio_restante_y = plancha_largo - espacio_ocupado_y


# Obtener las dimensiones restantes en la plancha
# Texto con las áreas en la plancha
###texto_areas = f"Área ocupada por los cortes: {area_ocupada} cm²\nÁrea restante: {area_restante} cm²"
dimensiones_restantes = f"Espacio restante: {espacio_restante_x}x{espacio_restante_y} cm"
###dimensiones_restantes = f"Espacio restante: {plancha_ancho - max(coordenadas, key=lambda x: x[0] + x[2])[0]}x{plancha_largo - max(coordenadas, key=lambda x: x[1] + x[3])[1]} cm"
dibujante.text((10, 10), dimensiones_restantes, fill="black")

# Mostrar la imagen
imagen_plancha.show()

    




print(f"\nEl precio total de todas los cortes es: ${precio_total:.2f}")
print(f"El precio total de todas los cortes aproximado es: ${precio_total_aprox:.2f}")

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    largo = int(request.form['largo'])
    ancho = int(request.form['ancho'])
    grosor = float(request.form['grosor'])
    densidad = request.form['densidad']

    if densidad in precios:
        volumen = largo * ancho * grosor
        precio_volumen = precios[densidad] * (volumen / (150 * 190 * 10))
        precio_aprox = round(precio_volumen, -2)
        
        print(f"\nEl precio del corte {i + 1} es: ${precio_volumen:.2f}")
        print(f"El precio del corte {i + 1} aproximado es: ${precio_aprox:.2f}")

        precio_total += precio_volumen
        precio_total_aprox = round(precio_total, -2)

        cantidad_espuma_restante = cantidad_espuma - volumen
        espuma_restante.append(cantidad_espuma_restante)

        # Crear una imagen con fondo blanco que representa la plancha original
        imagen_plancha = Image.new("RGB", (largo_inicial, ancho_inicial), "white")
        dibujante = ImageDraw.Draw(imagen_plancha)

        dibujante.rectangle([(0, 0), (largo_inicial - 1, ancho_inicial - 1)], outline="blue", width=2)


        # Dibujar la cuadrícula que representa la plancha original
        cuadricula = 10  # Tamaño de la cuadrícula
        for i in range(0, largo_inicial, cuadricula):
            dibujante.line([(i, 0), (i, ancho_inicial)], fill="lightgrey", width=1)
        for j in range(0, ancho_inicial, cuadricula):
            dibujante.line([(0, j), (largo_inicial, j)], fill="lightgrey", width=1)

        # Dibujar el corte realizado
        dibujante.rectangle([(0, 0), (int(largo), int(ancho))], outline="red", width=2)

        # Añadir texto con las dimensiones restantes
        dimensiones_restantes = f"Restante: {largo_inicial - int(largo)}x{ancho_inicial - int(ancho)} cm"
        dibujante.text((10, 10), dimensiones_restantes, fill="black")

        # Mostrar la imagen de la plancha original con el corte realizado
        imagen_plancha.show()

        return f'El precio del corte es: {precio_volumen}'  # resultados es el JSON con los resultados
       
    else:
        return "Densidad no válida"




app = Flask(__name__)
@app.route('/calcular_cortes', methods=['POST'])
def calcular_cortes():
    # Estructura los resultados en un diccionario
    resultados = {
        "precios": precios,
        "precio_total": precio_total,
        "precio_volumen": precio_volumen,
    }

    # Convierte los resultados a JSON y devuelve la respuesta
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
    
    
