def submit(value : str, hclass : str ="primary") -> str:
    return f""" <div class="col-12">
			        <ul class="actions">
					    <li><input type="submit" value="{value}" class="{hclass}"/></li>
					    <li><input type="reset" value="Reset" /></li>
					</ul>
				</div>"""

def postbtn(value : str, hclass : str ="primary") -> str:
	return f""" <div class="col-12">
					<input type="submit" value="{value}" class="{hclass}"/>	
				</div>"""

def pwd(name : str, placeholder : str, value : str = "") -> str:
	return f"""<div class="col-6 col-12-xsmall">
					<input type="password"  name="{name}" id="{name}" value="{value}" placeholder="{placeholder}" requiered/>
				</div>"""

def txt(name : str, placeholder : str = "", value : str = "") -> str:
	return f"""<div class="col-6 col-12-xsmall">
					<input type="text" name="{name}" id="{name}" value="{value}" placeholder="{placeholder}" requiered/>
				</div>"""

def logger(placeholder : str) -> str:
	return f"""<div class="col-6 col-12-xsmall">
					<input type="text" name="id" id="id" value="" placeholder="{placeholder}"/>
				</div>
				<div class="col-6 col-12-xsmall">
					<input type="password"  name="password" id="pw" value="" placeholder="password"/>
				</div>"""

def breaker() -> str:
	return """<div class="col-6 col-12-xsmall">
				<br>
			</div>"""

def selector_inc(name : str, options : list, category : str = "") -> str:

	opt = ""
	for value,option in enumerate(options):
		opt += f"""<option value="{value}">{option}</option>"""
		
	return f"""<div class="col-6 col-12-xsmall">
					<div class="select-wrapper">
						<select name="{name}" id="{name}" requiered>
							<option value="">- {category} -</option>
							{opt}
						</select>
					</div>
				</div>"""