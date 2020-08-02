# SDRD API


## Para instalar las librerias
```
pip install -r requirements.txt
```

## Base de datos
Para obtener la base de datos, abrir con mysqlworkbench el modelo modelo_sdrd, luego en la pestaña database con la opción Reverse Engineer... crean la base de datos, luego ejecutan los scripts en el archivos sql.txt

## Para iniciar
```
python app.py
```

## USO

### Pacientes

REGISTRAR PACIENTE ->Petición POST
http://127.0.0.1:5000/pacientes
body JSON
{
    "idpaciente":"81269138",
    "nombres":"Ana María",
    "apellidos":"Roca Cusy",
    "dni":"81269138",
    "direccion":"urb piramide 116 campoy",
    "telefono":"984421516"
}

OBTENER PACIENTES ->Petición GET
http://127.0.0.1:5000/pacientes

OBTENER PACIENTE ->Petición GET
http://127.0.0.1:5000/pacientes/<id>
http://127.0.0.1:5000/pacientes/71260558

ACTUALIZAR PACIENTE ->Petición PUT
http://127.0.0.1:5000/pacientes/<idpaciente>
http://127.0.0.1:5000/pacientes/81269138
body JSON
{
    "nombres":"Ana María",
    "apellidos":"Roca Rivas",
    "direccion":"urb piramide 116, Campoy"
}

BUSCAR PACIENTES POR NOMBRES,APELLIDOS,ID->Petición GET
http://127.0.0.1:5000/pacientes/busqueda/<texto>
http://127.0.0.1:5000/pacientes/busqueda/<Ana>


### Diagnosticos

REGISTRAR DIAGNOSTICO ->Petición POST
http://127.0.0.1:5000/diagnosticos
body JSON
{
    "rutaimagen":"https:www.....com",
    "diagnostico":"RD_Heavy",
    "observaciones":"El paciente está enfermo",
    "idpaciente":"81269138",
    "idusuario":1
}

OBTENER DIAGNOSTICOS ->Petición GET
http://127.0.0.1:5000/diagnosticos

OBTENER DIAGNOSTICO ->Petición GET
http://127.0.0.1:5000/diagnosticos/<iddiagnostico>
http://127.0.0.1:5000/diagnosticos/1


OBTENER DIAGNOSTICO PACIENTE ->Petición GET
http://127.0.0.1:5000/diagnosticos/paciente/<idpaciente>
http://127.0.0.1:5000/diagnosticos/paciente/81269138
