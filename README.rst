========
tatorter
========

"tatorter" is a simple script to rename video files of the German police crime drama television series "Tatort" to a standardized file name format.
That makes it a lot easier to archive local copies of the episodes which may come from various sources with different and/or insufficient naming schemes.
The used information such as episode indexes and detective team is fetched from the list of episodes on the German Wikipedia.
For each video file to be renamed, tatorter uses an easy heuristic with some fuzzy string matching to find the 5 best fitting episodes and to rename the file
according to the user's choice.

GitHub page: https://github.com/DLFW/tatorter

tatorter depends on Python 3 and can be installed with *pip*.

Since tatorter can handle only the original German episode names, the rest of this documentation is also written in German. :)

Deutsch
=======

„tatorter" ist ein einfaches Skript um lokale Videodateien der Serie „Tatort" automatisch umzubenennen und so ein einheitliches Dateinamensschema für alle Videos zu erhalten.
Das macht die Archivierung einfacher und erhöht die Übersichtlichkeit der Sammlung.
Die notwendigen Daten wie Episodennummer und Ermittlerteam werden dabei aus der deutschen Wikipedia bezogen.
Für jede Videodatei, die umbenannt werden soll, ermittelt tatorter die fünf besten Episoden-Treffer durch eine Heuristik mit Fuzzy-String-Suche. Der Anwender wählt dann
den passenden Treffer aus.

Erhält man Tatort-Videos beispielsweise aus der ARD-Mediathek, haben diese oft Namen wie ``Tatort Auf einen Schlag MDR Fernsehen Video ARD Mediathek.mp4``.
tatorter würde für diese Datei etwa folgende Umbenennungsvorschläge machen:

.. code-block::

   ================================================================================
   Choose new name for "Tatort Auf einen Schlag MDR Fernsehen Video ARD Mediathek.mp4"
   --------------------------------------------------------------------------------
       1  (84%)| Tatort - 2022x07 - Sieland, Gorniak, Mohr und Schnabel - 18 - Auf einen Schlag.mp4
   --------------------------------------------------------------------------------
       2  (63%)| Tatort - 1982x01 - Stoever und Brockmöller - 2 - Tod auf Eis.mp4
   --------------------------------------------------------------------------------
       3  (57%)| Tatort - 2014x03 - Lannert und Bootz - 28 - Stau.mp4
   --------------------------------------------------------------------------------
       4  (53%)| Tatort - 1994x06 - Ehrlicher und Kain - 5 - Feuertaufe.mp4
   --------------------------------------------------------------------------------
       5  (51%)| Tatort - 1996x02 - Ehrlicher und Kain - 10 - Tanz auf dem Hochseil.mp4
   --------------------------------------------------------------------------------

Dabei wird je ein Index (hier von 1 bis 5), eine Trefferquote (als Prozentangabe) und der zur Wahl stehende neue Dateiname angezeigt.

Verwendung
==========

„tatorter" benötigt Python 3. Die Installation kann mit *pip* vorgenommen werden (``pip3 install tatorter``).

Das Skript ist nur unter Linux getestet. Durch die Windows-Dateisysteme werden unter Windows viele Umbenennungen fehlschlagen, da viele
Tatort-Titel Zeichen enthalten, die unter Windows nicht in Dateinamen erlaubt sind.

.. NOTE::

    Für **Linux** gilt: Wird ein Paket nicht als „root" installiert, kann es je nach Distribution sein,
    dass das Python-Skript später nicht direkt aufgerufen werden kann.

    Für **Windows** relevant: Es steht neben dem Skript ``tatorter`` auch ein identisches Skript mit
    dem Namen ``tatorter.py`` zur Verfügung, welches auch für Windows als Python3-Skript zu erkennen ist,
    sofern die Dateiendung mit dem Python3-Interpreter verknüpft ist.

„tatorter" wird als Python-Skript installiert und kann damit typischerweise systemweit aufgerufen werden.
Die umzubenennenden Dateien müssen mit Dateinamen oder „Globbing"-Dateinamenmuster mit „*" und „?" und „[...]" als Platzhaltern als Argument übergeben werden.
Etwa ``tatorter "Schwanensee Tatort Video ARD Mediathek.mp4"`` oder ``tatorter *.mp4``.

Für alle passenden Dateien werden anschließend Namensvorschläge ermittelt. Die besten fünf Treffer stehen dann jeweils zur Auswahl.

Beim ersten Start werden die notwendigen Informationen von der `Liste der Tatort-Folgen`_ der deutschen Wikipedia bezogen und in einer Cache-Datei ``.tatorter.cache`` im Heimverzeichnis abgelegt.
Ist dieser Cache älter als 24 Stunden, wird er verworfen und die Daten erneut aus der Wikipedia bezogen.
Mit der Option ``-c`` kann eine andere Cache-Datei gewählt werden.
Die Option ``-r`` forciert ein Update des Cache, egal wann dieser zuletzt aktualisiert wurde.

Das Namensschema ist derzeit fest codiert und müsste bei Bedarf in ``cli.py`` (Variable ``file_rename_pattern``) manuell angepasst werden.
Es lautet derzeit::

    Tatort - {season}x{episode:0>2} - {team} - {case_index} - {title}

Beispiel: ``Tatort - 2022x07 - Sieland, Gorniak, Mohr und Schnabel - 18 - Auf einen Schlag.mp4``

Die Variable ``location`` enthält dabei die Heimatstadt/-region des jeweiligen Ermittlerteams. Sie ist die einzige Information, die nicht direkt aus der Wikipedia stammt,
sondern anhand eines Mappings (``team_to_location`` in ``grabber.py``) aus dem Teamnamen abgeleitet wird.
Das Mapping umfasst derzeit alle ~150 bekannten Ermittlerteams aus der Geschichte des Tatort.
Bei Crossover-Folgen mit mehreren Teams (z.B. „Ballauf und Schenk / Saalfeld und Keppler") werden die Heimatstädte automatisch kombiniert (z.B. „Köln-Leipzig").

.. WARNING::

   Manuelle Änderungen an den Quellen werden bei einem Update via *pip* überschrieben!

Insgesamt stehen die folgenden Variablen für das Namensschema zur Verfügung:

* ``episode_index``: Absoluter Episodenindex (fortlaufend über alle Jahre)
* ``season``: Staffel (= Ausstrahlungsjahr)
* ``episode``: Episodennummer innerhalb der Staffel
* ``location``: Heimatstadt/-region des Ermittlerteams
* ``title``: Titel der Episode
* ``broadcaster``: Produzierende Rundfunkanstalt
* ``premiere``: Datum der Erstausstrahlung
* ``team``: Ermittlerteam
* ``case_index``: Fall-Nummer des jeweiligen Ermittlerteams
* ``author``: Autor der Episode
* ``director``: Regisseur der Episode

GitHub-Seite: https://github.com/DLFW/tatorter

.. _`Liste der Tatort-Folgen`: https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen

tatorter steht unter der `GNU General Public License`, Version 3 (GPL 3).

+--------------------------------------------------------------------------------------+
| tatorter is a free and open project, you can redistribute it and/or modify           |
| it under the terms of the `GNU General Public License`_ as published by              |
| the Free Software Foundation, either version 3 of the License, or any later version. |
|                                                                                      |
| tatorter is distributed in the hope that it will be useful,                          |
| but without any warranty; without even the implied warranty of                       |
| merchantability or fitness for a particular purpose.  See the                        |
| GNU General Public License for more details.                                         |
+--------------------------------------------------------------------------------------+

.. _GNU General Public License: http://www.gnu.org/licenses/
