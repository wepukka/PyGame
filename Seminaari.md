# Target practice
Pythonin pygame kirjastolla tehty peli, jossa klikkaillaan maalitauluja ja saadaan pisteitä.

## Sisältö

[Target practice](#target-practice)

[Johdanto](#johdanto)

[Toteutus](#toteutus)

$~~~~~~$[Renderöinti](#renderöinti)

$~~~~~~$[Pelilogiikka](#pelilogiikka)


$~~~~~~~~~~~~$[FPS](#fps)

[Käyttöönotto](#käyttöönotto)


[Linkkejä](#linkkejä)

# Johdanto
Target practice on totetukseltaan suhteellisen yksinkertainen, jossa tarkoituksena oli harjoitella pythonin ja pygame kirjaston perus elementtejä.

# Toteutus
Peli koostuu pääosin kolmesta python tiedostosta: peliä pyörittävästä [main.py](https://github.com/wepukka/PyGame/blob/main/main.py), tärkeimmät pelifunktiot sisältävästä [targetPractice.py](https://github.com/wepukka/PyGame/blob/main/TargetPractice.py), sekä tietokannan hallinnointiin [handleDb.py](https://github.com/wepukka/PyGame/blob/main/handleDb.py).

## Renderöinti
Pelin käynnistyessä aletaan renderöimään (piirtämään) [main_menu()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L58-L104) funktiota, joka toimiii pelin päävalikkona.
Tällöin ruutu täytetään kuvalla tai vaikka pelkällä yhdellä värillä, jonka päälle sitten renderöidään kaikki muu.

    WIDTH, HEIGHT = 1600, 900 # Määritellään haluttu leveys ja korkeus
    WIN = pygame.display.set_mode((WIDTH,HEIGHT)) # Asetetaan peli-ikkunan mitat
    WIN.fill((BLACK)) # Täytetään ruutu mustalla

[main_menu()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L58-L104) pyörii koko pelin ajan taustalla, ollaan sitten [Asetuksissa](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L106-L139) tai itse [Pelimuodossa](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L141-L184).
Kun halutaan vaihtaa näkymää, aletaan uutta näkymää vain renderöimään päävalikon päälle.

     if button_1.collidepoint((mouse_x, mouse_y)):
            if click:
                play() # Tämän jälkeen tapahtuu taas WIN.fill((VÄRI)), joka tulee aikaisemman päälle.

        if button_2.collidepoint((mouse_x, mouse_y)):
            if click:
                options()

Toisin muin [main_menu()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L58-L104) funktio, [play()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L141-L184) ja [options()](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L106-L139) funktiot eivät pyöri jatkuvasti aikaa, vaan ne lopetetaan määritellyssä tapahtumassa. Esim. play() funktiossa, kun painetaan haluttua näppäintä ja "game_over" ehto on täyttynyt tallennetaan pisteet ja lopetetaan renderöinti.

    if event.key != 1 and game_over: # game over, save score
                    save_score(score,hit_accuracy,today)
                    running = False # LOPETETAAN RENDERÖINTI 

## Pelilogiikka

### FPS
Pygame:ssa voidaan määrittää FPS (Frames per second), mikä kertoo kuinka usein ruutua päivitetään. Tämä on hyvä määrittää mikäli sillä on vaikutusta pelin toimivuuteen. Target practice:ssa ohjelman tulee koko ajan tarkistaa missä hiiri sekä maalitaulu sijaitsevat. Tällöin pieni FPS (testattu 30) ei riitä päivittämään hiiren sijainti tarpeeksi nopeasti, jolloin maalitaulua klikatessa hiiren sijainti ei ole päivittynyt oikeille kordinaateilla.

    FPS = 60 # ENOUGH FPS TO HANDLE MOUSE INPUT


## Kuvat ja musiikki
[Assets](https://github.com/wepukka/PyGame/tree/main/assets) kansioissa sijaitsee pelissä käytettävät kuvat ja musiikit. Valikkojen nappulat ja pelin maalitaulu on tehty [Piskelillä](https://www.piskelapp.com/), missä niiden korkeus ja leveys voidaan määrittää pikseleinä ja näin ei tarvinnut miettiä skaalausta pelin sisällä.

Musiikki joka pyörii pelin aikana on ladattu [free-stock-music.com](https://www.free-stock-music.com):sta ja kreditoitu [Readme](https://github.com/wepukka/PyGame/blob/main/README.md) tiedostossa.





# Käyttöönotto
Pelaamiseen vaaditaan tietokoneelle asennettu [Python](https://realpython.com/installing-python/), peli on tehty ja testattu käyttäen Python versiota 3.10.4.
Githubista tiedostojen lataamisen jälkeen riittää terminaalissa "pip install -r requirements.txt" komennon ajaminen.
Mikäli halutaan asentaa tarvittavat kirjastot erikseen voidaan ajaa "python3 -m pip install -U pygame --user" ja "pip install tinydb" 

# Linkkejä


#
[Päävalikko](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L58-L104)
[Asetukset](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L106-L139)
[Peli](https://github.com/wepukka/PyGame/blob/main/main.py?plain1#L141-L184)
[database](main.py)
[pelifunktiot](TargetPractice.py)


