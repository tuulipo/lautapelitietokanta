# Lautapelitietokanta
Yksinkertainen web-sovelluksena toteutettu lautapelitietokanta, johon käyttäjät voivat lisätä lautapelejä sekä arvioida ja kommentoida niitä. 

* **Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.**
* **Käyttäjä pystyy lisäämään sovellukseen lautapelejä. Lautapeli sisältää perustiedot pelistä (nimi, kesto, pelaajamäärä (min ja max), genre ja ikäraja). Lisäksi käyttäjä pystyy muokkaamaan tai poistamaan lisäämiänsä pelejä.** 
* **Käyttäjä pystyy tarkastelemaan kaikkia lautapelitietokantaan lisättyjä lautapelejä.**
* **Käyttäjä pystyy hakemaan lautapelejä esimerkiksi hakusanan tai genren avulla.**
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisen käyttäjän lisäämän lautapelit sekä viimeisimmän käyttäjän jättämän kommentin tai arvostelun.
* Lautapeleillä on useampia luokitteluja, kuten genre, kesto ja pelaajamäärä. Käyttäjä voi valita jokaisen luokittelun kohdalla yhden tai useamman vaihtoehdon. 
* Sovelluksen toissijainen tietokohde on pelin arvostelu tai peliin liittyvä kommentti. Käyttäjä pystyy lisäämään arvosteluja ja kommentteja kaikkiin tietokantaan lisättyihin peleihin.

(Boldatut osiot on jo toteutettu, muut kohdat odottavat toimia)

## Sovelluksen asennus ja käynnistäminen

1. Kloonaa projekti GitHubista:

   ```bash
   git clone https://github.com/tuulipo/lautapelitietokanta.git
   ```

2. Siirry projektin kansioon:

   ```bash
   cd lautapelitietokanta
   ```

3. Luo virtuaaliympäristö:

   ```bash
   python3 -m venv venv
   ```

4. Aktivoi virtuaaliympäristö:

   Linux/macOS:
   ```bash
   source venv/bin/activate
   ```

5. Asenna Flask:

   ```bash
   pip install flask
   ```

6. Luo tietokanta suorittamalla skeematiedosto:

   ```bash
   sqlite3 database.db < schema.sql
   ```

7. Käynnistä sovellus:

   ```bash
   flask run
   ```

8. Avaa selaimessa osoite:

   http://127.0.0.1:5000


