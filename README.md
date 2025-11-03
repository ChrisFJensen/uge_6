# uge_6
Dette er min implementation af ETL opgaven fra uge 6 i specialisterne
De nødvendige modules kan hentes fra requirements.txt
## Beskrivelse

Har skrevet modules og koder som gør det muligt at hente data fra enten en lokal csv eller fra en angivet API, og så uploade det til min MySQL server som jeg har oprettet.

## Datastruktur
Har beholdt så meget meget af dataen som de naturligt kommer fra csv'erne og har lavet de følgende ændringer til dataen.

### Brands
brands tabellen har 2 kolonner:
 - brand_id (primary key): int (unique)
 - brand_name: string

brand_id er en unik identifier for hvilket brand man arbejder med, brand_name gemmer navnet på brandet.

### Categories
Categories tabellen har 2 kolonner:
- category_id (primary key): int (unique)
- category_name : string

category_id er en unik identifier for hvilken kategory produkt tilhører. category_name gemmer navnet for kategorien.

### Products
products tabellen har 6 kolonner:
- product_id (primary key): int (unique)
- product_name : string
- brand_id (foreign key): int
- category_id (foreign key): int
- model_year: int
- list_price: float

Beskrivelse af kolonnerne:
- product_id er en unik identifier 
- product_name er navnet på produktet
- brand_id beskriver hvilket brand produktet tilhører 
- category_id beskriver hvilken kategory produktet tilhører.
- model_year beskriver hvilket år modellen er fra.
- list_price beskriver prisen på produktet.

### Stores
stores tabellen har 8 kolonner:
(undersøg mysql tabel)

- name er navnet på butikken
- phone er butikkens tlf nummer
- email er butikkens email adresse
- street er butikken adresse
- state er den stat hvor butikken ligger i
- zip_code er butikkens postnummer
- store_id er butikkens identifier

### Stocks
stocks tabellen har 3 kolonner:
mysql tabel
- store_id er identifier for hvilken butik
- product_id er en identifier for hvilket produkt
- quantity er hvor mange genstande på lager
### Staffs
Har fjernet store_name og street, og har istedet indsat store_id som en foreign key, har derudover tilføjet en staff_id som identifier.
Staff_id er en primary key.

### Customers
customers tabellen har 9 kolonner:
tabel tid

- city er den by hvor kunden bor.
- customer_id er en unik identifier for hver kunde.
- email er kundens email.
- first_name er kundens fornavn.
- last_name er kundens efternavn.
- phone er kundens tlf nummer.
- stat er den stat hvor kunden bor.
- street er kundens adresse.
- zip_code er kundens postnummer.

### Orders
orders tabellen har 8 kolonner:
ikke mere opfindsom

- customer_id er identifier for hvilken kunde der har lagt ordren
- order_date er den dato hvor ordren er bestilt
- order_id er en unik identifier for hver order
- order_status er en indikator for ordrens status
    - 4 betyder afsendt
    - 1,2,3 vides ikke endnu
- required_date er en dato med uvidst mening.
- shipped_data er dato hvor ordren er afsendt fra butikken.
- staff_id er en identifier for hvilken ansat der har lavet salget.
- store_id er en identifier for hvilken butik der har lavet salget.

### Order_items
har fjernet list price. Order_id & product id er foreign keys.


## Klasser

### Connector
For at køre programmet skal man først definere en connector class object ved brug af connector. Connectoren initaliseres med user,password,host og database, hvor database er optional. Derudover har Connector klassen følgende funktioner:
- Opret og Luk forbindelse til server
- Tjek forbindelse
- Opret Databaser
- Skift nuværende database
- slet nuværende database
- Opret tabel(ler) fra SQL Script
- se tabeller i database

### Extractor
Er en klasse som extractor data fra forskellige kilder og returnerer dem i en pandas dataframe. Klassen har 3 funktioner, extract_api, extract_csv & extract_sql, men extract_sql er ej implementeret endnu.

Extract_api tager som input en url til en API, eller navnet på en af de 3 datasæt fra opgaven ("orders","order_items","customer") og henter det til en pandas dataframe ved at bruge python request pakke.

extract_csv tager som input en filpath til en csv fil og indlæser det til en pandas dataframe.

### Transformer
Transformer er en klasse som defineres med en connector. Derudover har transformer en enkelt funktion som tager en pandas dataframe og tabelnavn som input og giver en pandas dataframe retur. Tabelnavnet bliver brugt til at transformere dataen korrekt.

### Loader
Transformer er en klasse som defineres med en connector. Klassen har en funktion som hedder load_data. load_data tager en pandas dataframe & tabelnavn som input, og loader dataen til serveren, returner true hvis lykkedes.