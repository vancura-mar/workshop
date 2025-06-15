# Technická dokumentace - Záchrana včel (Bee Saver)

## 1. Základní třídy

### 1.1 GameObject (game_object.py)

Základní třída pro všechny herní objekty. Tato třída poskytuje základní funkcionalitu pro pozicování, pohyb a vykreslování herních objektů.

#### Atributy
- `x` (int): X-ová souřadnice objektu
- `y` (int): Y-ová souřadnice objektu
- `width` (int): Šířka objektu
- `height` (int): Výška objektu
- `color` (tuple): RGB barva objektu (výchozí: černá)
- `speed_y` (int): Rychlost pohybu ve směru Y (výchozí: 0)
- `rect` (pygame.Rect): Obdélník pro kolizní detekci
- `image` (pygame.Surface): Obrázek objektu (volitelný)

#### Metody

##### `__init__(self, x, y, width, height, color=(0, 0, 0), speed_y=0, image=None)`
Inicializuje nový herní objekt.

**Parametry:**
- `x` (int): Počáteční X-ová souřadnice
- `y` (int): Počáteční Y-ová souřadnice
- `width` (int): Šířka objektu
- `height` (int): Výška objektu
- `color` (tuple): RGB barva objektu
- `speed_y` (int): Rychlost pohybu ve směru Y
- `image` (pygame.Surface): Obrázek objektu

##### `update(self)`
Aktualizuje pozici objektu. Přidává `speed_y` k Y-ové souřadnici a aktualizuje kolizní obdélník.

##### `draw(self, screen)`
Vykreslí objekt na obrazovku.

**Parametry:**
- `screen` (pygame.Surface): Plocha pro vykreslování

**Chování:**
- Pokud je nastaven `image`, vykreslí obrázek
- Jinak vykreslí obdélník s nastavenou barvou

##### `is_off_screen(self, screen_height)`
Kontroluje, zda je objekt mimo spodní okraj obrazovky.

**Parametry:**
- `screen_height` (int): Výška obrazovky

**Návratová hodnota:**
- `bool`: True, pokud je objekt mimo obrazovku

#### Příklad použití
```python
# Vytvoření nového objektu
objekt = GameObject(x=100, y=100, width=50, height=50, color=(255, 0, 0))

# Aktualizace pozice
objekt.update()

# Vykreslení na obrazovku
objekt.draw(screen)

# Kontrola, zda je objekt mimo obrazovku
if objekt.is_off_screen(screen_height=600):
    # Objekt je mimo obrazovku
    pass
```

#### Dědičnost
Tato třída slouží jako základ pro všechny herní objekty. Ostatní třídy jako `Player`, `Bee`, `Wasp`, `Hive` a `Honey` dědí z této třídy a rozšiřují její funkcionalitu.

### 1.2 Player (player.py)

Třída reprezentující hráče (včelaře). Hráč se pohybuje pouze horizontálně po spodní hraně obrazovky a sbírá padající včely.

#### Atributy
- `x` (int): X-ová souřadnice včelaře
- `y` (int): Y-ová souřadnice včelaře (vždy na spodní hraně obrazovky)
- `width` (int): Šířka včelaře (výchozí: 50)
- `height` (int): Výška včelaře (výchozí: 50)
- `speed` (int): Rychlost pohybu (výchozí: 5)
- `lives` (int): Počet životů (výchozí: 3)
- `score` (int): Skóre hráče
- `rect` (pygame.Rect): Kolizní obdélník
- `color` (tuple): Barva včelaře (žlutá)
- `screen_height` (int): Výška obrazovky
- `stunned_until` (float): Čas do kdy je hráč omráčen
- `bee_buffer` (int): Aktuální počet včel v zásobníku
- `bee_buffer_max` (int): Maximální kapacita zásobníku včel (výchozí: 5)

#### Metody

##### `__init__(self, x, y, width=50, height=50, speed=5, screen_height=800)`
Inicializuje nového včelaře.

**Parametry:**
- `x` (int): Počáteční X-ová souřadnice
- `y` (int): Počáteční Y-ová souřadnice
- `width` (int): Šířka včelaře
- `height` (int): Výška včelaře
- `speed` (int): Rychlost pohybu
- `screen_height` (int): Výška obrazovky

##### `is_stunned(self)`
Kontroluje, zda je včelař momentálně omráčen.

**Návratová hodnota:**
- `bool`: True, pokud je včelař omráčen

##### `move(self, dx, screen_width, max_x=None)`
Pohybuje včelařem horizontálně po spodní hraně obrazovky.

**Parametry:**
- `dx` (int): Směr pohybu (-1 pro vlevo, 1 pro vpravo)
- `screen_width` (int): Šířka obrazovky
- `max_x` (int, optional): Maximální X-ová souřadnice

**Chování:**
- Včelař se nemůže pohybovat, pokud je omráčen
- Pohyb je omezen na hranice obrazovky
- Y-ová pozice zůstává konstantní na spodní hraně

##### `draw(self, screen)`
Vykreslí včelaře na obrazovku.

**Parametry:**
- `screen` (pygame.Surface): Plocha pro vykreslování

#### Příklad použití
```python
# Vytvoření nového včelaře
vcelar = Player(x=400, y=0, screen_height=800)

# Pohyb včelaře doprava
vcelar.move(1, screen_width=800)

# Kontrola omráčení
if vcelar.is_stunned():
    print("Včelař je omráčen!")

# Vykreslení včelaře
vcelar.draw(screen)
```

#### Poznámky
- Včelař se pohybuje pouze horizontálně
- Y-ová pozice je vždy fixována na spodní hraně obrazovky
- Včelař má omezený počet životů
- Systém zásobníku včel umožňuje sbírat více včel najednou
- Omráčení dočasně znemožňuje pohyb

### 1.3 Bee (bee.py)

Třída reprezentující včelu v hře. Včela padá shora dolů a může být zachráněna včelařem. Dědí z třídy `GameObject`.

#### Atributy
Dědí všechny atributy z `GameObject`:
- `x` (int): X-ová souřadnice včely
- `y` (int): Y-ová souřadnice včely
- `width` (int): Šířka včely (40)
- `height` (int): Výška včely (40)
- `color` (tuple): Barva včely (světle žlutá)
- `speed_y` (int): Rychlost pádu (výchozí: 4)
- `rect` (pygame.Rect): Kolizní obdélník
- `image` (pygame.Surface): Obrázek včely

#### Metody

##### `__init__(self, screen_width, max_x=None, speed_y=4)`
Inicializuje novou včelu. Včela se náhodně objeví na horní hraně obrazovky a začne padat dolů.

**Parametry:**
- `screen_width` (int): Šířka obrazovky
- `max_x` (int, optional): Maximální X-ová souřadnice pro spawn včely
- `speed_y` (int): Rychlost pádu včely

**Chování:**
- Načte sprite včely z assets/bees.png
- Nastaví náhodnou X-ovou pozici
- Y-ová pozice začíná nad obrazovkou
- Sprite je načten ze spritesheetu a škálován na požadovanou velikost

#### Příklad použití
```python
# Vytvoření nové včely
vcelicka = Bee(screen_width=800)

# Vytvoření včely s omezeným rozsahem spawnu
vcelicka_omezena = Bee(screen_width=800, max_x=400)

# Vytvoření včely s vlastní rychlostí pádu
vcelicka_rychla = Bee(screen_width=800, speed_y=6)
```

#### Poznámky
- Včela se spawnuje náhodně na horní hraně obrazovky
- Používá sprite z assets/bees.png
- Sprite je načten ze spritesheetu (4 včely v jednom obrázku)
- Včela padá konstantní rychlostí dolů
- Dědí základní funkcionalitu z GameObject (update, draw, is_off_screen)

### 1.4 Wasp (wasp.py)

Třída reprezentující vosu v hře. Vosa padá shora dolů a představuje nebezpečí pro včelaře. Dědí z třídy `GameObject`.

#### Atributy
Dědí všechny atributy z `GameObject`:
- `x` (int): X-ová souřadnice vosy
- `y` (int): Y-ová souřadnice vosy
- `width` (int): Šířka vosy (15)
- `height` (int): Výška vosy (15)
- `color` (tuple): Barva vosy (tmavá)
- `speed_y` (int): Rychlost pádu (výchozí: 5)
- `rect` (pygame.Rect): Kolizní obdélník

#### Metody

##### `__init__(self, screen_width, max_x=None, speed_y=5)`
Inicializuje novou vosu. Vosa se náhodně objeví na horní hraně obrazovky a začne padat dolů.

**Parametry:**
- `screen_width` (int): Šířka obrazovky
- `max_x` (int, optional): Maximální X-ová souřadnice pro spawn vosy
- `speed_y` (int): Rychlost pádu vosy

**Chování:**
- Nastaví náhodnou X-ovou pozici
- Y-ová pozice začíná nad obrazovkou
- Vosa padá rychleji než včela (výchozí rychlost: 5)

#### Příklad použití
```python
# Vytvoření nové vosy
vosa = Wasp(screen_width=800)

# Vytvoření vosy s omezeným rozsahem spawnu
vosa_omezena = Wasp(screen_width=800, max_x=400)

# Vytvoření vosy s vlastní rychlostí pádu
vosa_rychla = Wasp(screen_width=800, speed_y=7)
```

#### Poznámky
- Vosa se spawnuje náhodně na horní hraně obrazovky
- Je menší než včela (15x15 pixelů)
- Padá rychleji než včela (výchozí rychlost: 5)
- Při kolizi s včelařem způsobuje ztrátu životů
- Dědí základní funkcionalitu z GameObject (update, draw, is_off_screen)

### 1.5 Hive (hive.py)

Třída reprezentující úl v hře. Úl je umístěn v pravém dolním rohu obrazovky a slouží jako cíl pro zachráněné včely. Dědí z třídy `GameObject`.

#### Atributy
Dědí všechny atributy z `GameObject`:
- `x` (int): X-ová souřadnice úlu (pravý okraj obrazovky)
- `y` (int): Y-ová souřadnice úlu (spodní okraj obrazovky)
- `width` (int): Šířka úlu (výchozí: 50)
- `height` (int): Výška úlu (výchozí: 60)
- `color` (tuple): Barva úlu (hnědá)
- `rect` (pygame.Rect): Kolizní obdélník

Další atributy:
- `bee_buffer` (int): Aktuální počet včel v úlu
- `bee_buffer_max` (int): Maximální kapacita úlu (výchozí: 15)

#### Metody

##### `__init__(self, screen_width, screen_height, width=50, height=60)`
Inicializuje nový úl. Úl je umístěn v pravém dolním rohu obrazovky.

**Parametry:**
- `screen_width` (int): Šířka obrazovky
- `screen_height` (int): Výška obrazovky
- `width` (int): Šířka úlu
- `height` (int): Výška úlu

**Chování:**
- Nastaví pozici úlu do pravého dolního rohu
- Inicializuje zásobník včel na 0
- Nastaví maximální kapacitu úlu na 15 včel

#### Příklad použití
```python
# Vytvoření nového úlu
ul = Hive(screen_width=800, screen_height=600)

# Vytvoření většího úlu
velky_ul = Hive(screen_width=800, screen_height=600, width=70, height=80)
```

#### Poznámky
- Úl je statický objekt (nemá rychlost pohybu)
- Je umístěn v pravém dolním rohu obrazovky
- Slouží jako cíl pro zachráněné včely
- Má omezenou kapacitu (15 včel)
- Dědí základní funkcionalitu z GameObject (draw)
- Kolize s úlem znamená úspěšnou záchranu včely

### 1.6 Honey (honey.py)

Třída reprezentující med v hře. Med je bonusový předmět, který padá shora dolů a může být sebrán včelařem. Dědí z třídy `GameObject`.

#### Atributy
Dědí všechny atributy z `GameObject`:
- `x` (int): X-ová souřadnice medu
- `y` (int): Y-ová souřadnice medu
- `width` (int): Šířka medu (20)
- `height` (int): Výška medu (20)
- `color` (tuple): Barva medu (medová)
- `speed_y` (int): Rychlost pádu (výchozí: 4)
- `rect` (pygame.Rect): Kolizní obdélník

#### Metody

##### `__init__(self, screen_width, max_x=None, speed_y=4)`
Inicializuje nový med. Med se náhodně objeví na horní hraně obrazovky a začne padat dolů.

**Parametry:**
- `screen_width` (int): Šířka obrazovky
- `max_x` (int, optional): Maximální X-ová souřadnice pro spawn medu
- `speed_y` (int): Rychlost pádu medu

**Chování:**
- Nastaví náhodnou X-ovou pozici
- Y-ová pozice začíná nad obrazovkou
- Med padá stejnou rychlostí jako včela (výchozí: 4)

#### Příklad použití
```python
# Vytvoření nového medu
med = Honey(screen_width=800)

# Vytvoření medu s omezeným rozsahem spawnu
med_omezeny = Honey(screen_width=800, max_x=400)

# Vytvoření medu s vlastní rychlostí pádu
med_rychly = Honey(screen_width=800, speed_y=6)
```

#### Poznámky
- Med se spawnuje náhodně na horní hraně obrazovky
- Je menší než včela (20x20 pixelů)
- Padá stejnou rychlostí jako včela (výchozí: 4)
- Při kolizi s včelařem přidává bonusové body
- Dědí základní funkcionalitu z GameObject (update, draw, is_off_screen)

### 1.7 Game (game.py)

Hlavní třída hry, která řídí celý herní proces. Spravuje herní stav, zpracovává vstupy, aktualizuje pozice objektů a vykresluje herní scénu.

#### Atributy

##### Základní nastavení
- `width` (int): Šířka herního okna (výchozí: 500)
- `height` (int): Výška herního okna (výchozí: 800)
- `screen` (pygame.Surface): Herní plocha
- `clock` (pygame.time.Clock): Herní hodiny pro FPS
- `running` (bool): Stav běhu hry
- `fps` (int): Cílové FPS (60)

##### Herní objekty
- `player` (Player): Instance včelaře
- `hive` (Hive): Instance úlu
- `bees` (list): Seznam aktivních včel
- `wasps` (list): Seznam aktivních vos
- `honey` (Honey): Instance medu (pokud existuje)

##### Čítače a časovače
- `spawn_timer` (int): Čítač pro spawn včel
- `spawn_interval` (int): Interval spawnu včel (80 ticků)
- `wasp_spawn_timer` (int): Čítač pro spawn vos
- `wasp_spawn_interval` (int): Interval spawnu vos (160 ticků)

##### Stav hry
- `score` (int): Aktuální skóre
- `game_over` (bool): Stav konce hry
- `keys` (dict): Slovník stisknutých kláves
- `score_effect` (tuple): Efekt získání bodů
- `life_effect_end` (float): Čas konce efektu ztráty života

#### Metody

##### `__init__(self, width=500, height=800, title="Bee Saver")`
Inicializuje hru a vytváří herní okno.

**Parametry:**
- `width` (int): Šířka herního okna
- `height` (int): Výška herního okna
- `title` (str): Titulek herního okna

##### `reset(self)`
Resetuje herní stav do výchozího nastavení.

##### `handle_events(self)`
Zpracovává uživatelské vstupy a události.

**Zpracovává:**
- Uzavření okna
- Stisknutí kláves (ESC, R, ENTER)
- Pohyb včelaře (šipky, A/D)

##### `update(self)`
Aktualizuje herní stav.

**Provádí:**
- Aktualizaci pozice včelaře
- Spawn včel a vos
- Detekci kolizí
- Správu bodů a životů
- Kontrolu konce hry

##### `draw(self)`
Vykresluje herní scénu.

**Vykresluje:**
- Všechny herní objekty
- HUD (skóre, životy, zásobníky)
- Efekty (získání bodů, ztráta životů)
- Game Over obrazovku

##### `run(self)`
Spouští hlavní herní smyčku.

#### Příklad použití
```python
# Vytvoření a spuštění hry
game = Game(width=800, height=600)
game.run()
```

#### Herní mechaniky

##### Pohyb a ovládání
- Včelař se pohybuje horizontálně pomocí šipek nebo A/D
- Pohyb je omezen na levou stranu obrazovky a pravou stranu až k úlu

##### Bodový systém
- +1 bod za každou včelu doručenou do úlu
- Med přidává extra život
- Vosa způsobuje dočasné omráčení

##### Kolize
- Včelař + Včela: Sběr včely do zásobníku
- Včelař + Úl: Předání včel do úlu
- Včelař + Vosa: Omráčení
- Včelař + Med: Bonusový život

##### Game Over
- Hra končí při ztrátě všech životů
- Možnost restartu (R) nebo ukončení (ESC)

#### Poznámky
- Hra používá Pygame pro grafiku a vstupy
- Všechny herní objekty dědí z GameObject
- Herní logika je rozdělena do samostatných tříd
- Implementuje systém zásobníků pro včely
- Obsahuje vizuální efekty pro herní události

## 2. Vstupní bod aplikace

### 2.1 main.py

Vstupní bod aplikace, který inicializuje a spouští hru. Jednoduchý skript, který vytváří instanci hlavní herní třídy a spouští herní smyčku.

#### Struktura

```python
from core.game import Game

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
```

#### Funkce

##### `main()`
Hlavní funkce, která:
- Vytváří novou instanci hry s výchozími parametry
- Spouští herní smyčku

#### Spuštění hry
Hra se spustí při přímém spuštění souboru `main.py`. Výchozí nastavení:
- Šířka okna: 500 pixelů
- Výška okna: 800 pixelů
- Titulek: "Bee Saver"

#### Příklad spuštění
```bash
python main.py
```

#### Poznámky
- Soubor je navržen jako jednoduchý vstupní bod
- Všechna herní logika je implementována v třídě `Game`
- Při spuštění se automaticky inicializuje Pygame
- Hra se ukončí při stisknutí ESC nebo zavření okna
