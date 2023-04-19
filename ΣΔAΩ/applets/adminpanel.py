from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
LOGINRESSOURCES = join(BASEDIR, 'login_ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(LOGINRESSOURCES)
sys.path.append(BASEDIR)
from buttons import * # type: ignore 
from check_user import * # type: ignore 
from home import home

def adminpanel(elem, method, form, args):

	toadd = ""
	if method == 'POST':
		
		pass	
		
   
	elem['content'] = Mk(f"""   <section>
									<h3>Admin panel</h3>
									
									<form method="post">
	
										<div class="row gtr-uniform">
	
											{txt("id", "Username")} 
											
											{selector_inc("attr",["None", "User", "Employee", "Admin", "Super User"], "Attribution")}
										
	
											{submit("Log In")}
										</div>
									</form>
								</section>""") + toadd 
	
	return elem