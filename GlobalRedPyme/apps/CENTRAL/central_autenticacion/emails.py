def emailCreacionUsuarioGeneral(empresaIfis, url):
    txt_content = f"""
                    Registro de Contraseña

                    Para completar su registro en el portal de la Cooperativa {empresaIfis.nombreEmpresa}
                    para acceder a su Línea de Crédito y realizar pagos a sus proveedores y/o empleados,
                    haga click en el siguiente enlace: {url}

                    Si al hacer click en el enlace anterior NO FUNCIONA, copie y pegue el siguiente enlace en una ventana del navegador: {url}

                    Atentamente,
                    {empresaIfis.nombreEmpresa}
            """
    html_content = f"""
            <html>
                <body>
                    <h1>Registro de Contraseña</h1>
                    <br>
                    <p>Para completar su registro en el portal de la Cooperativa {empresaIfis.nombreEmpresa}
                    para acceder a su Línea de Crédito y realizar pagos a sus proveedores y/o empleados, 
                    haga click en el siguiente enlace:  <a href='{url}'>ENLACE</a>
                    </p>
                    <br>
                    <p>
                    Si al hacer click en el enlace anterior NO FUNCIONA, copie y pegue el siguiente enlace en una ventana del navegador:
                     </p>
                    <br>
                    <p>{url}</p>
                    <br>
                    Atentamente,
                    <br>
                    <b>{empresaIfis.nombreEmpresa}</b>
                    <br>
                </body>
            </html>
            """
    return txt_content, html_content


def emailCreacionUsuarioCorp(empresaIfis, url, nombreUsuario, empresaCorp):
    txt_content = f"""
                    Estimad@ {nombreUsuario.nombres} {nombreUsuario.apellidos}

                    Su correo ha sido registrado para poder operar el portal Corp de la empresa {empresaCorp.nombreEmpresa}
                    Haga click en el siguiente {url} para completar su registro

                    Si al hacer click en el enlace anterior NO FUNCIONA, copie y pegue el siguiente enlace en una ventana del navegador: {url}

                    Atentamente,
                    {empresaIfis.nombreEmpresa}
            """
    html_content = f"""
            <html>
                <body>
                    <h1>Estimad@ {nombreUsuario.nombres} {nombreUsuario.apellidos}</h1>
                    <br>
                    <p>Su correo ha sido registrado para poder operar el portal Corp de la empresa {empresaCorp.nombreEmpresa}
                    Haga click en el siguiente <a href='{url}'>ENLACE</a> para completar su registro 
                    </p>
                    <br>
                    <p>
                    Si al hacer click en el enlace anterior NO FUNCIONA, copie y pegue el siguiente enlace en una ventana del navegador: 
                     </p>
                    <br>
                    <p>{url}</p>
                    <br>
                    Atentamente,
                    <br>
                    <b>{empresaIfis.nombreEmpresa}</b>
                    <br>
                </body>
            </html>
            """
    return txt_content, html_content
