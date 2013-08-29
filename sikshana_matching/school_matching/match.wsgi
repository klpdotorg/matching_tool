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
db1=web.database(dbn='postgres',user='',pw='',db='')
db2=web.database(dbn='postgres',user='',pw='',db='')

urls = (
	'/', 'index',
	'/match','result',
	'/topframe','topframe',
        '/content/(.*)/(.*)','content'
)


queryvalues={"klpcode":"","klpname":"","schoolcode":"","schoolname":"","district":"","block":"","cluster":""}


class prints:
	def GET(SELF):
		return render.prints()

class index:
	def GET(SELF):
		return render.main()

class topframe:
	def GET(SELF):
		district_query = db2.query('select distinct cast(b3.id as text),b3.name from tb_institution s, tb_boundary b1, tb_boundary b2,tb_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b3.name')
	
		block_query = db2.query('select distinct cast(b2.id as text),b2.name,b2.parent_id from tb_institution s, tb_boundary b1, tb_boundary b2,tb_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b2.name')

		cluster_query = db2.query('select distinct cast(b1.id as text),b1.name,b1.parent_id from tb_institution s, tb_boundary b1, tb_boundary b2,tb_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b1.name')
		
		sikshana_district = db2.query('select distinct district from tb_sikshana_school_data order by district')

		sikshana_block = db2.query('select distinct district,block from tb_sikshana_school_data order by district,block') 

		sikshana_cluster = db2.query('select distinct block,cluster from tb_sikshana_school_data order by block,cluster')

		return render.topframe(district_query,block_query,cluster_query,sikshana_district,sikshana_block,sikshana_cluster)

class content:
	def GET(SELF,klp_cluster_id,sikshana_cluster_id):

		klp_school = db2.query('select cast(s.id as text) as school_code,s.name as school_name from tb_institution s, tb_boundary b1, tb_boundary b2,tb_boundary b3 where s.boundary_id = b1.id and s.active=2 and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.boundary_type_id=1 and b3.boundary_category_id=9 and s.id not in (select distinct klp_id from school_match_found) and cast(b1.id as text)=''$name'' order by s.name',{"name":klp_cluster_id})
	
		sik_school = db2.query('select distinct a.school_code,a.school_name,cluster,block,district from tb_sikshana_school_data a,school_match_found b where a.school_code != cast(b.school_code as text) order by school_code,school_name')
		
		klp_schools=[[row.school_code,row.school_name] for row in klp_school]
		sik_schools=[[row.school_code,row.school_name] for row in sik_school if row.cluster.strip().upper() == sikshana_cluster_id.strip().upper()]
	
		return render.content(klp_schools,sik_schools)

application = web.application(urls,globals()).wsgifunc()


class result:
    def POST(self):
	inputs=web.input()

	if str(inputs.klp_value)!='' and str(inputs.sikshana_value)!='':
		queryvalues["klpcode"]=str(inputs.klp_value).split("|")[0]
		queryvalues["klpname"]=str(inputs.klp_value).split("|")[1]
		queryvalues["schoolcode"]=str(inputs.sikshana_value).split("|")[0]
		queryvalues["schoolname"]=str(inputs.sikshana_value).split("|")[1]
		
		db2.query('insert into school_match_found values($klpcode,$klpname,$schoolcode,$schoolname)',queryvalues)
	
        raise web.seeother('/content/'+str(inputs.matched_value).split("|")[0]+'/'+str(inputs.matched_value).split("|")[1])
