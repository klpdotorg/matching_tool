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
    	'/content/(.*)/(.*)/(.*)','content'
)

klp_students=None

queryvalues={"klpcode":"","klpname":"","studentcode":"","studentname":"","district":"","block":"","cluster":""}


class prints:
	def GET(SELF):
		return render.prints()

class index:
	def GET(SELF):
		return render.main()

class topframe:
	def GET(SELF):
		district_query = db1.query('select distinct b3.id,b3.name from school_match_found a, tb_institution s, tb_boundary b1, tb_boundary b2,tb_boundary b3 where a.klp_id=s.id and s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b3.name')
	
		block_query = db1.query('select distinct b2.id,b2.name,b2.parent_id from school_match_found a, tb_institution s, tb_boundary b1, tb_boundary b2,tb_boundary b3 where a.klp_id=s.id and s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b2.name')

		cluster_query = db1.query('select distinct b1.id,b1.name,b1.parent_id from school_match_found a, tb_institution s, tb_boundary b1, tb_boundary b2,tb_boundary b3 where a.klp_id=s.id and s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b1.name')
	
        	school_query = db1.query('select distinct a.klp_id as id,a.klp_school_name as name,b1.id as clust_id from school_match_found a, tb_institution s, tb_boundary b1, tb_boundary b2,tb_boundary b3 where a.klp_id=s.id and s.boundary_id = b1.id and s.active=2 and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by a.klp_school_name')
                
                ac_year = db1.query('select distinct b.klp_id,a.ayid,c.name from tb_sikshana_student_data a,school_match_found b,tb_academic_year c where a.school_code=cast(b.school_code as text) and a.ayid=c.id') 

		cls = db1.query('select distinct b.klp_id,a.class as cls from tb_sikshana_student_data a,school_match_found b where a.school_code=cast(b.school_code as text)')
		
		return render.topframe(district_query,block_query,cluster_query,school_query,ac_year,cls)

class content:
	def GET(SELF,sch,cls,ac_id):
		klp_students = [] 
		#if klp_students is None:
		
		klp_student=db1.query('select s_fewer.student_id,initcap(c.first_name) as first_name,c.middle_name,initcap(c.last_name) as last_name from (select distinct student_id from tb_schools_student_studentgrouprelation where student_group_id in ((select distinct id from tb_schools_studentgroup where institution_id=$name and name =\'7\' and group_type=\'Class\')) and academic_id=$aid) as s_fewer,tb_schools_child c,tb_schools_student s where s_fewer.student_id not in (select distinct klp_id from s_m_f) and s_fewer.student_id = s.id and s.child_id = c.id order by first_name',{"name":sch,"class":cls,"aid":ac_id})

		klp_students=[[row.student_id,row.first_name,row.middle_name,row.last_name] for row in klp_student]

		sikshana_student=db1.query('select distinct a.student_id,a.student_name from tb_sikshana_student_data a,school_match_found b where a.school_code=cast(b.school_code as text) and b.klp_id=$name and a.ayid=$aid and a.class=7 and a.student_id not in(select distinct student_id from s_m_f) order by a.student_name',{"name":sch,"class":cls,"aid":ac_id})
		
		sikshana_students=[[row.student_id,row.student_name] for row in sikshana_student]

		return render.display(klp_students,sikshana_students)


application = web.application(urls,globals()).wsgifunc()


class result:
    def POST(self):
	inputs=web.input()
	klp=''
	sikshana=''
	if str(inputs.sikshana_value1)!='' and str(inputs.klp_value1)!='':
		klp=str(inputs.klp_value1).split("&")
		sikshana=str(inputs.sikshana_value1).split("&")
		print klp
		print sikshana
		for i in range(1,len(klp)	):
			queryvalues["klpcode"]=str(klp[i]).split("|")[0]
			queryvalues["klpname"]=str(klp[i]).split("|")[1]
			queryvalues["studentcode"]=str(sikshana[i]).split("|")[0]
			queryvalues["studentname"]=str(sikshana[i]).split("|")[1]		
			db1.query('insert into s_m_f values($studentcode,$studentname,$klpcode,$klpname)',queryvalues)
	#return render.display()
        raise web.seeother('/content/'+str(inputs.matched_value).split("|")[0]+'/'+str(inputs.matched_value).split("|")[1]+'/'+str(inputs.matched_value).split("|")[2])


