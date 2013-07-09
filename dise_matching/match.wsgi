import socket
import csv
import web
import json

import sys, os,traceback
abspath = os.path.dirname(os.path.abspath(__file__))
#print abspath
if abspath not in sys.path:
	sys.path.append(abspath)
if abspath+'/templates' not in sys.path:
	sys.path.append(abspath+'/templates')

os.chdir(abspath)

render = web.template.render('templates/')


urls = (
	'/', 'index',
	'/match','result',
	'/topframe','topframe',
        '/content/(.*)/(.*)','content'
)


queryvalues={"disecode":"","disename":"","klpcode":"","klpname":"","district":"","block":"","cluster":""}


class prints:
	def GET(SELF):
		return render.prints()

class index:
	def GET(SELF):
		return render.main()

class topframe:
	def GET(SELF):
		
		fp1=csv.reader(open('/home/brijesh/matching_tool/dise_matching/data/DISE.csv','r'),delimiter='|')
		
		dise_district=[]
		dise_block=[]
		dise_cluster=[]

		schools=[row for row in fp1]
		for row in schools:
			if row[0] not in dise_district:
				dise_district.append(row[0])
		for row in schools:
			if [row[0],row[1]] not in dise_block:
				dise_block.append([row[0],row[1]])
		for row in schools:
			if [row[1],row[2]] not in dise_cluster:
				dise_cluster.append([row[1],row[2]])

		fp2=csv.reader(open('/home/brijesh/matching_tool/dise_matching/data/KLP.csv','r'),delimiter='|')

		klp_district=[]
		klp_block=[]
		klp_cluster=[]

		schools=[row for row in fp2]
		for row in schools:
			if row[0] not in klp_district:
				klp_district.append(row[0])
		for row in schools:
			if [row[0],row[1]] not in klp_block:
				klp_block.append([row[0],row[1]])
		for row in schools:
			if [row[1],row[2]] not in klp_cluster:
				klp_cluster.append([row[1],row[2]])

		return render.topframe(dise_district,dise_block,dise_cluster,klp_district,klp_block,klp_cluster)

class content:
	def GET(SELF,dise_cluster,klp_cluster):
			
		fp1=csv.reader(open('/home/brijesh/matching_tool/dise_matching/data/DISE.csv','r'),delimiter='|')
		dise_school_id=db1.query('select distinct dise_code from dise_match_found')
		dise_school_ids=[str(row.dise_code) for row in dise_school_id]
		dise_schools=[row for row in fp1 if row[2].strip() == dise_cluster.strip() and row[3].strip() not in dise_school_ids]

		fp2=csv.reader(open('/home/brijesh/matching_tool/dise_matching/data/KLP.csv','r'),delimiter='|')
		klp_school_id=db1.query('select distinct klp_code from dise_match_found')
		klp_school_ids=[str(row.klp_code) for row in klp_school_id]
		klp_schools=[row for row in fp2 if row[2].strip().upper() == klp_cluster.strip().upper() and row[3].strip() not in klp_school_ids]

		return render.content(dise_schools,klp_schools)

application = web.application(urls,globals()).wsgifunc()


class result:
    def POST(self):
	inputs=web.input()

	if str(inputs.dise_value)!='' and str(inputs.klp_value)!='':
		queryvalues["disecode"]=str(inputs.dise_value).split("|")[0]
		queryvalues["disename"]=str(inputs.dise_value).split("|")[1]
		queryvalues["klpcode"]=str(inputs.klp_value).split("|")[0]
		queryvalues["klpname"]=str(inputs.klp_value).split("|")[1]
		
		db1.query('insert into dise_match_found values($disecode,$disename,$klpcode,$klpname)',queryvalues)
	
        raise web.seeother('/content/'+str(inputs.matched_value).split("|")[0]+'/'+str(inputs.matched_value).split("|")[1])


