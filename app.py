from flask import Flask, render_template, request, redirect, url_for
import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# --- CONFIGURACIÓN DE CORREO ---
# Recomendación: Usá una "Contraseña de aplicación" de Google, nunca tu clave personal.
EMAIL_EMISOR = "rubendarioveronn@gmail.com"
PASSWORD_EMISOR = "nxrg whtx owmr dwoj" 
EMAIL_DESTINO = "rubendarioveronn@gmail.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/solicitar_presupuesto', methods=['POST'])
def solicitar_presupuesto():
    nombre = request.form.get('nombre')
    razon_social = request.form.get('razon_social')
    telefono = request.form.get('telefono')
    email = request.form.get('email')
    direccion = request.form.get('direccion')
    servicio = request.form.get('servicio')
    comentarios = request.form.get('comentarios')

    # Guardar en el archivo CSV local
    archivo_existe = os.path.isfile('presupuestos.csv')
    with open('presupuestos.csv', mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        if not archivo_existe:
            writer.writerow(['Nombre', 'Razón Social', 'Teléfono', 'Email', 'Dirección', 'Servicio', 'Comentarios'])
        writer.writerow([nombre, razon_social, telefono, email, direccion, servicio, comentarios])

    # Enviar correo electrónico automático
    try:
        asunto = f"Nuevo Presupuesto Solicitado - {razon_social}"
        cuerpo = f"""
        ¡Hola Ruben! Tenés una nueva solicitud de presupuesto desde la web de MV Consultora:

        - Apellido y Nombre: {nombre}
        - Razón Social: {razon_social}
        - Teléfono: {telefono}
        - Correo: {email}
        - Dirección: {direccion}
        - Servicio Requerido: {servicio}
        - Comentarios: {comentarios}
        """

        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_EMISOR
        mensaje['To'] = EMAIL_DESTINO
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(EMAIL_EMISOR, PASSWORD_EMISOR)
        servidor.sendmail(EMAIL_EMISOR, EMAIL_DESTINO, mensaje.as_string())
        servidor.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

    return """
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 80px; color: #1a365d;">
            <h2 style="color: #27ae60; font-size: 2rem;">¡Solicitud de presupuesto enviada con éxito!</h2>
            <p style="font-size: 1.1rem; color: #555;">Gracias por contactar a <strong>MV Consultora</strong>. Nos pondremos en contacto a la brevedad.</p>
            <br>
            <a href='/' style="background: #1a365d; color: white; padding: 12px 25px; text-decoration: none; border-radius: 6px; font-weight: bold;">Volver a la página principal</a>
        </div>
    """

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
