from flask import Markup as Mk


def logout(elem, method, form, args):
    elem['content'] = Mk("""<div class="inner">
								<section>
									<h3>See you around!</h3>

									
								</section>
	
								<section>
									<div class="row gtr-uniform">
									<ul class="actions fit">
											<li><a href="/home" class="button fit icon solid fa-home">Home</a></li>
									</ul>
								</div>
								</section>

								<section>
									<br>
								</section>""")
    return elem