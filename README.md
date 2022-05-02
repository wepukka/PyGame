# Seminaarityö pygame target practice
Pythonin pygame kirjastolla tehty peli, jossa klikkaillaan maalitauluja ja saadaan pisteitä. Tarkoitus esitellä asioita mitkä koin tärkeiksi ja mistä suurin oppimiskokemus


# Tavoitteet
Target practice peli  on totetukseltaan suhteellisen yksinkertainen, jossa tarkoituksena oli harjoitella pythonin ja pygame kirjaston perus elementtejä. Pythonin ollessa suhteellisen tuntematon ohjelmointikieli itselle, peli koodauksen alkeista taustaa [Unityllä](https://unity.com/).

# Toteutus

Peli koostuu pääosin kolmesta python tiedostosta: peliä pyörittävästä [main.py](https://github.com/wepukka/PyGame/blob/main/main.py), tärkeimmät pelifunktiot sisältävästä [targetPractice.py](https://github.com/wepukka/PyGame/blob/main/TargetPractice.py), sekä tietokannan hallinnointiin [handleDb.py](https://github.com/wepukka/PyGame/blob/main/handleDb.py).

Jotta pygame kirjastoa voidaan käyttöö tulee se asentaa, importoida ja alustaa ohjelmaan. Tähän tarvitaan [PIP](https://pypi.org/project/pip/):iä, pythonin paketinhallintaa millä voidaan asentaa paketteja, jotka eivät kuulut python standardi kirjastoon. Uusimmat python versiot sisältävät tämän.

    python3 -m pip install -U pygame --user
    from pygame import *
    pygame.init()


## Renderöinti
Pelin käynnistyessä aletaan renderöimään (piirtämään) [main_menu()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L58-L104) funktiota, joka toimii pelin päävalikkona.
Tällöin ruutu jolle on määritelty leveys ja korkeus arvot, täytetään kuvalla tai vaikka pelkällä yhdellä värillä, jonka päälle sitten renderöidään kaikki muu. Leveys ja korkeus hyvä määrittää muuttujiin jotta niihin voidaan viitata ohjelman myöhemmissä vaiheissa.

    WIDTH, HEIGHT = 1600, 900 # Määritellään haluttu leveys ja korkeus
    WIN = pygame.display.set_mode((WIDTH,HEIGHT)) # Asetetaan peli-ikkunan mitat
    WIN.fill((BLACK)) # Täytetään ruutu mustalla

[main_menu()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L58-L104) pyörii koko pelin ajan taustalla, ollaan sitten [Asetuksissa](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L106-L139) tai itse [Pelimuodossa](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L141-L184).
Kun halutaan vaihtaa näkymää, aletaan uutta näkymää renderöimään päävalikon päälle.

     if button_1.collidepoint((mouse_x, mouse_y)):
            if click:
                play() # Tämän jälkeen tapahtuu taas WIN.fill((VÄRI)), joka tulee aikaisemman päälle.

        if button_2.collidepoint((mouse_x, mouse_y)):
            if click:
                options()
 

Toisin muin [main_menu()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L58-L104) funktio, [play()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L141-L184) ja [options()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L106-L139) funktiot eivät pyöri jatkuvasti, vaan ne lopetetaan määritellyssä tapahtumassa. Esim. play() funktiossa, kun painetaan haluttua näppäintä ja "game_over" ehto on täyttynyt tallennetaan pisteet ja lopetetaan renderöinti.

    if event.key != 1 and game_over: # game over, save score
                    save_score(score,hit_accuracy,today)
                    running = False # LOPETETAAN RENDERÖINTI 


 ### Nappuloiden renderöinti
 Tässä esimerkissä renderöidään päävalikon nappulat, jotka olivat hieman näkyvissä jo aikaisemmassa esimerkissä.

 **Options ja Play kuvat ladataan assets kansiosta**

    OPTIONS_IMAGE = pygame.image.load(os.path.join("assets", "Options.png"))
    PLAY_IMAGE = pygame.image.load(os.path.join("assets", "Play.png"))

 **Määritellään napit ja piirretään kuvat**

 Rect() funktiolla taltioidaan nappuloiden sijainti x,y kordinaateissa, sekä koko pikseleinä. Tämän jälkeen piirretään kuvat kyseiseen sijantiin.
 
    button_1 = pygame.Rect(WIDTH/2-100, HEIGHT/2 -100, 200, 50)
    button_2 = pygame.Rect(WIDTH/2-100, HEIGHT/2, 200, 50)

    WIN.blit(PLAY_IMAGE, (button_1.x, button_1.y)) 
    WIN.blit(OPTIONS_IMAGE, (button_2.x, button_2.y))

Itselläni kuvat olivat entuudestaan halutun kokoiset joten niitä ei ollut tarvetta muokata. Isommissa projekteissa koon muokkaaminen tulisi varmasti eteen, varsinkin jos halutaan skaalata kuvien kokoa suhteessa ikkunan kokoon.

    uusi_koko = pygame.transform.scale(muokattava kuva, (haluttu_leveys, haluttu_korkeus))

 ## Pelilogiikka
Peruspelin totetuttaminen ei ole logiikaltaan kauhean mullistava. Piirretään maalitaulut satunnaisesti ruutuun tiettyjen x,y kordinaattien sisälle. Tässä käytetty vain pythonin omaa randrange() funktiota. Arvoina annettu leveys ja korkeus, joista poistettu 100 pikseliä suuntaansa. Tähän syynä se että kun pygame:ssa piirretään esim. 50 leveä 50 korkea maalitaulu kohtaan x = 1550 ja y = 850, on piirrettävän maalitaulun 0,0 kohta siinä pisteessä. Jos voitaisiin piirtää lähemmäs reunaa, saattaisivat taulut mennä ruudun ulkopuolelle.

    def randomize_spawn(): # Randomize target spawn   
        x = randrange(WIDTH - 100)
        y = randrange(HEIGHT - 100)
        return x,y

Yhtenä ydinfunktiona tässä pelissä toimii handle_hit() funktio, jossa tarkastetaan onko hiiren kursori maalitaulun päälle kun sitä klikataan ja poistaa kyseisen kohteen. mouse_position() palauttaa x ja y kordinaatit hiiren sijainnista ja niitä vertaillaan piirrettyjen taulujen sijaintiin. Tässä piti ottaa huomioon myös tuo taulujen koko, mikä oli tässä tapauksessa 50 pikseliä x ja y akselilla. 

    def handle_hit(targets): # Check if mouse cursor x & y axis inside targets 50px range
        mouse_position = get_mouse_position()
        for target in targets:
            if mouse_position[0] >= target.x and mouse_position[0] <= target.x + 50 and mouse_position[1] >= target.y and mouse_position[1] <= target.y + 50:
                    targets.remove(target)
                    return True

Tätä testailtaessani ihmettelin että jopas toimii huonosti, kun klikatessa taulut eivät aina kadonneetkaan. Tämä johtuikin liian alhaiseksi määritellystä [FPS](#fps):stä.


### FPS
Pygame:ssa määritetään FPS (Frames per second), mikä kertoo kuinka usein ruutua päivitetään. Ruudun päivityksen tarve voi vaihdella peleittäin, eivätkä kaikki pelit välttämättä tarvitse korkeaa ruudun päivitystä. Target practice:ssa ohjelman tulee koko ajan tarkistaa missä hiiri sekä maalitaulu sijaitsevat. Tällöin pieni FPS (testattu 30) ei riitä päivittämään hiiren sijainti tarpeeksi nopeasti, jolloin maalitaulua klikatessa ohjelma ei ole vielä välttämättä saanut viimeisintä sijaintia.

**Ruudun päivittämisen määrittäminen**

    FPS = 60
    clock = pygame.time.Clock() # ALUSTETAAN FUNKTION ULKOPUOLELLA
    clock.tick(FPS) # AJETAAN FUNKTION WHILE LOOPISSA

## Lisäksi
**Musiikki**

Musiikin lisääminen oli tärkeä osa pelin luomista, jotta siihen saadaan edes jonkinlaista tunnelmaa. Tämä oli äärimmäisen helppo prosessi. Importoidaan mixer ja laitetaan pauhamaan. 

        mixer.music.load(os.path.join("assets", "hayden-folker-cast-aside.wav"))
        mixer.music.play(-1) # -1 laittaa musiikin toistumaan sen päättyessä.

**Tietokanta**

Tietokantana parhailla pisteille toimii tinydb, joka toimii kätevästi lokaalisti. Pelin käynnistyessä tietokanta käydään läpi ja lajitellaan "scoren" mukaan. Kurssilla käytetty algorytmi sopi tähän mainiosti

    scores = search_all() # SORT BY SCORE
    for i in range(len(scores)):
        key = scores[i]
        j = i-1
        while j >= 0 and key["score"] > scores[j]["score"] :
            scores[j+1] = scores[j]
            j -= 1
        scores[j+1] = key


# Käyttöönotto
Pelaamiseen vaaditaan tietokoneelle asennettu [Python](https://realpython.com/installing-python/), peli on tehty ja testattu käyttäen Python versiota 3.10.4.
Githubista tiedostojen lataamisen jälkeen riittää terminaalissa "pip install -r requirements.txt" komennon ajaminen.

# Yhteenveto
Pienellä python taustalla ja muutamalla tutoriaalilla pääsi aika hyvin alkuun. Python kielenä on hyvin selkeä lukuista ja sen takia se sopii hyvin tähänkin tarkoitukseen. Pygame oli hyvin dokumentoitu, siten että sitä ymmärtää vaikka taustalla ei välttämättä olisikaan alan ymmärrystä. Tietenkään pygamea ei voi verrata isoihin pelimoottoreihin kuten [UNITY](https://unity.com/) tai [UNREAL ENGINE](https://www.unrealengine.com/en-US/) mutta tälläkin saa ihmeitä aikaiseksi.

# Sisältö

[Target practice](#target-practice)

[Johdanto](#johdanto)

[Toteutus](#toteutus)

&emsp;&emsp;[Renderöinti](#renderöinti)

&emsp;&emsp;[Pelilogiikka](#pelilogiikka)

&emsp;&emsp;&emsp;&emsp;[FPS](#fps)

$~~~~~~$[Lisäksi](#lisäksi)

[Käyttöönotto](#käyttöönotto)

[Lähteet](#lähteet)

[Krediitit](#krediitit)
# Lähteet
- [pygame](https://www.pygame.org/docs/)
- [tinydb](https://tinydb.readthedocs.io/en/latest/)
- [Tech with Tim. Pygame in 90 minutes](https://www.youtube.com/watch?v=jO6qQDNa2UY&t=4092s&ab_channel=TechWithTim)
- [CDcodes. Pygame Sprite Sheet Tutorial](https://www.youtube.com/watch?v=ePiMYe7JpJo&t=724s)

# Krediitit
**Musikki**

Cast Aside by Hayden Folker | https://soundcloud.com/hayden-folker
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US


----

