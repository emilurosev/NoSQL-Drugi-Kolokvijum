Koraci:
    - Instalirati pymongo Python bilblioteku
    - Preuzeti greece-latest.osm XML fajl sa http://download.geofabrik.de/europe/greece-latest.osm.bz2 i raspakovati ga u folder gde je osm.py
    - Pokrenuti lokalno MongoDB na portu 27017
    - Pokrenuti Python skriptu osm.py
Ishod: 
    - U bazu će biti upisane svi grčki gradovi i ulice
    - U json fajl result.json će biti upisane sve ulice koje se nalaze na slici image.png u prilogu (result.json najbolje otvori u firefox-u zbog prikaza grčkih slova)
Dodatne informacije:
    - koordinate ulica su preuzete iz taga koji sadrži nazive ulica
    - kao test koordinate uzete su dve tačke - severo-zapadna tačka(40.642178, 22.942729) i jugo-istočna tačka(40.625734, 22.977441)
    - koordinate svih ulica u Solunu su proveravane u odnosu na test koordinate