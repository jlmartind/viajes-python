#!/usr/bin/python
# -*- coding:utf-8 -*-
from lxml import etree
import urllib2,sys,urllib
import cgi
import cgitb

cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers  

form = cgi.FieldStorage()

print '<link rel="shortcut icon" href="http://localhost/images/favicon.ico">'

print "<head>"
print "<title>Viajes Portofino</title>"
print '<link rel="StyleSheet" href="http://localhost/style/style.css" type="text/css" media="screen"/>'
print "</head>"

print "<body>"
print '<img src="http://localhost/images/logo-agencia2.jpg"></img><br /><br />'

# Lectura de credenciales desde fichero 'cuentas.cfg'
# *********************************************************

    # Abrimos el fichero que contiene las credenciales de información estática
ficherocs = open ('cuentas.cfg','r')

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

URL = direccion[0]


# Adquisición de datos desde el formulario html
#**********************************************

# Asignamos variables python a las variables del formulario
v_pais = form["pais"].value
v_area = form["area"].value
v_region = form["region"].value
v_ciudad = form["ciudad"].value
v_regimen = form["regimen"].value
v_alojamiento = form["alojamiento"].value
v_habitaciones = form["habitaciones"].value
v_adultos = form["adultos"].value

# Comprobación de que al menos uno de los valores de zona se ha introducido
if v_area == v_region == v_ciudad == 'vacio':
    print "<H1>Error</H1>"
    print "<p> "
    print "<H2>Por favor rellene los campos área, región o ciudad.</H2>"
    print "<p> "
    
else:
    print "<p>pais: ", v_pais, ",  area: ", v_area, ",  region:", v_region, ",  ciudad: ", v_ciudad
    print "<p>regimen: ", v_regimen, ", alojamiento: ", v_alojamiento, 
    print "<p>habitaciones: ", v_habitaciones, ", adultos: ", v_adultos
    print "<p> "
#print "<p>nino1:", form["nino1"].value
#print "<p>nino2:", form["nino2"].value
#print "<p>nino3:", form["nino3"].value
#print "<p>nino4:", form["nino4"].value
#print "<p>nino5:", form["nino5"].value

#Sustituimos las variables con valor 'vacio' (que no reconoce la solicitud) por ''
if v_area == 'vacio':
    v_area = ''
    
if v_region == 'vacio':
    v_region = ''

if v_ciudad == 'vacio':
    v_ciudad = ''

print "<p>pais: ", v_pais, ",  area: ", v_area, ",  region:", v_region, ",  ciudad: ", v_ciudad

print "<p> "

if v_area != v_region != v_ciudad and v_region != v_area != v_ciudad:
    print "<H1>Error</H1>"
    print "<p> "
    print "<H2>Por favor rellene sólo uno de los campos área, región o ciudad.</H2>"
    print "<p> "
else:
    print ",  area: ", v_area, ",  region:", v_region, ",  ciudad: ", v_ciudad
    print "<p> "


# Prueba de conexión con el servidor, nos indica si ha podido conectar o no
#**************************************************************************

try:
    urllib.urlopen(URL).read()
    print "Conectado al servidor",'\n'
    print "<p> "
except:
    print "No es posible conectar con el servidor",'\n'
    print "<p> "
    sys.exit(1)
 
 
# Creación de la estructura XML de la petición 
#***********************************************

# Indicamos el elemento raiz de petición con los atributos 'type',
    # 'version' y 'sessionId' 
raizpeticion = etree.Element("request", \
    attrib={"type":"ACCOMMODATIONS_AVAIL","version":"4.1","sessionId":"5551123"})
    # Creamos la estructura del arbol a partir del elemento raiz
arbolpeticion = etree.ElementTree (raizpeticion)
    # Definimos el primer hijo del elemento raiz, es cliente y tiene
    # atributos 'code','branch' y 'password'
cliente = etree.SubElement(raizpeticion,"client",\
    attrib={"code":"%s" %usuario[0], "branch":"%s" %sucursal[0], "password":"%s" %clave[0]})
    # Definimos el segundo hijo del raiz, es lenguaje y tiene el atributo 'code'
lenguaje = etree.SubElement(raizpeticion,"languaje", attrib={"code":"SPA"})
    # Definimos el tercer hijo del raiz, es criterio_b y contiene más elementos
criterio_b = etree.SubElement(raizpeticion,"searchCriteria")
    # Definimos los hijos de criterio_b, son criterio y todos tienen los atributos
    # 'type', 'code' y 'value', cambia el valor de 'code'
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"0", "code":"country", "value":"%s" %v_pais})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"0", "code":"area", "value":"%s" %v_area})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"0", "code":"region", "value":"%s" %v_region})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"0", "code":"city", "value":"%s" %v_ciudad})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"1", "code":"accommodationCode", "value":""})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"1", "code":"accommodationType", "value":"0"})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"1", "code":"category", "value":""})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"2", "code":"priceType", "value":"3"})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"2", "code":"offer", "value":""})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"2", "code":"concept", "value":""})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"2", "code":"board", "value":""})
criterio = etree.SubElement(criterio_b,"criterion", \
    attrib={"type":"2", "code":"cancelPolicies", "value":"1"})
    # Definimos el cuarto hijo del elemento raiz, es periodo y tiene los 
    # atributos de inicio > start y fin > end
periodo = etree.SubElement(raizpeticion, "period", \
    attrib={"start":"20120612", "end":"20120613"})
    # Definimos el quinto hijo del raiz, es rooms contiene los elementos de la estancia
habitaciones = etree.SubElement(raizpeticion, "rooms")
    # Definimos el primer hijo de rooms
habitacion = etree.SubElement(habitaciones, "room", \
    attrib={"type":"1", "adults":"2", "children":"0"})
habitacion = etree.SubElement(habitaciones, "room", \
    attrib={"type":"2", "adults":"2", "children":"0"})

pet_xml = etree.tostring(arbolpeticion,pretty_print=True)

#pet_xml = open('peticion6.xml','r')

#f = open("peticion.xml","w")
#f.write(pet_xml)
#f.close()
#print pet_xml

#parameter = urllib.urlencode({'XML':pet_xml})
#response = urllib.urlopen(URL, parameter)
#result = response.read()

opener = urllib2.build_opener()
opener.addheaders = [('Accept', 'application/xml'),
                    ('User-Agent', 'Python-urllib/2.6')]


req = urllib2.Request(url=URL, data= pet_xml,
                      headers={'Content-Type': 'application/xml','language' : 'Python'})

#req = urllib2.Request(url=URL, data=pet_xml)
assert req.get_method() == 'POST'


#values = {'name' : 'Michael Foord',
#          'location' : 'Northampton',
#          'language' : 'Python' }
#
#data = urllib.urlencode(values)
#req = urllib2.Request(url, data)
#response = urllib2.urlopen(req)
#the_page = response.read()



response = opener.open(req)
print 'Respuesta del servidor',response.code
print "<p> "

#opener = urllib2.build_opener()
#opener.addheaders = [('Accept', 'application/xml'),
#                     ('Content-Type', 'application/xml'),
#                     ('User-Agent', 'Python-urllib/2.6')]
#
#req = urllib2.Request(url=URL, data=pet_xml)
#assert req.get_method() == 'POST'
#
#response = opener.open(req)
# 
#respuesta = etree.fromstring(req)
print response.read()

#print etree.tostring(respuesta,pretty_print=True)
print "<p> "
print '<a href="http://localhost/index.html"><img src="http://localhost/images/atras.jpg" alt=""/> </a><br />Volver<br />'

print "</body>"