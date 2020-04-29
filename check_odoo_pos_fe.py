#!/usr/bin/env python3

import xmlrpc.client
import datetime
import sys
import getopt

class Odoo():

# Funcion para autenticar en odoo
    def authenticateOdoo(self,database,mail,secret,port,url):
        self.DATA = database # db name
        self.USER = mail # email address
        self.PASS = secret # password
        self.PORT = port # port
        self.URL  = url # base url
        self.URL_COMMON = "{}:{}/xmlrpc/2/common".format(
            self.URL, self.PORT)
        self.URL_OBJECT = "{}:{}/xmlrpc/2/object".format(
            self.URL, self.PORT)

        self.ODOO_COMMON = xmlrpc.client.ServerProxy(self.URL_COMMON)
        self.ODOO_OBJECT = xmlrpc.client.ServerProxy(self.URL_OBJECT)
        self.UID = self.ODOO_COMMON.authenticate(
            self.DATA
            , self.USER
            , self.PASS
            , {})

# Funcion para obtener las ordenes del pos segun estado
    def posorderCheck(self, stateOrder):
        odoo_filter = [[("state_tributacion", '=', False)]]
#        odoo_filter = [[("state_tributacion", '!=', 'aceptado'),("state_tributacion", '!=', 'rechazado'),("state_tributacion", '!=', 'no_aplica'),("state_tributacion", '!=', 'error'),("state_tributacion", '!=', 'rejected'),("state_tributacion", '!=', 'no_encontrado'),("state_tributacion", '!=', 'firma_invalida'),("state_tributacion", '!=', 'procesando'),("state_tributacion", '!=', 'invalido')]]
        posorder_id = self.ODOO_OBJECT.execute_kw(
            self.DATA
	    , self.UID
	    , self.PASS
            , 'pos.order'
            , 'search'
            , odoo_filter)
        return len(posorder_id)
    def help(self):
        print('Usage: check_odoo_fe.py -d database -m mail -s password -p port -u url')

def main(argv):
    od = Odoo()

# Si no estan todos los argumentos salir
    if len(sys.argv) < 10:
       od.help()
       sys.exit(2)
    try:
       opts,args=getopt.getopt(argv,"hd:m:s:p:u:")
    except getopt.GetoptError:
       od.help()
       sys.exit(2)

# Obtener argumentos
    for opt, arg in opts:
        if opt == '-h':
            od.help()
            sys.exit(2)
        elif opt == '-d':
            database = arg
        elif opt == '-m':
            mail = arg
        elif opt == '-s':
            secret = arg
        elif opt == '-p':
            port = arg
        elif opt == '-u':
            url = arg

    od.authenticateOdoo(database,mail,secret,port,url)

    # Buscar sesion
    posorder_id = od.posorderCheck("closed")
    # Leer detalles de las sesiones
    if posorder_id == 0:
       print('OK - You have '+str(posorder_id)+' orders without Hacienda state')
       sys.exit(0)
    else:
       print('CRITICAL - You have '+str(posorder_id)+' orders without Hacienda state')
       sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])
