Detta är källkoden till XPs loggbok V2.0

Alla kodfiler ligger i mappen Loggbok2.0/src/ och består av följande

- main.py
Detta är huvudprogrammet som körs. I denna finns kod relaterad till
den logiska ordningsföljden av huvudloopen samt koden för att flytta
olika bilder för att visa hur många som är inloggade just nu

-excel_handler
I denna fil finns allt som rör hanteringen av excelfiler.

-paths
Här finns alla stringvariabler relaterade till olika filnamn och sökvägar

-statistic_handler
All kod som behandlar loggning av statistik finns här. Dock ej koden som
sparar statistiken som excelfil, den finns i excel_handler.

-member
Innehåller klassen member vilken är en klass som alla medlemmar i medlems-
registret tillhör och initieras till vid uppstart av programmet.

-gui_module
Denna behandlar allt det grafiska i gränssnittet.

Alla resurser vilka bör vara statiska finns i mappen Loggbok2.0/res/
Dessa innefattar bilder/bakgrundsbilder.

