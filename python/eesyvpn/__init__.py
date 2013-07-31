# -*- coding: utf-8 -*-

import subprocess
import csv
from datetime import datetime
import re
import logging

_eesyvpn_bin = "/usr/sbin/eesyvpn"
_eesyvpn_ca_home = "/etc/openvpn/ca"

class EesyvpnException(Exception):
	def __init__(self, code=None, stdout=None,stderr=None):
		self.code = code
		self.stdout = stdout
		self.stderr = stderr

	def __str__(self):
		return "EesyVPN return error (code : %s)\n\n%s\n\n%s" % (self.code,self.stdout,self.stderr)

def eesyvpn(cmd=""):
	cmd = subprocess.Popen('%s %s' % (_eesyvpn_bin,cmd),shell=True,  stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	return [cmd.wait(),cmd.stdout.read(),cmd.stderr.read()]

def listCerts(type=None,state=None):
	code,ret,err = eesyvpn('list --csv')
	l={}
	for row in csv.reader(ret.split('\n'),delimiter=';',quotechar="'"):
		if len(row)!=6:
			continue
		if type is not None and type!=row[3]:
			continue
		if state is not None and state!=row[2]:
			continue
		l[row[0]]={
			'id':     row[0],
			'name':   row[1],
			'state':  row[2],
			'type':   row[3],
			'expire': str2date(date=row[4]),
			'revoke': str2date(date=row[5])
		}
	return l

def listValidCerts(type=None):
	l=listCerts(type=type,state='V')
	r={}
	for i in l:
		if l[i]['expire']>datetime.now():
			r[l[i]['name']]=l[i]
	return r

def listRevokedCerts(type=None):
	l=listCerts(type=type,state='R')
	r={}
	for i in l:
		if l[i]['name'] not in r:
			r[l[i]['name']]=[]
		r[l[i]['name']].append(l[i])
	return r


def str2date(date=None):
	if not date or date == "":
		return None
	return datetime.strptime(date,'%Y/%m/%d %H:%M:%S')

def is_valid_name(name):
	return re.match('^[0-9a-zA-Z\.\-\_]*$',name)

def simpleAction(action,name):
	if not is_valid_name(name):
		logging.error('Invalid name')
		return False

	code,ret,err = eesyvpn('%s %s' % (action,name))

	if code == 0:
		return True
	else:
		raise EesyvpnException(code,ret,err)
		return False

def create(name):
	return simpleAction('create',name)

def recreate(name):
	return simpleAction('recreate',name)

def renew(name):
	return simpleAction('renew',name)

def revoke(name):
	return simpleAction('revoke',name)

def updateConfig(name):
	if simpleAction('makeconf',name):
		return simpleAction('makezipconf',name)
	return False

def view(i):
	code,ret,err = eesyvpn('view %s' % i)
	if code==0:
		return ret

def nameById(i):
	code,ret,err = eesyvpn('namebyid %s' % i)
	if code==0:
		return ret.rstrip()

def getZipConfig(name):
	if not is_valid_name(name):
		return
	f='%s/openvpn/clients-zip/%s.zip' % (_eesyvpn_ca_home,name)
	try:
		fd=open(f,'r')
		ret=fd.read()
		fd.close()
		return ret
	except Exception, e:
		logging.error('Failed to read Zip file %s ; %s' % (f,e))
		return

