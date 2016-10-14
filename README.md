Eat Da Fruit Fruit in Python
----------------------------

A simple game for studying a better infrastructure for games.  
You are a monkey and you need to eat da fruit fruit. A human is throwing apples at you.
Catch them with a mouse click.

![monkey](images/monkey.png)


Requirements
------------

Download [Windows standalone exe from eize.ninja](http://eize.ninja/d/eatdafruitfruit-win.7z)  
_No one really knows what Windows versions it supports..._

**Or** you can use Python 2.7 and pygame directly. Best practice would be `pip install pygame` in a virtual env.
Run with `python run.py`.


Bundle to exe using pyinstaller
-------------------------------

This was surprisingly easy.

 - Create and activate a virtual env with Python 2.7
 - `pip install pygame pyinstaller`
 - `pyinstaller --windowed --oneline --icon=icon.ico run.py --name "Eat Da Fruit Fruit"

