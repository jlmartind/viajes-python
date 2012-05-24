# -*- coding:utf-8 -*-
from suds.client import Client
from suds.plugin import MessagePlugin
from lxml import etree


        #********************************************
        #*** APLICACIÓN PARA LA DESCARGA DE DATOS *** 
        #***    ESTÁTICOS DESDE EL WEB SERVICE    ***
        #********************************************



# Lectura de credenciales desde fichero 'cuentasstatic.cfg'
# *********************************************************

    # Abrimos el fichero que contiene las credenciales de información estática
ficherocs = open ('cuentasstatic.cfg','r')

    # inicializamos un nombre para cada lista de variables
proveedor = []
direccion = []
usuario = []
clave = []
sucursal = []

    # con este bucle creamos las listas de los diferentes datos
for i in ficherocs:
	campos = i.split(';;')
        proveedor.append(campos[1])
        direccion.append(campos[2])
        usuario.append(campos[3])
        clave.append(campos[4])
        sucursal.append(campos[5])

    # cerramos el fichero de credenciales
ficherocs.close()



# Consulta y almacenado de datos estáticos de los paises
#*******************************************************

# Se definen los atributos de los elementos del XML de la petición SOAP
# de la siguiente manera (es necesario utilizar # suds >= 0.4):

class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        body = context.envelope.getChild('Body')
    # Elemento hijo del Body de SOAP, con atributos version y sessionId
        destino = body[0]
        destino.set('version', '5.0')
        destino.set('sessionId', '55551')
    # Primer elemento hijo de destino, con atributos password, branch y 
    # code (utilizando las variables de la consulta al fichero de credenciales)
        client = destino[0]
        client.set('password', clave[0])
        client.set('branch', sucursal[0])
        client.set('code', usuario[0])
    # Segundo elemento hijo de destino, con atributo code
        language = destino[1]
        language.set('code', 'SPA')
        

    # URL WSDL del servicio SOAP (utilizando la variable de consulta credenciales) 
url = direccion[0]
    # Instanciamos el cliente SOAP
cliente = Client(url,plugins=[MyPlugin()])
    # Queremos que las respuestas del cliente sean en XML
cliente.set_options(retxml=True)

# Formamos la salida del método GET_COUNTRIES como html para las listas 
# que necesitamos en nuestro formulario web

    # Formateamos la salida del método
arbolpais = etree.fromstring(cliente.service.GET_COUNTRIES())
    # Definimos el listado que utilizaremos en el primer bucle
paises = arbolpais.xpath ("//country/@name")
    # Indicamos el elemento raiz de nuestros datos con los atributos 'method' y 'action' 
raizhtml_pais = etree.Element("form",attrib={"method":"post","action":"viajes.py"})
    # Creamos la estructura del arbil a partir del elemento raiz
arbolhtml_pais = etree.ElementTree (raizhtml_pais)
    # Bucle para la obtención de los nombres y códigos de los paises
for pais in paises:
    nombre_pais = pais
    nombre_pa = arbolpais.xpath ("//country[@name='%s']" %nombre_pais)
    codigo_pais = arbolpais.xpath ("//country[@name='%s']/@code" %nombre_pais)
    for pais2 in codigo_pais:
        option = etree.SubElement(raizhtml_pais, "option", attrib={"value":'%s'%pais2})
        option.text = '%s' %pais

    # Creamos el fichero 'paises.html' y le asignamos la variable 'ficheropais'
ficheropais = open('paises.html', 'w')
    # Escribimos el fichero con el contenido del arbol creado anteriormente
ficheropais.write(etree.tostring(arbolhtml_pais,pretty_print=True))
    # Cerramos el fichero creado
ficheropais.close()
    # Se imprime un mensaje indicando el nombre del fichero creado
    # éste mensaje sirve además para que el usuario compruebe que hay
    # progreso en la ejecución, ya que ésta puede tardar
print 'Resultados almacenados en el fichero "paises.html"'



# consulta de datos estáticos para las áreas
#*******************************************

# Se definen los atributos de los elementos del XML de la petición SOAP
# de la siguiente manera (es necesario utilizar # suds >= 0.4):
    
class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        body = context.envelope.getChild('Body')
    # Elemento hijo del Body de SOAP, con atributos version y sessionId
        destino = body[0]
        destino.set('version', '5.0')
        destino.set('sessionId', '5555')
    # Primer elemento hijo de destino, con atributos password, branch y 
    # code (utilizando las variables de la consulta al fichero de credenciales)
        client = destino[0]
        client.set('password', 'klmw4sjyyb')
        client.set('branch', '8249')
        client.set('code', 'ESTTRV')
    # Segundo elemento hijo de destino, con atributo code
        language = destino[1]
        language.set('code', 'SPA')

    # URL WSDL del servicio SOAP (utilizando la variable de consulta credenciales)
url = direccion[0]
    # Instanciamos el cliente SOAP
cliente = Client(url,plugins=[MyPlugin()])
    # Queremos que las respuestas del cliente sean en XML
cliente.set_options(retxml=True)

    # Formateamos la salida del método
arbolarea = etree.fromstring(cliente.service.GET_AREAS())
    # Definimos el listado que utilizaremos en el primer bucle
areas = arbolarea.xpath ("//area/@name")
    # Indicamos el elemento raiz de nuestros datos con los atributos 'method' y 'action' 
raizhtml_area = etree.Element("form",attrib={"method":"post","action":"viajes.py"})
    # Creamos la estructura del arbil a partir del elemento raiz
arbolhtml_area = etree.ElementTree (raizhtml_area)
    # Bucle para la obtención de los nombres y códigos de areas
for are in areas:
    nombre_area = are
    area = arbolarea.xpath ("//area[@name='%s']/subareas/subarea/@name" %nombre_area)
    codigo_area = arbolarea.xpath ("//area[@name='%s']/@code" %nombre_area)
    for are2 in codigo_area:
    # Se crean los grupos de áreas (se muestra el nombre como título)
        optgroup = etree.SubElement(raizhtml_area, "optgroup",attrib={"label":'%s'%are})
    # Se repite de nuevo el mismo elemento pero esta vez como opción, indicando
    # nombre y el valor que utiliza, añadimos la cadena '(todo)' a continuación
    # del nombre, ya que si se selecciona esta opción se busca en todo el grupo
        option = etree.SubElement(optgroup, "option", attrib={"value":'%s'%are2})
        option.text = '%s'' (todo)' %are
    
    # Con este bucle se listan los subareas de cada grupo
    for are3 in area:
        nombre_ar = are3
        codigo_area = arbolarea.xpath ('//subarea[@name="%s"]/@code' %nombre_ar)
        for are4 in codigo_area:
            option = etree.SubElement(optgroup, "option", attrib={"value":'%s'%are4})
            option.text = '%s' %are3

    # Creamos el fichero 'areas.html' y le asignamos la variable 'ficheroa'
ficheroa = open('areas.html', 'w')
    # Escribimos el fichero con el contenido del arbol creado anteriormente
ficheroa.write(etree.tostring(arbolhtml_area,pretty_print=True))
    # Cerramos el fichero creado
ficheroa.close()
    # Se imprime un mensaje indicando el nombre del fichero creado
    # éste mensaje sirve además para que el usuario compruebe que hay
    # progreso en la ejecución, ya que ésta puede tardar
print 'Resultados almacenados en el fichero "areas.html"'





# consulta de datos estáticos Para las ciudades de España
#********************************************************

# Se definen los atributos de los elementos del XML de la petición SOAP
# de la siguiente manera (es necesario utilizar # suds >= 0.4):
    
class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        body = context.envelope.getChild('Body')
    # Elemento hijo del Body de SOAP, con atributos version y sessionId
        destino = body[0]
        destino.set('version', '5.0')
        destino.set('sessionId', '5555')
    # Primer elemento hijo de destino, con atributos password, branch y 
    # code (utilizando las variables de la consulta al fichero de credenciales)
        client = destino[0]
        client.set('password', clave[0])
        client.set('branch', sucursal[0])
        client.set('code', usuario[0])
    # Segundo elemento hijo de destino, con atributo code
        language = destino[1]
        language.set('code', 'SPA')
    # Tercer elemento hijo de destino, con atributo code
        country = destino[2]
        country.set('code', 'ESP')

    # URL WSDL del servicio SOAP (utilizando la variable de consulta credenciales)
url = direccion[0]
    # Instanciamos el cliente SOAP
cliente = Client(url,plugins=[MyPlugin()])
    # Queremos que las respuestas del cliente sean en XML
cliente.set_options(retxml=True)

# Formamos la salida del método GET_CITIES como html para las listas 
# que necesitamos en nuestro formulario web

    # Formateamos la salida del método
arbolsp = etree.fromstring(cliente.service.GET_CITIES())
    # Definimos el listado que utilizaremos en el primer bucle
provinciassp = arbolsp.xpath ("//region/@name")
    # Indicamos el elemento raiz de nuestros datos con los atributos 'method' y 'action' 
raizhtml_c_e = etree.Element("form",attrib={"method":"post","action":"viajes.py"})
    # Creamos la estructura del arbil a partir del elemento raiz
arbolhtml_c_e = etree.ElementTree (raizhtml_c_e)
    # Bucle para la obtención de los nombres y códigos de ciudades
for loc in provinciassp:
    nombre_pro = loc
    ciudad = arbolsp.xpath ("//region[@name='%s']/cities/city/@name" %nombre_pro)
    codigo_prov = arbolsp.xpath ("//region[@name='%s']/@code" %nombre_pro)
    for locb in codigo_prov:
    # Se crean los grupos de provincias (se muestra el nombre como título)
        optgroup = etree.SubElement(raizhtml_c_e, "optgroup",attrib={"label":'%s'%loc})
    # Se repite de nuevo el mismo elemento pero esta vez como opción, indicando
    # nombre y el valor que utiliza, añadimos la cadena '(provincia)' a continuación
    # del nombre, ya que si se selecciona esta opción se busca en todo el grupo
        option = etree.SubElement(optgroup, "option", attrib={"value":'%s'%locb})
        option.text = '%s'' (provincia)' %loc
    
    # Con este bucle se listan las localidades de cada provincia
    for locc in ciudad:
        nombre_loc = locc
        codigo_loc = arbolsp.xpath ('//city[@name="%s"]/@code' %nombre_loc)
        for locd in codigo_loc:
            option = etree.SubElement(optgroup, "option", attrib={"value":'%s'%locd})
            option.text = '%s' %locc

    # Creamos el fichero 'ciudades_esp.html' y le asignamos la variable 'ficherosp'
ficherosp = open('ciudades_esp.html', 'w')
    # Escribimos el fichero con el contenido del arbol creado anteriormente
ficherosp.write(etree.tostring(arbolhtml_c_e,pretty_print=True))
    # Cerramos el fichero creado
ficherosp.close()
    # Se imprime un mensaje indicando el nombre del fichero creado
    # éste mensaje sirve además para que el usuario compruebe que hay
    # progreso en la ejecución, ya que ésta puede tardar
print 'Resultados almacenados en el fichero "ciudades_esp.html"'



# consulta de datos estáticos Para las ciudades de Portugal
#**********************************************************

# Se definen los atributos de los elementos del XML de la petición SOAP
# de la siguiente manera (es necesario utilizar # suds >= 0.4):
    
class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        body = context.envelope.getChild('Body')
    # Elemento hijo del Body de SOAP, con atributos version y sessionId
        destino = body[0]
        destino.set('version', '5.0')
        destino.set('sessionId', '55555')
    # Primer elemento hijo de destino, con atributos password, branch y 
    # code (utilizando las variables de la consulta al fichero de credenciales)
        client = destino[0]
        client.set('password', clave[0])
        client.set('branch', sucursal[0])
        client.set('code', usuario[0])
    # Segundo elemento hijo de destino, con atributo code
        language = destino[1]
        language.set('code', 'SPA')
    # Tercer elemento hijo de destino, con atributo code
        country = destino[2]
        country.set('code', 'PRT')

    # URL WSDL del servicio SOAP (utilizando la variable de consulta credenciales)
url = direccion[0]
    # Instanciamos el cliente SOAP
cliente = Client(url,plugins=[MyPlugin()])
    # Queremos que las respuestas del cliente sean en XML
cliente.set_options(retxml=True)

# Formamos la salida del método GET_CITIES como html para las listas 
# que necesitamos en nuestro formulario web

    # Formateamos la salida del método
arbolpt = etree.fromstring(cliente.service.GET_CITIES())
    # Definimos el listado que utilizaremos en el primer bucle
provinciaspt = arbolpt.xpath ("//region/@name")
    # Indicamos el elemento raiz de nuestros datos con los atributos 'method' y 'action' 
raizhtml_c_p = etree.Element("form",attrib={"method":"post","action":"viajes.py"})
    # Creamos la estructura del arbil a partir del elemento raiz
arbolhtml_c_p = etree.ElementTree (raizhtml_c_p)
    # Bucle para la obtención de los nombres y códigos de ciudades
for loc1 in provinciaspt:
    nombre_pro1 = loc1
    ciudad1 = arbolpt.xpath ("//region[@name='%s']/cities/city/@name" %nombre_pro1)
    codigo_prov1 = arbolpt.xpath ("//region[@name='%s']/@code" %nombre_pro1)
    for locb1 in codigo_prov1:
    # Se crean los grupos de zonas (se muestra el nombre como título)
        optgroup = etree.SubElement(raizhtml_c_p, "optgroup",attrib={"label":'%s'%loc1})
    # Se repite de nuevo el mismo elemento pero esta vez como opción, indicando
    # nombre y el valor que utiliza, añadimos la cadena '(todo)' a continuación
    # del nombre, ya que si se selecciona esta opción se busca en todo el grupo
        option = etree.SubElement(optgroup, "option", attrib={"value":'%s'%locb1})
        option.text = '%s'' (todo)' %loc1
    
    # Con este bucle se listan las localidades de cada zona
    for locc1 in ciudad1:
        nombre_loc1 = locc1
        codigo_loc1 = arbolpt.xpath ('//city[@name="%s"]/@code' %nombre_loc1)
        for locd1 in codigo_loc1:
            option = etree.SubElement(optgroup, "option", attrib={"value":'%s'%locd1})
            option.text = '%s' %locc1
            
    # Creamos el fichero 'ciudades_por.html' y le asignamos la variable 'ficheropt'
ficheropt = open('ciudades_por.html', 'w')
    # Escribimos el fichero con el contenido del arbol creado anteriormente
ficheropt.write(etree.tostring(arbolhtml_c_p,pretty_print=True))
    # Cerramos el fichero creado
ficheropt.close()
    # Se imprime un mensaje indicando el nombre del fichero creado
    # y que se ha terminado el proceso
print 'Resultados almacenados en el fichero "ciudades_por.html"','\n','\n','PROCESO TERMINADO'
