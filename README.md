# Nástroj pro detekci urbanistické scény
Tento nástroj vznikl jako součást bakalářské práce. Jedná se o program, který rozezná budovu na snímku a umístí na něj snímek budovy z databáze.

# Instalace
**potřebné knihovny**
- OpenCV [link](https://opencv.org/)
- Pillow [link](https://pypi.org/project/Pillow/)
- Numpy [link](https://numpy.org/)
- Pickle [link](https://docs.python.org/3/library/pickle.html)

Zdůvodu patentovaných metod SURF a SIFT je potřeba si naistalovat i OpenCV contribution verzi [link](https://pypi.org/project/opencv-contrib-python/). Případně je možné přejít na starší verzi OpenCV.

# Config
Soubor config.json obsahuje nastavitelné proměnné pro celou aplikaci. Je možné zde nastavit cesty vstupního obrazu, metadat a dalších parametrů. Soubor je generován skriptem [config.py](./config.py)

# Dataset
## Tvorba
Fotografie budov by měli být pořizovány za dobrých světelných podmínke s minimem stínů a rušivých elementů např. cedule, auta apod.

**TODO obrázek dobrých  a špatných fotek**

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
Pro výpočet příznaků je použit deskritor SIFT. Příznaky pro budovy v databázi jsou předpočítány pomocí skriptu [extract_features_db.py](./extract_features_db.py). Příznaky pro vstupní snímek jsou vypočítány v rámci běhu aplikace. O výpočet se stará třída **FeatureExtractor**

### JSON

### Skript
Skript **config.py** je určený pro generování config souboru
Skript **extract_features_db.py** je určený pro výpočet příznaků všech budov v datasetu.
Skript **json_data.py** je určený pro přegenerování JSON metadat všech budov.

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
### Config
#### Parametry
**path**
**data**
#### Metody
##### load()
##### get_metadata()
##### get_input_image()
##### get_gps_radius()
##### get_flann_matching_setup()
##### get_filter_features()
------------------------------------------------------------------------------------------------     
### Visualization
#### Metody
##### create_mask()
------------------------------------------------------------------------------------------------    
### Homography
#### Parametry
**H**
**keypoints1**
**keypoints2**
#### Metody
##### add_keypoints()
##### find_matrix()
##### warp_image()
##### merge_images()
------------------------------------------------------------------------------------------------   
### Building
#### Parametry
**id**
**location**
**name**
**path**
#### Metody
##### set_from_json()
##### get_longtitude()
##### get_latitude()
------------------------------------------------------------------------------------------------   
### BuildingFeature
#### Parametry
**id**
**path**
**original**
**img**
**keypoints**
**descriptor**
**matches**
#### Metody
##### load_image()
##### set_keypoints()
##### set_descriptor()
##### update_matches()
##### get_num_of_matches()
##### get_sum_of_matches()
##### sort_matches_by_distance()
------------------------------------------------------------------------------------------------    
### BuildingRepository 
#### Metody
##### get_all_buildings()
##### get_building_features()
------------------------------------------------------------------------------------------------    
### FeatureExtractor
#### Metody
##### extract_sift(img)
------------------------------------------------------------------------------------------------   
### Matcher
#### Parametry
**matcher**
#### Metody
##### set_sift_match()
##### match_sift()
##### ratio_test()
##### show_matches()
##### draw_matches()
##### best_match()
##### check_distances()
##### filter_out_close_keypoints()
------------------------------------------------------------------------------------------------    
### App
#### Parametry
**config**  
**img_in**  
**db_path**  
**building**  
**building_feature**  
**matcher**  
**matches**  
**warped_img**  
**sift** 
**surf**
**orb**
**best_match**  
#### Metody
##### load_buildings()
##### load_features()
##### load_image()
##### check_perimeter()
##### match_features()
##### find_best_match()
##### find_best_keypoints()
##### show_matches()
##### warp_image()
##### visualization()
------------------------------------------------------------------------------------------------   
