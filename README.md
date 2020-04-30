# Nástroj pro detekci urbanistické scény
Tento nástroj vznikl jako součást bakalářské práce. Jedná se o program, který rozezná budovu na snímku a umístí na něj snímek budovy z databáze.

# Instalace
**potřebné knihovny**
- OpenCV [link](https://opencv.org/)
- Pillow [link](https://pypi.org/project/Pillow/)
- Numpy [link](https://numpy.org/)
- Pickle [link](https://docs.python.org/3/library/pickle.html)

Zdůvodu patentovaných metod SURF a SIFT je potřeba si naistalovat i OpenCV contribution verzi [link](https://pypi.org/project/opencv-contrib-python/). Případně je možné přejít na starší verzi OpenCV.

# Dataset
## Tvorba
## Struktura
Ukázka složkové struktury pro uchování předpočítaných příznaků a snímků budov

.  
+-- skripty                    - všechny skripty .py  
+-- data                       - adresář pro budovy  
    +-- metadata               - metadata budov ve formátu JSON  
    +-- b1                     - adresář budovy b1  
    |    +-- obrázky           - upravené snímky budovy b1  
    |    +-- deskriptory       - předpočítané příznaky b1  
    |    +-- klíčové body      - předpočítané budovy b1  
    +-- b1_original            - data pro vizualizaci budovy b1  
    +-- b2  
    +-- b2_original  


## Výpočet příznaků

### JSON

### Skript
Skript **JMÉNO** je určený pro výpočet příznaků všech budov v datasetu.
Skript **JMÉNO** je určený pro přegenerování JSON metadat všech budov.

# Dokumentace

## Třídy
------------------------------------------------------------------------------------------------  
### GPSLocation
#### Parametry
**latitude** - zeměpisná výška (ve stupních)  
**longtitude** - zeměpisná délka (ve stupních)  
#### Metody
##### get_latitude()  
##### get_longtitude()  
##### check_if_belongs(Image, Building)
Statická metoda, která zjistí, zda jde budova z databáze v okolí od místa pořízení fotografie. Návratová hodnota je boolean.
Proměnná ``radius=0.003`` je velikost radiusu.
```python
@staticmethod  
def check_if_belongs(input_img, db_building):  
    radius = 0.003  # in degrees => 300m radius
    # (x - center_x)^2 + (y - center_y)^2 < radius^2  
    if (pow(db_building.get_longtitude() - input_img.get_longtitude(), 2)
        + pow(db_building.get_latitude() - input_img.get_latitude(), 2)) <= (radius**2):  
        return True  
    else:  
        return False  
```
------------------------------------------------------------------------------------------------  
### CVSerializer
Třída ``CVSerializer`` se stará o převod klíčových bodů z OpenCV třídy ``cv2.Keypoint`` na slovník (a zpět), který může být serializován např. pomocí knihovny pickle.
#### Metody
##### cv_keypoint_to_dict(keypoints)
##### dict_to_cv_keypoint(keypoints)
------------------------------------------------------------------------------------------------   
### Image
#### Parametry
**path** - cesta ke snímku  
**img** - načtený obraz pomocí ``cv2.imread``  
**location** - gps lokace (GPSLocation)  
**keypoints** - klíčové body 
**descriptors** - příznaky
#### Metody
##### get_descriptor()
##### load_location()
##### get_longtitude()
##### get_latitude()
##### preprocess()
##### resize(max_dimension=960)
##### extract_features()  
##### merge_image()  
##### show()  
------------------------------------------------------------------------------------------------     
### Visualization
#### Parametry
**parametr**
#### Metody
##### metoda()
------------------------------------------------------------------------------------------------    
### Homography
#### Parametry
**parametr**
#### Metody
##### metoda()
------------------------------------------------------------------------------------------------   
### Building
#### Parametry
**parametr**
#### Metody
##### metoda()
------------------------------------------------------------------------------------------------   
### BuildingFeature
#### Parametry
**parametr**
#### Metody
##### metoda()
------------------------------------------------------------------------------------------------    
### BuildingRepository
#### Parametry
**parametr**
#### Metody
##### metoda()
------------------------------------------------------------------------------------------------    
### FeatureExtractor
#### Parametry
**parametr**
#### Metody
##### metoda()
------------------------------------------------------------------------------------------------   
### Matcher
#### Parametry
**parametr**
#### Metody
##### metoda()
------------------------------------------------------------------------------------------------    
### App
#### Parametry
**parametr**
#### Metody
##### metoda()
------------------------------------------------------------------------------------------------   
