========
tatorter
========

“tatorter” is a simple script to rename video files of the German police crime drama television series “Tatort” to a standardized file name format. The used information like episode indexes and detective team is fetched from the list of episodes on the German Wikipedia. That makes it a lot easier to archive local copies of the episodes.

Since tatorter can handle only the original German epsiode names, the rest of this documentation is also written in German. :)


„tatorter“ ist einfaches Skript um lokale Videodateien der Serie „Tatort“ automatisch umzubennen und so ein ein einheitliches Dateinamensschema für alle Videos zu erhalten. Die notwendigen Daten wie Episodennummer und Ermittlerteam werden dabei aus der deutschen Wikipedia bezogen. Erhält man Tatort-Videos beispielsweise aus der ARD-Mediathek, haben diese oft Namen wie ``Tatort Hinter dem Spiegel hr-fernsehen Video ARD Mediathek.mp4``. tatorter würde für diese Datei etwa folgende Umbennennungsvorschläge machen:

.. code-block::

    ================================================================================
    Choose new name for "Tatort Hinter dem Spiegel hr-fernsehen Video ARD Mediathek.mp4"
    ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        1  (84%)| 0955--Frankfurt--Hinter dem Spiegel.mp4
    ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        2  (56%)| 0181--[Hirth]--Die Spieler.mp4
    ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        3  (56%)| 0585--Konstanz--Die Spieler.mp4
    ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        4  (53%)| 0498--[Dellwo und Sänger]--Oskar.mp4
    ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        5  (53%)| 0598--München--Nur ein Spiel.mp4
    ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Dabei wir je ein Index (hier von 1 bis 5), eine Trefferquote (als Prozentangabe) und der zur Wahl stehende neue Dateiname angezeigt.

Verwendung
==========

„tatorter“ wird als Python-Skript installiert und kann damit typischerweise systemweit aufgerufen werde. Als einiziges notweniges Argument muss ein Dateiname oder ein „Globbing“-Dateinamenmuster mit „*“ und „?“ und „[...]“ als Platzhaltern.

Für alle passenden Dateien werden anschließend Namensvorschläge ermittelt. Die besten fünf Treffer stehen dann jeweils zur Auswahl.

Beim ersten Start  werden die notwenigen Information von der `Liste der Tatort-Folgen`_ der deutschen Wikipedia bezogen und in einer Cache-Datei ``.tatorter.cache`` im Heimverzeichnis abgelegt. Ist dieser Cache älter als 24 Stunden wird er verworfen und die Daten erneut aus der Wikipedia bezogen. Mit der Option ``-c`` kann eine andere Cache-Datei gewählt werden.   

.. _`Liste der Tatort-Folgen`: https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen
