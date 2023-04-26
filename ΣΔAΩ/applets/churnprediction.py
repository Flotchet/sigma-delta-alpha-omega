from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
CHURNPREDICTIONRESSOURCES = join(BASEDIR, 'churn_prediction_ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(CHURNPREDICTIONRESSOURCES)
sys.path.append(BASEDIR)
from buttons import * # type: ignore 
from CPfunctions import * # type: ignore 
from home import home

models : dict[str:any] = models_loader()# type: ignore
clf = models['churn_model'] # type: ignore

def churnprediction(elem, method, form, args):




	toadd = ""
	if method == 'POST':

		
		result = ""
		errors = ""

		if form['Client_ID'] == "" or form['Client_ID'] == None:

			try:
                                
				Total_Relationship_Count = int(form['Total_Relationship_Count'])
			
			except:
                                
				Total_Relationship_Count = 0
				
				errors += "Warning error during converting"
            
			try:
            	
				Credit_Limit = float(form['Credit_Limit'])
            
			except:
                
				Credit_Limit = 0
                
				errors += "Warning error during converting"
                                
			try:
                
				Total_Revolving_Bal = float(form['Total_Revolving_Bal'])
            
			except:
                
				Total_Revolving_Bal = 0
                
				errors += "Warning error during converting"
				
			try:
                
				Avg_Open_To_Buy = float(form['Avg_Open_To_Buy'])
            
			except:
                
				Avg_Open_To_Buy = 0
                
				errors += "Warning error during converting"
				
			try:
                
				Total_Trans_Amt = float(form['Total_Trans_Amt'])
            
			except:
                
				Total_Trans_Amt = 0
                
				errors += "Warning error during converting"
				
			try:
				
				Total_Trans_Ct = int(form['Total_Trans_Ct'])
            
			except:
                
				Total_Trans_Ct = 0
                
				errors += "Warning error during converting"

			data = pd.DataFrame({
            'Total_Relationship_Count': [Total_Relationship_Count],
            'Credit_Limit': [Credit_Limit],
            'Total_Revolving_Bal': [Total_Revolving_Bal],
            'Avg_Open_To_Buy': [Avg_Open_To_Buy],
            'Total_Trans_Amt' : [Total_Trans_Amt],
            'Total_Trans_Ct' : [Total_Trans_Ct]
            })

			#predict
			if clf.predict(data)[0] != 'Attrited Customer':
                
				r = 'not ' 


			

			



			
		
	result = ""
	elem['content'] = Mk(f"""   <div class="wrapper">
								<div class="inner">
									<!-- Form -->
								<section>
									<h3>Churn predictor</h3>
									<h4>
										{result}
									</h4>
									<form method="POST" action="#">
										<div class="row gtr-uniform gtr-50">
	
																									
	
	
											<div class="col-12">
												<h4>Enter the client number</h4>
											</div>
	
	
											<div class="col-12"><div class="col-12 col-12-xsmall">
												<input type="number" name="Client_ID" id="Client_ID" value="" placeholder="Client number" pattern="[0-9]{9}"/>
											</div></div>
	
	
	
											
											<div class="col-12">
												<h4>or</h4>
											</div>
				
											
											
											<div class="col-6">
												<input type="number" min="0" step="1" max="100" name="Total_Relationship_Count" id="Total_Relationship_Count" value="" placeholder="Number of products" />
											</div>
	
											<div class="col-6">
												<input type="number" min="0" step="0.01" max="1000000000000" name="Credit_Limit" id="Credit_Limit" value="" placeholder="Credit Limit" />
											</div>
	
											<div class="col-6">
												<input type="number" min="0" step="0.01" max="1000000000000" name="Total_Revolving_Bal" id="Total_Revolving_Bal" value="" placeholder="Revolving balance" />
											</div>
	
											<div class="col-6">
												<input type="number" min="0" step="0.01" max="1000000000000" name="Avg_Open_To_Buy" id="Avg_Open_To_Buy" value="" placeholder="Avg Open_To_Buy" />
											</div>
	
											<div class="col-6">
												<input type="number" min="0" step="0.01" max="1000000000000" name="Total_Trans_Amt" id="Total_Trans_Amt" value="" placeholder="Total transaction amount" />
											</div>
	
											<div class="col-6">
												<input type="number" min="0" step="0.01" max="1000000000000" name="Total_Trans_Ct" id="Total_Trans_Ct" value="" placeholder="Total number of transaction" />
											</div>
	
											<div class="col-12">
												<br>
											</div>
			
											<div class="col-12">
												<ul class="actions">
													<li><input type="submit" value="submit" class="primary" /></li>
													<li><input type="reset" value="Reset" /></li>
												</ul>
											</div>
										</div>
	
	
	
										
									</form>



								<h3>Data insight</h3>
								<p>
									We can see in the graphs below the impact that different personal criteria (gender, income, education,...) have on the attrition flag.
								</p>""" + """
								<section>
									<div class='tableauPlaceholder' id='viz1677705562080' style='position: relative'><noscript><a href='#'><img alt='Tableau de bord 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Cl&#47;Cluster_16775116554160&#47;Tableaudebord1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Cluster_16775116554160&#47;Tableaudebord1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Cl&#47;Cluster_16775116554160&#47;Tableaudebord1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='fr-FR' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1677705562080');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='755px';vizElement.style.maxWidth='1355px';vizElement.style.width='100%';vizElement.style.minHeight='287px';vizElement.style.maxHeight='1087px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='755px';vizElement.style.maxWidth='1355px';vizElement.style.width='100%';vizElement.style.minHeight='287px';vizElement.style.maxHeight='1087px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1127px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
									<div class='tableauPlaceholder' id='viz1677746820346' style='position: relative'><noscript><a href='#'><img alt='Tableau de bord 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;Income_16777458109470&#47;Tableaudebord2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Income_16777458109470&#47;Tableaudebord2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;Income_16777458109470&#47;Tableaudebord2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='fr-FR' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1677746820346');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='755px';vizElement.style.maxWidth='1355px';vizElement.style.width='100%';vizElement.style.minHeight='287px';vizElement.style.maxHeight='1087px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='755px';vizElement.style.maxWidth='1355px';vizElement.style.width='100%';vizElement.style.minHeight='287px';vizElement.style.maxHeight='1087px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1027px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>								</section>


								</section>
							
					</section>""") + toadd 
	
	return elem