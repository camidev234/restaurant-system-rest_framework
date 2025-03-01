## QuickDine

<details>
  <summary>Descripcion tecnica</summary>

  **QuickDine** es una plataforma de gestión de pedidos para restaurantes, diseñada para optimizar la interacción entre restaurantes, domiciliarios y clientes. Está implementada con un enfoque en el backend y una arquitectura escalable, permitiendo a los restaurantes gestionar su menú, domiciliarios y pedidos de manera eficiente a través de una API RESTful.

---

## Características clave:
- **Gestión de roles y permisos**:  
  El sistema maneja roles como **Domiciliarios**, **Clientes** y **Restaurantes**, cada uno con acceso restringido a ciertos endpoints. La validación de permisos se realiza mediante middleware, permitiendo configurar permisos globalmente para el sistema y adaptándose a necesidades específicas sin necesidad de modificar el código. De la misma manera, estos roles son configurables de manera que en el tiempo el nombre de los mismos puede cambiar e inclusive se podran crear nuevos; los roles que se configuren, tambien son globales para toda la plataforma.

- **Autenticación y seguridad**:  
  Implementación de autenticación basada en **JWT** para garantizar la seguridad de los endpoints, con un sistema de validación que verifica el acceso de los usuarios según su rol y los permisos asignados.

- **Gestión de pedidos**:  
  Los clientes pueden realizar pedidos desde el menú de cualquier restaurante registrado en la plataforma, con pagos gestionados a través de la integración con pasarelas de pago como **Openpay**. Los domiciliarios pueden visualizar y tomar los pedidos asignados, garantizando una gestión eficiente de la entrega.

- **Escalabilidad**:  
  El sistema permite agregar nuevos restaurantes, cada uno con su propio menú y domiciliarios, mientras que la configuración de roles y permisos se gestiona de manera centralizada para facilitar la administración y minimizar la complejidad.

---

## Tecnologías y Herramientas:
- **Django Rest Framework (DRF)**:  
  Para la creación de la API RESTful e implementación de la lógica de negocio.  

- **PostgreSQL**:  
  Base de datos relacional utilizada para almacenar datos de usuarios, restaurantes, pedidos, etc.  

- **Redis**:  
  Utilizado como backend para manejar conexiones **WebSocket** mediante **Django Channels**.  

- **WebSockets**:  
  Implementados para notificar en tiempo real a los clientes integrados con la API sobre cambios de estado en las órdenes (pedidos) y actualizaciones del estado de un pago asociado a una orden específica.  


- **Docker**:  
  Utilizado para contenerizar la aplicación y facilitar el despliegue en diferentes entornos.

- **Pasarela de Pago (Openpay)**:  
  Integración para procesar pagos de manera segura a través de **PSE**.

  ![Proceso de creacion de ordenes y pago por PSE](https://github.com/camidev234/restaurant-system-rest_framework/blob/master/procesopagopsejpeg.jpg?raw=true)

</details>


<details>
  <summary>Setup de la aplicacion</summary>
  -test
</details>



