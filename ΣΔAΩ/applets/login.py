from flask import Markup as Mk


from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
import sys
sys.path.append(RESSOURCES)
from buttons import *


def login(elem, method, form, args):
    elem['content'] = Mk(f"""       <section>
									<h3>Log In</h3>
									
									<form method="post" >
	
										<div class="row gtr-uniform">
	
											{logger("username")}
										
	
											{submit("Log In")}
										</div>
									</form>
								</section>""")
    return elem