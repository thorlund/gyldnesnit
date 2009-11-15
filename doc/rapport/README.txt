* Globals

/ = doc/rapport/

Bemærk at der ligger en nice Makefile som sørger for det rette antal
kompileringer.


* Navngivningskonvention for filnavne

Små bogstaver
Mellemrum bliver underscore


* Struktur

Hoveddokument
	/rapport.tex

Litteratur
	/litteraturliste.bib

Hvert afsnit i rapporten skal have sin egen mappe i /afsnit/

	Eksempel:

		Afsnittet "Indledning" har sine filer liggende i
		/afsnit/indledning/

		Et hypotetisk afsnit kaldet "Vores implementering" vil ligge i
		mappen /afsnit/vores_implementering/

Hvis et afsnit har underafsnit bør disse også ligge separat.

	Eksempel:
		"Vores implementering" har underafsnittene "Kantdetektion" og
		"Monstergenkendelse". Strukturen ser da således ud:

		vores_implementering.tex
		   |
		   |----- kantdetektion.tex
		   |
		   |----- monstergenkendelse.tex

		Denne struktur betyder at i vores_implementering vil
		underafsnittene blive taget ind ved brug af
		\input{}-kommandoen i latex.

		Eksempel (uddrag fra vores_implementering.tex):
			\section{Kantdetektion}
			\input{afsnit/vores_implementering/kantdetektion.tex}
		
		BEMÆRK! I input-kommandoen skal underafsnittene refereres til
			som stod man ved hoveddokumentet.


* Billeder/Illustrationer

Er der i et afsnit brug for at inkludere billeder skal der i det pågældende
afsnits mappe tilføjes en ny mappe der hedder "billeder" til disse.

	Eksempel:

		Eventuelle billeder i afsnittet "Vores implementering" lægges
		i mappen /afsnit/vores_implementering/billeder/
