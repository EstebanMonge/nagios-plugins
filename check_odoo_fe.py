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

# Funcion para obtener los datos de las facturas
    def invoiceRead(self, invoice_id):
        odoo_filter = [[("id", "=", invoice_id)]]
        result = self.ODOO_OBJECT.execute_kw(
            self.DATA
            , self.UID
            , self.PASS
            , 'account.invoice'
            , 'read'
            , [invoice_id]
            , {"fields": ["date_invoice","number","partner_id","sequence"]})
        return result

# Funcion para obtener las facturas segun estado
    def invoiceCheck(self, stateTributacion):
        odoo_filter = [[("state_tributacion", "=", stateTributacion)]]
        invoice_id = self.ODOO_OBJECT.execute_kw(
            self.DATA
            , self.UID
            , self.PASS
            , 'account.invoice'
            , 'search'
            , odoo_filter)
        return invoice_id
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

# Obtener todos los argumentos
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

    # Buscar las facturase segun estado
    invoice_id = od.invoiceCheck("rechazado")

    # Leer detalle de facturas
    result = od.invoiceRead(invoice_id)
    print(result)

if __name__ == '__main__':
    main(sys.argv[1:])
