from flask import Markup as Mk
from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(BASEDIR)
from buttons import * # type: ignore 
from home import home

def logout(elem, method, form, args):

	if method == 'POST':
		elem['_attr_lvl'] = 0
		elem['_usr'] = ""
    
	elem['content'] = Mk(f"""<div class="inner">
								<section>
									<h3>See you around!</h3>									
								</section>
	
								<section>
									<form method="post" >
										{postbtn("Log out", "button primary fit")}
									</form>
								</div>
								</section>

								<section>
									<br>
								</section>""")
	return elem