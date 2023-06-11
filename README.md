# Sigma Delta Alpha Omega

Sigma Delta Alpha Omega is a highly dynamic & customizable application made with modular programming & object oriented prgramming principles.

## What is modular programming?

Modular programming is a software design technique that emphasizes separating the functionality of a program into independent, interchangeable modules, such that each contains everything necessary to execute only one aspect of the desired functionality.

Conceptually, modules represent a separation of concerns, and can be independently created, tested, modified or updated, then reused across multiple systems. This modularization of code contributes to reusability, scalability, and efficiency, making it easier to understand, maintain and debug.

Modules are often incorporated through interfaces. A module interface expresses the elements that are provided and required by the module. The elements defined in the interface are detectable by other modules. The implementation contains the working code that corresponds to the elements declared in the interface.

Programming languages have different levels of modularity, from minimal language support (C, FORTRAN) to moderate modularization (Java, C++) to high modularization (Ada, Modula, Pascal, Python).

## What is coming next ?

Adaptation of the rest of the applets from previous projects

## Authors

- [@flotchet](https://www.github.com/flotchet)

## Schematic of how the app works

![Schematic of the app](README/images/schematicbg.png)

## How to create your applet

First of all you need to create an ini file. This is where you put all the information about your applet. It's very easy to do. Just open up notepad and type in the following:

```bash
min_lvl = integer between 0 and 4
max_lvl = integer between 0 and 4 (must be greater or equal than min_lvl)
name = the name of your applet
author = your name
version = the version of your applet
description = a description of your applet
dep0 = the name of the first dependency
dep1 = the name of the second dependency
...
depN = the name of the Nth dependency
```

Second you need to create a folder in the applets folder. The name of the folder must be the name of your applet with the word ressources at the end
this folder will contain all the python files that are needed for your applet to work.

Third you need to create a python file in the applet folder. This file will contain the code for your applet. It must be named {name of your ini file}.py.

Fourth you need to create to create only one function called {name of your ini file} with these arguments
elem, method, form, args this function must return only the modified elem

elem is all the HTML content that your applet will be displayed in
it also contains the following keys and type:

```bash
    head : Markdown         = Markdown(String)
    header : Markdown       = Markdown(String)
    content : Markdown      = Markdown(String)
    side_content : Markdown = Markdown(String)
    search : Markdown       = Markdown(String)
    menu : Markdown         = Markdown(String)
    side_footer : Markdown  = Markdown(String)
    scripts : Markdown      = Markdown(String)

    _attr_lvl : int     = Integer (0-4) MUST NOT BE CHANGED BY YOUR APPLET
    _usr : str          = String MUST NOT BE CHANGED BY YOUR APPLET

```

Method is the method that is used to call your applet. It can be either 'GET', 'POST', 'PUT', 'DELETE', 'SUPER'.

form is the form that will be attached with the POST method if the method is POST or PUT.

args is a list of arguments that are passed to your applet if needed.
