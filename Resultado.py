from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')


@app.route('/')
def datos_personales():
    return render_template('datos_personales.html')


@app.route('/ingresar_datos_corte', methods=['POST'])
def ingresar_datos_corte():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']

    # Puedes guardar estos datos en una base de datos o utilizarlos como desees

    # Redirigir a la página del formulario de corte
    return redirect('/formulario_corte')


@app.route('/formulario_corte')
def formulario_corte():
    return render_template('formulario.html')


precios = {"D21": 46000, "D24": 59000, "D30": 79000}
pesos = {"D21": 6.3, "D24": 7.2, "D30": 8.7}


@app.route('/')
def formulario():
    return render_template('formulario.html')


@app.route('/calcular', methods=['POST', 'GET'])
def calcular():
    largo = int(request.form['largo'])
    ancho = int(request.form['ancho'])
    grosor = float(request.form['grosor'])
    densidad = request.form['densidad']

    if largo > 150:
        mensaje = "Si desea una medida superior a 150 cm de largo, por favor contáctese via WhatsApp."
        return render_template('formulario.html', mensaje=mensaje)

    elif ancho > 190:
        mensaje = "Si desea una medida superior a 190 cm de ancho, por favor contáctese via WhatsApp."
        return render_template('formulario.html', mensaje=mensaje)

    if densidad in precios:
        volumen = largo * ancho * grosor
        precio_volumen = precios[densidad] * (volumen / (150 * 190 * 10))

        if grosor == 5 and densidad == "D21":
            precio_volumen *= 1.67
        elif grosor == 6 and densidad == "D21":
            precio_volumen *= 1.55
        elif grosor == 7 and densidad == "D21":
            precio_volumen *= 1.50
        elif grosor == 8 and densidad == "D21":
            precio_volumen *= 1.35
        elif grosor == 9 and densidad == "D21":
            precio_volumen *= 1.35
        elif grosor == 10 and densidad == "D21":
            precio_volumen *= 1.67
        elif grosor == 11 and densidad == "D21":
            precio_volumen *= 1.67
        elif grosor == 12 and densidad == "D21":
            precio_volumen *= 1.55
        elif grosor == 13 and densidad == "D21":
            precio_volumen *= 1.55
        elif grosor == 14 and densidad == "D21":
            precio_volumen *= 1.55
        elif grosor == 15 and densidad == "D21":
            precio_volumen *= 1.50
        elif grosor == 16 and densidad == "D21":
            precio_volumen *= 1.50
        elif grosor == 17 and densidad == "D21":
            precio_volumen *= 1.50
        elif grosor == 18 and densidad == "D21":
            precio_volumen *= 1.35
        elif grosor == 19 and densidad == "D21":
            precio_volumen *= 1.35
        elif grosor == 20 and densidad == "D21":
            precio_volumen *= 1.35
        elif grosor == 5 and densidad == "D24":
            precio_volumen *= 1.40
        elif grosor == 6 and densidad == "D24":
            precio_volumen *= 1.38
        elif grosor == 7 and densidad == "D24":
            precio_volumen *= 1.35
        elif grosor == 8 and densidad == "D24":
            precio_volumen *= 1.30
        elif grosor == 9 and densidad == "D24":
            precio_volumen *= 1.30
        elif grosor == 10 and densidad == "D24":
            precio_volumen *= 1.40
        elif grosor == 11 and densidad == "D24":
            precio_volumen *= 1.40
        elif grosor == 12 and densidad == "D24":
            precio_volumen *= 1.38
        elif grosor == 13 and densidad == "D24":
            precio_volumen *= 1.38
        elif grosor == 14 and densidad == "D24":
            precio_volumen *= 1.38
        elif grosor == 15 and densidad == "D24":
            precio_volumen *= 1.35
        elif grosor == 16 and densidad == "D24":
            precio_volumen *= 1.35
        elif grosor == 17 and densidad == "D24":
            precio_volumen *= 1.35
        elif grosor == 18 and densidad == "D24":
            precio_volumen *= 1.30
        elif grosor == 19 and densidad == "D24":
            precio_volumen *= 1.30
        elif grosor == 20 and densidad == "D24":
            precio_volumen *= 1.30
        elif grosor == 5 and densidad == "D30":
            precio_volumen *= 1.35
        elif grosor == 6 and densidad == "D30":
            precio_volumen *= 1.31
        elif grosor == 7 and densidad == "D30":
            precio_volumen *= 1.30
        elif grosor == 8 and densidad == "D30":
            precio_volumen *= 1.28
        elif grosor == 9 and densidad == "D30":
            precio_volumen *= 1.30
        elif grosor == 10 and densidad == "D30":
            precio_volumen *= 1.35
        elif grosor == 11 and densidad == "D30":
            precio_volumen *= 1.35
        elif grosor == 12 and densidad == "D30":
            precio_volumen *= 1.31
        elif grosor == 13 and densidad == "D30":
            precio_volumen *= 1.31
        elif grosor == 14 and densidad == "D30":
            precio_volumen *= 1.31
        elif grosor == 15 and densidad == "D30":
            precio_volumen *= 1.30
        elif grosor == 16 and densidad == "D30":
            precio_volumen *= 1.30
        elif grosor == 17 and densidad == "D30":
            precio_volumen *= 1.30
        elif grosor == 18 and densidad == "D30":
            precio_volumen *= 1.28
        elif grosor == 19 and densidad == "D30":
            precio_volumen *= 1.28
        elif grosor == 20 and densidad == "D30":
            precio_volumen *= 1.28

        precio_aprox = round(precio_volumen, -2)
        peso_corte = pesos[densidad] * (volumen / (150 * 190 * 10))
        peso_aprox = round(peso_corte, 3)

        return render_template('resultado.html', precio=precio_aprox, peso=peso_aprox)

    else:
        return "Densidad no válida"


if __name__ == '__main__':
    # app.run(debug=True, port = 59547)
    app.run(debug=True, port=5000)
