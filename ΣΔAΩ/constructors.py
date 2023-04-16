from __future__ import annotations
from flask import Markup as _Mk
from os.path import join, dirname, abspath
from os import listdir
from json import dumps



BASEDIR = abspath(dirname(__file__))
JSDIR = join(BASEDIR, 'static', 'js')

class elements():

    class __metaclass__(type):
        def __repr__(self):
            return """
    <elements class>
    This class is used to construct the HTML elements of the webapp
    attributes type: flask.Markup (flask.wrappers.Response) for the HTML elements and str for the user name and int the attribute level
    """



    """
    This class is used to construct the HTML elements of the webapp
    
    It is meant to be used as a class, not a module.

    attr_level : -0 disconnected 
                 -1 user
                 -2 employee
                 -3 admin
                 -4 SUPERUSER
    
    """

    head : _Mk         = _Mk("")
    header : _Mk       = _Mk("")
    content : _Mk      = _Mk("")
    side_content : _Mk = _Mk("")
    search : _Mk       = _Mk("")
    menu : _Mk         = _Mk("")
    side_footer : _Mk  = _Mk("")
    scripts : _Mk      = _Mk("")

    _attr_lvl : int     = 0
    _usr : str          = ""


    def __init__(self, applets : list, authors : str, title : str = "ΣΔAΩ") -> None:

        self.scripts = self._scripts()
        self.head = self._head(title)
        self.header = self._header()
        self.usr = title
        self.menu = self._menu(applets)
        self.side_footer = self._footer(authors)
        self.content = "No content"
        self.side_content = "No side content"
        self.search = "No search bar"

        return None
    
    def __repr__(self):

        mtds = [(str(method_name)) for method_name in dir(self) if callable(getattr(self, method_name))]


        bs = ""
        for mtd in mtds:
            bs += "\n"
            bs += mtd
           


        return f"""
        elements object with accessible attributes:

        head:
        _____
        {self.head}

        header:
        _______
        {self.header}

        content:
        ________
        {self.content}

        search:
        _______
        {self.search}

        menu:
        _____
        {self.menu}

        side_footer:
        ____________
        {self.side_footer}

        scripts:
        ________
        {self.scripts}

        elements object with accessible methods:

        {bs}
        """

    def _scripts(self) -> _Mk:

        js = ""
        for f in listdir(JSDIR):
            if f.endswith('.js'):
                js += f'<script src="/static/js/{f}"></script> \n'

        return _Mk(js)
    
    def _head(self, title : str = "ΣΔAΩ") -> _Mk:

        return _Mk(f"""
            <title>{title}</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
            <link rel="stylesheet" href="static/css/main.css" />
        """)

    def _header(self) -> _Mk:

        return _Mk(f"""
            <a href="/" class="logo"><strong>ΣΔAΩ</strong></a>
            <ul class="icons">
                <li><a href="https://github.com/Flotchet" target="_blank" rel="noreferrer noopener" class="icon brands fa-github"><span class="label">Github</span></a></li>
                <li><a href="https://www.linkedin.com/in/florentmaisse/" target="_blank" rel="noreferrer noopener" class="icon brands fa-linkedin"><span class="label">LinkedIn</span></a></li>
                <li><a href="https://fm-personal-website.onrender.com/" target="_blank" rel="noreferrer noopener" class="icon solid fa-globe"><span class="label">Website</span></a></li>
            </ul>
        """)
    
    def _menu(self, applets : list[str]) -> _Mk:

        menu = """<nav id="menu">
	    <header class="major">
			<h2>Menu</h2>
		</header>
		<ul>
                                    """
        for applet in applets:
            menu += f"""
            <li><a href="/{applet}">{applet}</a></li>"""

        menu += "</ul>"

        return _Mk(menu)
    
    def _footer(self, authors : str):

        return _Mk(f"""<p class="copyright">&copy; {authors}. All rights reserved.</p>""")
    
    def set_content(self, content : str = "") -> _Mk:

        self.content = _Mk(content)

        return self.content
    
    def set_side_content(self, side_content : str = "") -> _Mk:

        self.side_content = _Mk(side_content)

        return self.side_content
    
    def set_search(self, datalist: list[str]) -> _Mk:

        selector = """
        <form method="post" action="#">
            <input type="text" list="search" id="src" name="search" />
		        <datalist id="search">
            """
        
        for data in datalist:
            selector += f"""
                <option value="{data}">
            """

        selector += """
            <form method="post" action="#">
        </datalist>
        """
        self.search = _Mk(selector)

        return self.search
    
    def set_usr(self, usr : str = "", attr_lvl : int = 0) -> None:

        self._usr = usr
        self._attr_lvl = attr_lvl

        return None
    
    def get_usr(self) -> tuple[str,int]:
        return self._usr, self._attr_lvl
    
    def get_usr_name(self) -> str:
        return self._usr
    
    def get_attr_lvl(self) -> int:
        return self._attr_lvl
    

    #make the object json serializable
    def __json__(self):
        return self.__dict__
    
    def toJSON(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    #make the object callable
    def __call__(self):
        return self.todict()
    
    #define the type of the object
    def __type__(self):
        return self.__metaclass__()
    
    def todict(self):
        return self.__dict__






    



if __name__ == "__main__":
    print("This module is not meant to be run as a script.")
    print("It is meant to be imported and used as a class.")
    print("See the documentation for more information.")
    
    elem = elements(applets = ["login", "sign up"], authors = "Florent Maisse")
    elem.set_content("hello")
    elem.set_side_content("HELLO")
    elem.set_search(["choice1", "choice2"])
    print(elem)


    HTML = f"""<!DOCTYPE HTML>
<html>
	<head>
		{elem.head}
	</head>
	<body class="is-preload">

		<!-- Wrapper -->
			<div id="wrapper">

				<!-- Main -->
					<div id="main">
						<div class="inner">

							<!-- Header -->
								<header id="header">
									{elem.header}
								</header>

							<!-- Content -->
								<section>
									<!-- Content -->
									{elem.content}

								</section>

						</div>
					</div>

				<!-- Sidebar -->
					<div id="sidebar">
						<div class="inner">

							<!-- Search -->
								<section id="search" class="alt">
									{elem.search}
								</section>

							<!-- Menu -->
								<nav id="menu">
									{elem.menu}
								</nav>

							<!-- Section -->
								{elem.side_content}

							<!-- Footer -->
								<footer id="footer">
									{elem.side_footer}
								</footer>
						</div>
					</div>

			</div>

		<!-- Scripts -->
			{elem.scripts}

	</body>
</html>"""
    #make an html file
    with open("test.html", "w") as f:
        f.write(HTML)





