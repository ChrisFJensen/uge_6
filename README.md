# uge_6
Dette er min implementation af ETL opgaven fra uge 6 i specialisterne
De nødvendige modules kan hentes fra requirements.txt
## Beskrivelse

Har skrevet modules og koder som gør det muligt at hente data fra enten en lokal csv eller fra en angivet API, og så uploade det til min MySQL server som jeg har oprettet.

## Datastruktur
Har beholdt så meget meget af dataen som de naturligt kommer fra csv'erne og har lavet de følgende ændringer til dataen.

### Brands
Har samme struktur som fra CSV'en, hvor brand_id er en primary key

### Categories
Har samme struktur som fra CSV'en, hvor category_id er en primary key

### Products
Har samme struktur som fra CSV'en, har product_id som primary key og 
category_id & brand_id er foreign key

### Stores
Har tilføjet en store_id som identifier, ellers er det samme som i CSV'en
Store_id er en primary key.
### Stocks
Har ændret store_name til store_id ellers samme som fra CSV'en
store_id er en foreign key
### Staffs
Har fjernet store_name og street, og har istedet indsat store_id som en foreign key, har derudover tilføjet en staff_id som identifier.
Staff_id er en primary key.

### Customers
Har ikke gjort noget ved dette datasæt, har customer_id som er en primary key

### Orders
Har ændret staff_name og store_name til deres id'er og konverterer datoerne fra ddmmyyyy til yyyymmdd.
Order_id er en primary key, store_id,staff_id og customer_id er foreign keys.
Det skal bemærkes at under transformationen så bliver nogle af de datoer der mangler lavet om til NaT, hvilket SQL kan håndtere men ved ikke om det anses som værende det samme som null.
### Order_items
har fjernet list price. Order_id & product id er foreign keys.


## Kørsel
For at køre programmet skal man først definere en connector class object ved brug af connector, hvor man kan angive forskellige værdier for at forbinde til sin server.
Man skal dærnest åbne en forbindelse med connector.connect(), og hvis man ikke allerede har gjort det kan man vælge database på serveren med .choose_db() eller lave en ny med .create_db()

Når den er åben kan man så kalde load_data_to_db(table_names, connector) som automatisk indlæser data ind på SQL serveren baseret på den data som bliver angivet ved table_names