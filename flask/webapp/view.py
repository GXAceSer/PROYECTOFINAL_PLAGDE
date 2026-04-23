from . import app
from flask import Flask, jsonify, request, render_template, flash, url_for, session, redirect
#Importacion base de datos
from . import bd
from .bd import get_connection
from psycopg2.extras import RealDictCursor
#Para el PDF
#Importaciones para crear el pdf: 
from io import BytesIO
from fpdf import FPDF
#Importaciones para el diseño del documento
from weasyprint import HTML, CSS
import pdfkit
import datetime 
#Importaciones para nombre pdf
from urllib.parse import quote
from flask import send_file
#Para imprimir en pantalla
from weasyprint import HTML



#Bienvenida al generador-------------------------------------------------------------------------
@app.route('/generador', methods=['GET'])
def bienvenida():
   #Login:
   if 'user_id' not in session:
       return redirect(url_for('login'))
   return render_template('generador.html') #Muestra la plantilla base

#-----------------------------------------------------------------------------------------------

#LOGIN-------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET','POST'])
def login():
    #Si es metodo post
    if request.method == 'POST':
        #Obtenemos los datos ingresados
        email = request.form['email']
        contraseña = request.form['contraseña'] 

        #Conexion con la base de datos y consulta
        conexion = get_connection()
        cursor = conexion.cursor()
        #Consulta
        cursor.execute("SELECT id, contraseña FROM usuario WHERE email=%s", (email,))
        usuario = cursor.fetchone() #Los datos se quedaran en la variable usuario
        #fin conexion base de datos
        cursor.close()
        conexion.close()   

        #Comparando contraseña
        if usuario and usuario[1] == contraseña: #Si la contraseña y usuario son igual a la contraseña guardada
            session['user_id'] = usuario[0]
            return redirect(url_for('bienvenida')) #manda la bienvenida 
        else:
            flash('Email o contraseña incorrectos', 'error')

    return render_template('login.html')
#-----------------------------------------------------------------------------------------------
#LOGOUT-----------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
#-----------------------------------------------------------------------------------------------

#CONSTANCIA-------------------------------------------------------------------------
@app.route('/generador/constancia', methods=['GET', 'POST'])
def constancia():
   #Comprobar si hizo inicio de sesion
   if 'user_id' not in session:
       return redirect(url_for('login'))
   
   #Si el usuario entra por GET, mostramos el formulario 
   if request.method == 'GET':
    return render_template('formularioConstancia.html') #Muestra la plantilla base
   
    #Si el usuario ya envió el formulario POST
   if request.method == 'POST':
       #El usuario ingresa la matricula del estudiante
       matricula = request.form['matricula']
       #Ahora nos conectamos a la base de datos 
       conexion = get_connection()
       cursor = conexion.cursor()

       #Buscamos al alumno con la matricula que ingresaron
       cursor.execute("SELECT nombre, apellido_P, apellido_M, grado, grupo FROM alumno WHERE matricula = %s", (matricula,))
       alumno = cursor.fetchone()
       #Cerramos 
       cursor.close() 
       conexion.close()
       
     #Obtener el año actual 
       now = datetime.datetime.now()
       año_Ac = now.year
       año_Sig= now.year + 1

       #Variable ciclo escolar 
       ciclo = f"{año_Ac} - {año_Sig}"

    #Generamos el PDF
   if alumno: 
       #Le pasamos los valores a cada variable
       nombre, apellido_P, apellido_M, grado, grupo = alumno
       #Creamos el PDF
       rendered_html = render_template(
                'constancia.html',
                nombre=nombre,
                apellido_P=apellido_P,
                apellido_M=apellido_M,
                grado=grado,
                grupo=grupo,
                ciclo=ciclo
            )
        #Generamos PDF en memoria
       pdf_bytes = HTML(string=rendered_html).write_pdf()
       pdf_output = BytesIO(pdf_bytes)
       pdf_output.seek(0)
       #Eenviamos el archivo PDF para descargar: 
       return send_file(
                pdf_output,
                as_attachment=True,
                download_name=f"constancia_{quote(nombre)}_{quote(apellido_P)}.pdf",
                mimetype='application/pdf'
            )
       
   else: 
      return render_template('formularioConstancia.html')
        
#-----------------------------------------------------------------------------------------------

#DIPLOMA-------------------------------------------------------------------------
@app.route('/generador/diplomado', methods=['GET', 'POST'])
def diploma():
   #Comprobar si hizo inicio de sesion
   if 'user_id' not in session:
       return redirect(url_for('login'))
   
   #Si el usuario entra por GET
   if request.method == 'GET':
    return render_template('formularioDiplomado.html') #Muestra la plantilla base
   
    #Si el usuario ya envió el formulario POST
   if request.method == 'POST':
       #El usuario ingresa la matricula del estudiante
       matricula = request.form['matricula']
       #Ahora nos conectamos a la base de datos 
       conexion = get_connection()
       cursor = conexion.cursor()

       #Buscamos al alumno con la matricula que ingresaron
       cursor.execute("SELECT nombre, apellido_P, apellido_M, grado, grupo, promedio FROM alumno WHERE matricula = %s", (matricula,))
       alumno = cursor.fetchone()
       
       #Cerramos 
       cursor.close() 
       conexion.close()
       
       #----Fecha realizacion------------------------
       #El usuario ingresa la matricula del estudiante
       fechaR = request.form['fechaR']
       #Ahora nos conectamos a la base de datos 
       conexion = get_connection()
       cursor = conexion.cursor()

       #Buscamos al alumno con la matricula que ingresaron
       cursor.execute("INSERT INTO diplomado (fechaR, id_alumno) VALUES (%s, %s) RETURNING id",(fechaR, matricula))
       diplomado_id_generado = cursor.fetchone()[0] # Guardamos el ID retornado en una nueva variable

       
       #Cerramos 
       cursor.close() 
       conexion.close()

       #Formato fecha: 
       try:
          fObj = datetime.datetime.strptime(fechaR, '%Y-%m-%d')
          meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
          7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
          fecha_Reg = f"{fObj.day} DE {meses[fObj.month].upper()} DE {fObj.year}"
       except: 
           fecha_Reg = fechaR

     #Obtener el año actual ----------------------
       now = datetime.datetime.now()
       año_Ac = now.year
       año_Sig= now.year + 1

       #Variable ciclo escolar 
       ciclo = f"{año_Ac} - {año_Sig}"

    #Generamos el PDF
   if alumno: 
       #Le pasamos los valores a cada variable
       nombre = alumno[0].upper()
       apellido_P = alumno[1].upper()
       apellido_M = alumno[2].upper()
       grado = alumno[3].upper()
       grupo = alumno[4].upper()
       promedio = alumno[5]
       #Creamos el PDF
       rendered_html = render_template(
                'diplomado.html',
                nombre=nombre,
                apellido_P=apellido_P,
                apellido_M=apellido_M,
                grado=grado,
                grupo=grupo,
                promedio = promedio,
                ciclo=ciclo,
                fecha_Reg=fecha_Reg
            )
        #Generamos PDF en memoria
       pdf_bytes = HTML(string=rendered_html).write_pdf()
       pdf_output = BytesIO(pdf_bytes)
       pdf_output.seek(0)
       #Eenviamos el archivo PDF para descargar: 
       return send_file(
                pdf_output,
                as_attachment=True,
                download_name=f"diploma_{quote(nombre)}_{quote(apellido_P)}.pdf",
                mimetype='application/pdf'
            )
       
   else: 
      return render_template('formularioDiplomado.html')

#-----------------------------------------------------------------------------------------------
@app.route('/generador/citatorio', methods=['GET', 'POST'])
def citatorio():
    #Comprobar si hizo inicio de sesion
    if 'user_id' not in session:
       return redirect(url_for('login'))
      
    # PROFESORES 
    # Inicializamos las variables 
    conexion = None
    cursor = None
    # Lista de profesores: 
    lista_prof = []  # Inicializamos

    # En caso: 
    try: 
        # Conexion base: 
        conexion = get_connection()
        cursor = conexion.cursor()

        # Obtenemos la lista de profesores
        cursor.execute("SELECT id_profesor, nombreP, materia FROM profesor ORDER BY nombreP")
        prof_db = cursor.fetchall()  # Aquí se almacenarán los datos de manera de tuplas como (1, 'juanito perez', 'ciencias naturales')

        # Lista profesores para mostrar
        for p in prof_db: 
            # p[0] es idprofesor
            # p[1] es nombreP
            # p[2] es materia
            lista_prof.append({
                'id': p[0],  # id
                'nombreP': p[1],
                'materia': p[2]
            })
        
        # Si el usuario entra por GET 
        if request.method == 'GET':
            return render_template('formularioCitatorio.html', lista_prof=lista_prof)  # Muestra la plantilla base

        # Si el usuario ya envió el formulario POST
        if request.method == 'POST':
            # -----------------ALUMNO y TUTOR-----------------------------------------------------------------------------------------------------
            matricula = request.form['matricula']
            # Como queremos que al momento de ingresar la matrícula del alumno se enlace con su respectivo tutor hacemos la siguiente 
            # consulta: 
            cursor.execute("""
                    SELECT
                        a.nombre, a.apellido_P, a.apellido_M, a.grado, a.grupo,
                        t.nombreT, t.apellido_PT, t.apellido_MT
                    FROM
                        alumno a
                    JOIN
                        alumno_tutor at ON a.matricula = at.id_A
                    JOIN
                        tutor t ON at.id_T = t.id_T
                    WHERE
                        a.matricula = %s
                """, (matricula,))
            aluANDtut = cursor.fetchone()  # Aquí se guardan los datos

            # En caso de que el alumno o tutor no se encuentren
            if not aluANDtut: 
                return render_template('fail.html',
                                    lista_prof=lista_prof,
                                    error_message="Error: Alumno o su tutor no encontrado. Por favor, verifica la matrícula y la relación tutor-alumno.")
            
            # Asignamos los valores 
            # Donde los índices son los siguientes: 0=a.nombre, 1=a.apellido_P, 2=a.apellido_M, 3=a.grado, 4=a.grupo,
            #          5=t.nombreT, 6=t.apellido_PT, 7=t.apellido_MT 
            # ---------------ALUMNO-----------------------
            alumno = aluANDtut[0]
            apellido_P = aluANDtut[1]
            apellido_M = aluANDtut[2]
            grado = aluANDtut[3]
            grupo = aluANDtut[4]
            # --------------FIN ALUMNO--------------------
            # --------------TUTOR----------------------
            nombreT = aluANDtut[5]
            apellido_PT = aluANDtut[6]
            apellido_MT = aluANDtut[7]
            # -------------FIN TUTOR-------------------
            # -----------------FIN ALUMNO Y TUTOR------------------------------------------------------------------------------------------------
            
            # -----------------PROFESOR-----------------------------------------------------------------------------------------------------
            prof_Sel = request.form['id_profesor']  # obtenemos como cadena
            
            
            # ***************************************************
            # Consulta para extraer los datos
            cursor.execute("SELECT nombreP , materia FROM profesor WHERE id_profesor = %s", (prof_Sel,))
            prof_datos = cursor.fetchone()

            # Por si no encuentra el profesor
            if not prof_datos: 
                return render_template('fail2.html',
                                    lista_prof=lista_prof,
                                    error_message="Error: Profesor no encontrado. Selecciona uno válido de la lista.")
            
            # Valores por separado
            nombre_prof = prof_datos[0]
            materia_prof = prof_datos[1]
            # -----------------FIN PROFESOR------------------------------------------------------------------------------------------------
              
            # ------------------DATOS CITATORIO----------------------------------------------------------------------------------------------------
            # ---FECHA REALIZACION------
            fecha_rea = request.form['fecha_R']
            # -----FECHA CITA----------------
            fecha_C = request.form['fecha_Cita']
            # -----HORA----------------------
            hora_C = request.form['hora']
            # -----MOTIVO--------
            motivoC = request.form['motivo']
            # --------FIN MOTIVO---------
            try: 
                fecha_Reg_db = datetime.datetime.strptime(fecha_rea, '%Y-%m-%d').date()
                fecha_cita_db = datetime.datetime.strptime(fecha_C, '%Y-%m-%d').date()
                hora_db = hora_C

                # Hacemos la búsqueda en la base de datos:
                cursor.execute("""
                            INSERT INTO citatorio (fecha_R, fecha_Cita, hora, motivo, id_profesor)
                            VALUES (%s, %s, %s, %s, %s) RETURNING id;
                        """, (fecha_Reg_db, fecha_cita_db, hora_db, motivoC, prof_Sel))

                # Obtenemos el ID del citatorio insertado 
                citatorio_id = cursor.fetchone()[0]
                conexion.commit()
            except Exception as e: 
                conexion.rollback()  # Si algo falla, revertimos el insert
                print(f"ERROR al insertar citatorio: {e}")
                return render_template('fail3.html',
                                    lista_prof=lista_prof,
                                    error_message=f"Error al guardar el citatorio en la base de datos: {e}")
            
            # Obtenemos los datos del citatorio
            cursor.execute("SELECT fecha_R, fecha_Cita, hora, motivo FROM citatorio WHERE id = %s", (citatorio_id,))
            citatorio_data_from_db = cursor.fetchone()
                
            if not citatorio_data_from_db:
                return render_template('fail4.html',
                                    lista_prof=lista_prof,
                                    error_message="Error: No se pudo recuperar el citatorio recién guardado para el PDF.")

            # Extraemos los datos separados para ponerlos en el formato
            fechaR_pdf = citatorio_data_from_db[0] 
            fechaC_pdf = citatorio_data_from_db[1]     
            hora_obj = citatorio_data_from_db[2]      
            # FORMATO HORAS 
            hora_pdf = hora_obj.strftime("%H:%M")

            motivo_pdf = citatorio_data_from_db[3]

            # FORMATO FECHAS
            meses_dict = {
                1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
                7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
            }
                
            # Formatear la fecha de registro para el PDF
            fechaR_for = f"{fechaR_pdf.day} de {meses_dict[fechaR_pdf.month]} de {fechaR_pdf.year}"

            # Formatear la fecha de la cita para el PDF
            fechaC_for = f"{fechaC_pdf.day} de {meses_dict[fechaC_pdf.month]} de {fechaC_pdf.year}"

            # -------------------------------CREAMOS PDF-----------------------------------------------------------
            print("Generando PDF...")
            rendered_html = render_template(
                'citatorio.html',
                alumno=alumno,
                apellido_P=apellido_P,
                apellido_M=apellido_M,
                grado=grado,
                grupo=grupo,
                nombreT=nombreT,
                apellido_PT=apellido_PT,
                apellido_MT=apellido_MT,
                motivo_citatorio=motivo_pdf, 
                fecha_Cit=fechaC_for, 
                hora=hora_pdf,           
                profesor=nombre_prof,
                materia=materia_prof,
                fechaReg=fechaR_for 
            )

            # Generamos PDF
            pdf_bytes = HTML(string=rendered_html).write_pdf()
            pdf_output = BytesIO(pdf_bytes)
            pdf_output.seek(0)
            print("PDF generado, tamaño:", pdf_output.getbuffer().nbytes)

            return send_file(
                pdf_output,
                as_attachment=True,
                download_name=f"citatorio_{quote(alumno)}_{quote(apellido_P)}_{citatorio_id}.pdf",
                mimetype='application/pdf'
            )
   
    except Exception as e: 
        print(f"ERROR: Fallo general en citatorio(): {e}")
        if conexion:
            conexion.rollback()
        return render_template('fail5.html',
                            error_message=f"Ocurrió un error al generar el citatorio: {e}",
                            lista_prof=lista_prof)
    

    finally: 
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

#/-----------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return redirect(url_for('login'))