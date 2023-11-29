import OpenSSL.crypto


def usuarioPropietarioFirma(p12_file, password, rucEmpresa):
    """
    Este metodo sirve para verificar la firma electronica
    @type rucEmpresa: REcibe el ruc de la empresa
    @type password: REcibe la contraseña de la firma electronica
    @type p12_file: REcibe el archivo
    @rtype: Devuelve verdarero o falso
    """
    # Ruta al archivo PKCS#12 (.p12 o .pfx)
    # p12_file = '/Users/papamacone/Documents/Edgar/grp-back-coop/GlobalRedPyme/6194645_identity (1).p12'

    # Contraseña del archivo PKCS#12
    # password = '1754188066E*22'

    try:
        p12 = OpenSSL.crypto.load_pkcs12(p12_file.read(), password)

        # Obtiene el certificado del archivo PKCS#12
        cert = p12.get_certificate()

        # Obtiene el propietario del certificado
        if cert.get_subject().organizationIdentifier:
            propietario = cert.get_subject().organizationIdentifier[6:]

            # Imprime el propietario
            print('Propietario:', propietario)
            print('rucEmpresa:', rucEmpresa)

            return True if rucEmpresa == propietario else False

        return False
    except Exception as e:
        return False
