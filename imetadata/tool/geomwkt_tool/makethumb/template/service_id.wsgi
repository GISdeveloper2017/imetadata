#coding=utf-8
import random
import memcache
import urlparse
import urllib
from cgi import parse_qs, escape
import logging
import psycopg2 as pg
from mapproxy.wsgiapp import make_wsgi_app
import os.path
import traceback

class GeocubeAuthFilter(object):

    def __init__(self, app, global_conf):
        self.app = app
        self.global_conf = global_conf

    def __call__(self, environ, start_response):
        # auth check and visit check
        request_uri = environ[ "REQUEST_URI" ]
        query_string = environ[ "QUERY_STRING" ]
		
        if "/demo" in request_uri:
            return self.app(environ, start_response)	
	  
	  
        # d = parse_qs(query_string)
        # token = d.get('token', [''])[0]
        # **************************************
        try:
            mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        except Exception,e:   
            logging.debug("Exception&&&&&&&&&&&&&&&&&&& init memcached faild.")
            logging.debug(Exception)
            logging.debug(e)

        d2 = request_uri.split("/")

        logging.debug("request_uri:" + request_uri)# log

        token = d2[2]
        logging.debug("token:" + token)# log
        environ[ "REQUEST_URI" ] = environ[ "REQUEST_URI" ].replace('/' + token + '/','/')
        environ[ "PATH_INFO" ] = environ[ "PATH_INFO" ].replace('/' + token + '/','/')
        environ[ "PATH_TRANSLATED" ] = environ[ "PATH_TRANSLATED" ].replace('/' + token + '/','/')
        environ[ "mod_wsgi.path_info" ] = environ[ "mod_wsgi.path_info" ].replace('/' + token + '/','/')
        environ[ "mapproxy.token" ] = token

        # get service address
        serviceAddr = request_uri.replace(query_string,"")
        serviceAddr = serviceAddr.replace('/' + token + '/','/')

        logging.debug("serviceAddr: unprocessed ::" + serviceAddr)# log

        serviceAddr = serviceAddr.lstrip("/")
        lst = serviceAddr.split('/')
        lst2 = lst[0:2]
        serviceAddr = "/".join(lst2)
        
        logging.debug("serviceAddr:   processed ::" + serviceAddr)# log

        initTag = mc.get("InitMem")
        #if not initTag:
        if False:		
            logging.debug("not initTag: ::" + serviceAddr)# log
            global conn
            global dbcur
            try:
                dbName = dbConfig.get("database")
                userName = dbConfig.get("user")
                passwd = dbConfig.get("password")
                hostIP = dbConfig.get("host")
                portID = dbConfig.get("port")
                conn = pg.connect(database=dbName, user=userName, password=passwd, host=hostIP, port=portID)
                dbcur = conn.cursor()
                sqlGet = "select * from ac_token"
                dbcur.execute(sqlGet)
                obj = dbcur.fetchall()
                for val in obj:
                    subKey = val[2] + "@" + val[3]
                    authKey = "Auth_" + subKey
                    countKey = "Count_" + subKey
                    address = val[3]
                    reqCount = val[5]
                    mc.set(authKey,address)
                    mc.set(countKey,reqCount)
                # set init tag
                mc.set("InitMem","Yes")
                
            except Exception,e:   
                logging.debug("Exception&&&&&&&&&&&&&&&&&&& init memcached faild.")
                logging.debug(Exception)
                logging.debug(e)
            finally:
                logging.debug("finally Tag: ::" )# log
                #close dbConnection
                if 'dbcur' in dir():
                    dbcur.close()
                if 'conn' in dir():
                    conn.close()               
            logging.debug("Init Coverage postgres Connection Successfull..." )   # log
        # auth
        tokenAuthKey = 'Auth_' + token + "@" + serviceAddr
        tokenCountKey = 'Count_' + token + "@" + serviceAddr
        authAddress = mc.get(tokenAuthKey)
        if not authAddress:
            logging.debug("authAddress is None,tokenAuthKey is :"+tokenAuthKey)

#        if authAddress == serviceAddr:
        if 1 == 1:
            # full auth
            logging.debug("auth yes: ::" + serviceAddr)# log
            #logging.debug("tokenAuthKey is: "+ tokenAuthKey +" && authAddress is: " + authAddress+" && serviceAddr is :" + serviceAddr)# log
            mc.incr(tokenCountKey)
            
            #close memcached connection,it's important!!
            #mc.servers[0].send_cmd('quit')
            
            return self.app(environ, start_response)
        else:
            # none auth
            logging.debug("auth no")# log
            status = '200 OK'
            headers = [('Content-type', 'image/png')]

            #close memcached connection,it's important!!
            #mc.servers[0].send_cmd('quit')

            start_response(status, headers)
            return open(self.global_conf.get('data_path')+'None.png', 'rb').read()#0000-noauth




logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='$log_file$',filemode='w')       #/home/qld/local/qld_wsgi/qld_WSGI_scene_2017.log

#connection string  'database="user_auth", user="postgres", password="postgres", host="127.0.0.1", port="5432"'
dbConfig = {"database":"qld", "user":"postgres", "password":"cube$pgs", "host":"127.0.0.1", "port":"5432"}
#dbConfig = {"database":"qld", "user":"postgres", "password":"postgres", "host":"172.172.9.250", "port":"5432"}

config = {'map_path': '/home/geocube/map/','data_path': '/home/extendStore/OriImages','uLimit' : 10000 }           
application = make_wsgi_app('$yaml_file$', reloader=True)                                                                      #/home/qld/local/qld_mapproxy/qld_mosaic2017_scene.yaml
application = GeocubeAuthFilter(application,config)