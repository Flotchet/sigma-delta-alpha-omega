from flask import Markup as Mk
import sqlalchemy as sql

from os.path import join, dirname, abspath
BASEDIR = abspath(dirname(__file__))
RESSOURCES = join(BASEDIR, 'ressources')
REALESTATERESSOURCES = join(BASEDIR, 'real_estate_ressources')
import sys
sys.path.append(RESSOURCES)
sys.path.append(REALESTATERESSOURCES)
sys.path.append(BASEDIR)
from buttons import * # type: ignore 
from REfunctions import * # type: ignore 
import pandas as pd


df : pd.DataFrame = pd.read_csv(join(REALESTATERESSOURCES, 'data_for_regression.csv'))

zipcode_converter : dict[int:float] = prepare_zipcode(df)# type: ignore
tax_converter : dict[int:float] = prepare_tax(df)# type: ignore
type_converter : dict[str:float] = prepare_type(df)# type: ignore

models : dict[str:any] = models_loader()# type: ignore


    



def realestate(elem, method, form, args):

	result = ""

	if method == 'POST':
		#category
		immo = form['category']
    	#zipcode
		zipcode = form['zipcode']
    	#number of room
		room = form['number of room']
    	#living area
		surface = form['living Area']
                
		value : float = 0

    	#check if the data are correct
		result : str = check(immo, zipcode, room, surface)
		
                
		if result != "":             
			result=Mk(result)
        
		else:
			zipcode = int(zipcode)  
        
			room = int(room)
                
			surface = float(surface)
                
			#other usefull form field
			garden : str = form['Total Area of gardens']
            
			try:
                
				garden = float(garden)
                                
			except:
                
				garden = 0
                                
			terrace = form['Total Area of terraces']
                        
			try:
                
				terrace = float(terrace)
                                
			except:
                              
				terrace = 0
                                
			try:
                              
				furnished = form['Furnished']
                                
				if furnished == "on":
                                      
					furnished = True
					
				else:
					
					furnished = False
					
			except:
				
				furnished = False
				
			try:
				
				Equiped = form['Equiped kitchen']
				
				if Equiped == "on":
					
					Equiped = True
					
				else:
					
					Equiped = False
					
			except:
				
				Equiped = False
				
			name = get_name(zipcode)
			
			try:
				
				current_mdl = models[name]
				
			except:
				
				result+=f"Sorry we don't have a model for {name}"
				
			if zipcode not in zipcode_converter.keys():
				
				result+=f"\n Sorry the zipcode: {zipcode} doesn't exist passing on default 'Liège' \n"
				 
				zipcode = 4000


				
			zipcode_v = zipcode_converter[zipcode]
				
			
			immo_v = type_converter[immo]
			
			if zipcode not in tax_converter:
				
				result+=f"\n Sorry the zipcode: {zipcode} doesn't refer to a city tax passing on default 'Liège' \n"

				zipcode = 4000		
				
			tax = tax_converter[zipcode]
			
			
			
			#make a dict of the data
			data = {
            	'Number of rooms': room, 
            	'Living Area': surface, 
            	'Fully equipped kitchen': Equiped, 
            	'Furnished': furnished, 
            	'Area of the terrace': terrace,
            	'Area of the garden': garden, 
            	'zipcode': zipcode_v,    
            	'type': immo_v, 
            	'Taxe': tax
				
				}
			
			#transform the dict in a data frame
			data = pd.DataFrame(data, index=[0])
			
			value = current_mdl.predict(data)*surface
			value = round(value[0])
			result += f"Your {immo} has a value of approximatly {value} euros. (The selected model is XGboost{name})"
		
		

	
	elem['content'] = Mk(f"""   <section>
									<h3>Real Estate Price Prediction</h3>

									<p>This AI property price estimator uses a machine learning model called XGboost to predict the price of a property based on certain features. These features include the type of property, its location (by zip code), the size of the living area, the number of rooms, and the total area of the terraces and gardens. The model takes into account whether the property is fully equipped with a kitchen and furnished or not. This tool can be used to get an estimate of a property's value with a mean precision from 79 % to 90 % depending on the location.</p>

								<table class="main">
									<thead>
									<tr>
									  <th><br>Province-Zone</br></th>
									  <th><br>Expected precision</br></th>
									</tr>
								</thead>
								<tbody>
									<tr>
										<td>Bruxelles</td>
										<td>84.0%</td>
									  </tr>
									<tr>
									  <td>Anvers</td>
									  <td>85.2%</td>
									</tr>
									<tr>
									  <td>Flandre-Occidentale</td>
									  <td>83.3%</td>
									</tr>
									<tr>
									  <td>Flandre-Orientale</td>
									  <td>85.1%</td>
									</tr>
									<tr>
									  <td>Limbourg</td>
									  <td>86.1%</td>
									</tr>
									<tr>
									  <td>Liège</td>
									  <td>79.7%</td>
									</tr>
									<tr>
									  <td>Luxembourg</td>
									  <td>81.2%</td>
									</tr>
									<tr>
									  <td>Namur</td>
									  <td>80.3%</td>
									</tr>
									<tr>
									  <td>Brabant flamand</td>
									  <td>88.3%</td>
									</tr>
									<tr>
									  <td>Brabant flamand 2</td>
									  <td>87.4%</td>
									</tr>
									<tr>
									  <td>Brabant wallon</td>
									  <td>89.4%</td>
									</tr>
									<tr>
									  <td>Hainaut 1</td>
									  <td>81.5%</td>
									</tr>
									<tr>
									  <td>Hainaut 2</td>
									  <td>79.1%</td>
									</tr>
									</tbody>
								  </table>

								<section>
								<h3>Enter the specification of your proprety</h3>
								
								<form method="post" >

									<div class="row gtr-uniform">

										<div class="col-12">
											<select name="category" id="category">
												<option value="">- Category -</option>
												<option value="Farm">Farm</option>
  												<option value="Apartment">Apartment</option>
  												<option value="Student housing">Student housing</option>
  												<option value="Penthouse">Penthouse</option>
  												<option value="Service apartment">Service apartment</option>
  												<option value="Chalet">Chalet</option>
  												<option value="House">House</option>
  												<option value="Ground floor">Ground floor</option>
  												<option value="Master house">Master house</option>
  												<option value="Country house">Country house</option>
  												<option value="Loft">Loft</option>
  												<option value="Bel-etage house">Bel-etage house</option>
  												<option value="Pavilion">Pavilion</option>
  												<option value="Duplex">Duplex</option>
  												<option value="Triplex">Triplex</option>
  												<option value="Studio">Studio</option>
  												<option value="Mixed building">Mixed building</option>
  												<option value="Exceptional property">Exceptional property</option>
  												<option value="Castle">Castle</option>
  												<option value="Building">Building</option>
  												<option value="Manor">Manor</option>
  												<option value="Bungalow">Bungalow</option>
  												<option value="Villa">Villa</option>
												<option value="Other goods">Other goods</option>
											</select>
										</div>

										<div class="col-6 col-12-xsmall">
											<input type="number" min="1000" name="zipcode"  max="9999" id="zipcode" value="" placeholder="zipcode ZZZZ" />
										</div>
										<div class="col-6 col-12-xsmall">
											<input type="number" min="1" name="number of room" max="100" id="number of room" value="" placeholder="number of rooms N" />
										</div>
										
										
										<div class="col-4 col-12-small">
											<input type="checkbox" id="Garden" name="Garden">
											<label for="Garden">Garden(s)</label>
										</div>
										<div class="col-4 col-12-small">
											<input type="checkbox" id="Terrace" name="Terrace">
											<label for="Terrace">Terrace(s)</label>
										</div>
										<div class="col-4 col-12-small">
											<input type="checkbox" id="Equiped kitchen" name="Equiped kitchen">
											<label for="Equiped kitchen">Equiped kitchen</label>
										</div>

										<div class="col-4 col-12-xsmall">
											<input type="number" min="0" step="0.01" max="1000000" name="Total Area of gardens" id="Total Area of gardens" value="" placeholder="gardens total area" />
										</div>
										<div class="col-4 col-12-xsmall">
											<input type="number" min="0" step="0.01" max="1000000" name="Total Area of terraces" id="Total Area of terraces" value="" placeholder="terraces total area" />
										</div>
										<div class="col-4 col-12-xsmall">
											<input type="number" min="5" step="0.01" max="1000000" name="living Area" id="living Area" value="" placeholder="living area" />
										</div>

										<div class="col-4 col-12-small">
											<input type="checkbox" id="Furnished" name="Furnished">
											<label for="Furnished">Furnished</label>
										</div>

										<div class="col-12">
											<ul class="actions">
												<li><input type="submit" value="Get an estimation" class="primary" /></li>
												<li><input type="reset" value="Reset" /></li>
											</ul>
										</div>
									</div>
								</form>
							</section>
									
									<section>
								<h3>{result}</h3>
							</section>
								</section>""") 
	
	return elem


