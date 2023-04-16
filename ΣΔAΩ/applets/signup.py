from flask import Markup as Mk


from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
import sys
sys.path.append(RESSOURCES)
from buttons import *


def signup(elem, method, form, args):
    elem['content'] = Mk(f"""       <section>
									<h3>Sign up</h3>
									
									<form method="post">
	
										<div class="row gtr-uniform">
	
											{logger("Username")}

											{breaker()}

											{pwd("Password2", "repeat password")}
	
											{submit("Sign up")}
										</div>
									</form>
								</section>""")
    return elem