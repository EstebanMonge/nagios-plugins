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
            , {"fields": ["date_invoice","partner_id","sequence"]})
        return result

# Funcion para obtener las facturas segun estado
    def invoiceCheck(self, stateTributacion,invoiceDate):
        odoo_filter = [[("state_tributacion", "=", stateTributacion),("date_invoice","=",invoiceDate)]]
        invoice_id = self.ODOO_OBJECT.execute_kw(
            self.DATA
            , self.UID
            , self.PASS
            , 'account.invoice'
            , 'search'
            , odoo_filter)
        return invoice_id
    def help(self):
        print('Usage: check_odoo_fe.py -d database -m mail -s password -p port -u url -i invoiceState')
        sys.exit(3)

def main(argv):
    od = Odoo()

# Si no estan todos los argumentos salir
    if len(sys.argv) < 10:
       od.help()
    try:
       opts,args=getopt.getopt(argv,"hd:m:s:p:u:i:")
    except getopt.GetoptError:
       od.help()

# Obtener todos los argumentos
    invoiceState = 'rechazado'
    for opt, arg in opts:
        if opt == '-h':
            od.help()
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
        elif opt == '-i':
            invoiceState = arg

    od.authenticateOdoo(database,mail,secret,port,url)

    # Buscar las facturase segun estado y fecha
    yesterday = datetime.date.today() - datetime.timedelta(days = 1)
    invoice_id = od.invoiceCheck(invoiceState,yesterday.strftime('%Y-%m-%d'))

    # Leer detalle de facturas
    if len(invoice_id) == 0:
        print('Pura vida! No invoices in state '+invoiceState+' was found')
        sys.exit(0)
    else:
        result = od.invoiceRead(invoice_id)
        print('You have '+str(len(invoice_id))+' invoices '+invoiceState+' from Hacienda yesterday')
        for x in result:
            print('Consectutive: '+str(x['sequence'])+'. Client: '+str(x['partner_id'][1])+'. Date: '+str(x['date_invoice']))
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])
