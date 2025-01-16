# Quick-test
Technical test - Quick

# Proyecto de Prueba Técnica

Este proyecto esta enfocado a la administracion de los pedidos de un restaurante, ahora bien ademas incluye 
a grosso modo las siguientes funcionalidades:

- Gestion de tipologias de usuario
- Gestion de api url, estas son utiles para posteriormente poder asignar permisos a las tipologias de manera que la gestion de permisos sea granular en la medida que se requiera para cada tipologia de usuario.
- Asignacion y gestion de permisos y revocacion de estos.
- Creacion de usuarios, cada usuario puede o no estar asociados a un restaurante, esto para mantener la flexibilidad en casos de que un usuario tenga una tipologia por ejemplo "Administrador de sistema" que se encarga de configurar todo el flujo de los permisos para el aplicativo en general O un cliente que simplemente consula los restaurantes, menus y solicita pedidos.
- Gestion de restaurantes, estos se podran actualizar y quedar desactivados, cuando se desactiva un restaurante todos los usuarios asociados a este tambien.
- Gestion de menus, cada uno de estos asociado a un restaurante
- Gestion de categorias cada de los menus, estas tambien asociadas a los restaurantes 
- Gestion de pedidos en cuanto su creacion, consulta y cambios de estado.

**Como se menciono anteriormente, el acceso a cada funcionalidad dependera de la asignacion de permisos que se le hagan a las tipologias configuradas.**
**De la misma manera, un usuario al intentar acceder a un recurso el cual su tipologia no tiene acceso, se mostrara el correspondiente mensaje de error devuelto por API** 

Este proyecto está construido con **Django** y **Django REST Framework**, utilizando **PostgreSQL** como base de datos. A continuación, encontrará las instrucciones para configurarlo y ejecutarlo en su máquina local.

## Requisitos Previos

Antes de comenzar, asegúrese de tener instalado lo siguiente:

- **Python 3.8 o superior**
- **PostgreSQL**
- **Git** (opcional, pero recomendado para clonar el repositorio)

## Configuración Inicial

Siga los pasos a continuación para preparar el entorno del proyecto:

### 1. Clonar el repositorio

Primero, descargue el proyecto desde el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

### 2. Crear un entorno virtual

Se recomienda usar un entorno virtual para manejar las dependencias de forma aislada. Para crear uno, ejecute:

```bash
python -m venv venv
```

Luego, active el entorno virtual:

- En windows

```bash
venv\Scripts\activate
```

- En linux

```bash
source venv/bin/activate
```   

### 3. Instalar dependencias

Con el entorno virtual activado, instale las dependencias del proyecto ejecutando:

```bash
pip install -r requirements.txt
```
Si desea instalar las dependencias manualmente, puede ejecutar:

```bash
pip install djangorestframework==3.15.2
pip install djangorestframework_simplejwt==5.4.0
pip install psycopg2-binary==2.9.10
```
### 4. Configuración de la base de datos

Edite el archivo `settings.py` para configurar su base de datos. Por ejemplo, si está utilizando PostgreSQL, puede modificar los campos en la sección `DATABASES` como sigue:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_la_bd',
        'USER': 'usuario_de_la_bd',
        'PASSWORD': 'contraseña_de_la_bd',
        'HOST': 'localhost',
        'PORT': '5432',       
    }
}
```

### 5. Aplicación de migraciones y seeding inicial

#### Migraciones
Después de configurar la base de datos, aplique las migraciones necesarias para crear las tablas requeridas en la base de datos. Ejecute el siguiente comando:

```bash
python manage.py makemigrations
python manage.py migrate
```
**Seed inicial de datos**
1. Creación de tipologías y permisos preconfigurados **(recomendado)**
Si desea evitar la configuración manual de nuevas tipologías y permisos, puede ejecutar el siguiente comando. Esto generará:

- Todas las tipologías necesarias (en un contexto de un restaurante)
- Permisos predefinidos para cada tipologia en un contexto de negocio relacionado con restaurantes, esto incluye tipologias como:

- Administrador de sistema: encargado de configurar, tipologias, api urls y asignar o revocar permisos a las tipologias asi como de crear los restaurantes y administradores de restaurante y asociarlos a un restaurante
- Administrador de restaurante: Encargado de crear menu items, repartidores (dealer) e incativarlos, menus y categorias de los menu para su restaurante
- Repartidores: Ademas de que un admin de restaurante los puede crear, estos se pueden registrar por propia cuenta.
- Clientes: Tambien se pueden registrar por si mismos, ademas pueden consultar menus (solo podran visualizar menus activos, es decir que estan disponibles), solicitar pedidos. 

De esta manera al ejecutar este script, teniendo en cuenta que ya se cuenta con tipologias y permisos puede iniciar creando un restaurante y de ahi en adelante todo lo descrito anteriormente y de acuerdo a la documentacion de API.

```bash
python manage.py permissions_seed
```
**Opcional**
2. Creación de una tipología inicial y usuario administrador **(Ejecutar si prefiere no usar el primero que incluye ya permisos y demas)**
Ejecute el siguiente comando para crear:

- Una tipología llamada Admin.
- Un usuario inicial asociado a esta tipología.
- Permisos asignados a este usuario para que pueda crear nuevas tipologías, gestionar permisos y de ahi en adelante todo el proceso de crear menu items y demas.

```bash
python manage.py users_seed
```
3. Creacion de estados de los pedidos **(ejecutar este script es obligatorio)**:

```bash
python manage.py status_seed
```

## 6. Ejecutar servidor

Finalmente, levante el servidor local para probar el proyecto:

```bash
python manage.py runserver
```
Abra su navegador y acceda a http://127.0.0.1:8000.
