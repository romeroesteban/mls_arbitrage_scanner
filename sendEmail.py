import smtplib
from email.mime.text import MIMEText

# Configuración del servidor de correo
SMTP_SERVER = 'smtp.office365.com'  # Servidor SMTP de proveedor de correo
SMTP_PORT = 587  # Puerto del servidor SMTP
SMTP_USERNAME = 'esteban98@live.com.mx'  # Tu dirección de correo electrónico
SMTP_PASSWORD = '2486753159852456'  # Tu contraseña de correo electrónico

# Función para enviar el correo electrónico
def send_email(subject, body):
    sender = SMTP_USERNAME
    receivers = ['romeroesteban@ciencias.unam.mx']  # Dirección del destinatario

    # Crear un objeto MIMEText con el cuerpo del correo
    msg = MIMEText(body, 'plain')

    # Configurar el asunto y los remitentes
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)

    try:
        smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.starttls()
        smtpObj.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        smtpObj.quit()
        print("Correo electrónico enviado correctamente")
    except smtplib.SMTPException:
        print("Error al enviar el correo electrónico")