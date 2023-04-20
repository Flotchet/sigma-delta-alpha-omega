from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
ADMINPANELRESSOURCES = join(BASEDIR, 'admin_panel_ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(ADMINPANELRESSOURCES)
sys.path.append(BASEDIR)
sys.path.append(BASEDIR)
from buttons import * # type: ignore 
from attributions_changer import * # type: ignore 
from home import home

def churnprediction(elem, method, form, args):

	#make a connection to the database
	engine = sql.create_engine('sqlite:///' + join(BASEDIR, 'databases/users.db'))
	conn = engine.connect()

	users = get_all_usr(conn) # type: ignore
	#remove the current user from the list
	users = [user for user in users if user[0] != elem['_usr']] # type: ignore
	dtlst = datalist("users", [user[0] for user in users], "usr") # type: ignore


	toadd = ""
	if method == 'POST':
		
		user = form['users']
		attr = form['attr']
		change_attr_lvl(user, attr, conn) # type: ignore
		
		
		toadd = Mk(f"""<div class="row gtr-uniform">
							<div class="col-12">
								<h3>Attribution changed</h3>
							</div>
						</div>""")
		
		if attr == "0":
			toadd = Mk(f"""<div class="row gtr-uniform">
							<div class="col-12">
								<h3>User deleted</h3>
							</div>
						</div>""")
								

   	#close 
	conn.close()

	elem['content'] = Mk(f"""   <section>
									<h3>Admin panel</h3>
									
									<form method="post">
	
										<div class="row gtr-uniform">
	
											{dtlst} 
											
											{selector_inc("attr",["None", "User", "Employee", "Admin", "Super User"], "Attribution")}
										
	
											{submit("Submit")}
										</div>
									</form>
								</section>""") + toadd 
	
	return elem