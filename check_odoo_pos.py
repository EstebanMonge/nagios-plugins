#!/usr/bin/env python

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

# Funcion para obtener los datos de las sesiones del POS
    def sessionRead(self, session_id):
        odoo_filter = [[("id", "=", session_id)]]
        result = self.ODOO_OBJECT.execute_kw(
            self.DATA
            , self.UID
            , self.PASS
            , 'pos.session'
            , 'read'
            , [session_id]
            , {"fields": ["config_id","user_id","start_at"]})
        return result

# Funcion para obtener las facturas segun estado
    def sessionCheck(self, stateSession):
        odoo_filter = [[("state", "!=", stateSession)]]
        session_id = self.ODOO_OBJECT.execute_kw(
            self.DATA
            , self.UID
            , self.PASS
            , 'pos.session'
            , 'search'
            , odoo_filter)
        return session_id
    def help(self):
        print 'Usage: check_odoo_fe.py -d database -m mail -s password -p port -u url'

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
    session_id = od.sessionCheck("closed")

    # Leer detalles de las sesiones
    result = od.sessionRead(session_id)
    print(result)

if __name__ == '__main__':
    main(sys.argv[1:])
