# Lecture Modern Data Technologies - Exercise 2 (Cassandra)

### Group 6

| Name | Matr. Nr. |
|:-----|----------:|
| David Sugar | 76050 |
| Moritz Berger| 76265 |
| Daniel Pawita| 70751 |

### Scenario

Eine Hotelkette mit mehreren Standorten in ganz Europa möchte ein einheitliches
Buchungssystem implementieren. Dazu soll im Backend der Cassandra Wide Column
Store verwendet werden.

- Es sollen Column Families für Gäste, Hotel, Zimmer und Buchung in der Datenbank angelegt werden.

- Buchungen sollen jeweils dem Gast, dem besuchten Hotel und dem gebuchten Zimmer zugeordnet werden können.

- Hotelzimmer werden jedem Hotel zugewiesen mit einem Status ob das Zimmer
  derzeit belegt ist etc.

#### 1. Erstelle Hotels mit Namen, Ort und Sternen

Zuerst muss ein neuer Keyspace erzeugt werden.
```sql
CREATE KEYSPACE ex2
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : '1'};
USE ex2;
```

Als nächstes muss die Hotel Column Family angelegt und einige Einträge
hinzugefügt werden.
```sql
create table hotels (
    city text,
    name text,
    stars int,
    primary key (city, name, stars)
);

```

#### 2. Erstelle Zimmer mit Preis, zugehörigem Hotel und ob es belegt ist

```sql
create table rooms (
	nr int,
    hotel text,
	beds int,
	price float,
	available boolean,
	features set<text>,
	primary key (hotel, beds, price)
);

```

#### 3. Erstelle Gäste mit Name und Anschrift

```sql
CREATE TABLE guests (
	userid uuid,
	joined timeuuid,
	titel text,
	vorname text,
	nachname text,
	geburtstag date,
	PRIMARY KEY (userid, joined)	
);

create index lname on guests(nachname);

```

#### 4. Erstelle Buchungen mit einer Referenz auf Hotel, den Gast und das Zimmer, sowie Übernachtungszeitraum.

```sql
create table bookings (
    hotel text, 
    f timestamp, 
    t timestamp, 
    room int, 
    guest uuid, 
    primary key (hotel, f, t) 
);

create index guest on bookings(guest);

```

```
BEGIN BATCH
insert into hotels (name, city, stars) 
values ('ibis Styles Aalen', 'Aalen', 3);
insert into hotels (name, city, stars) 
values ('ibis Stuttgart City', 'Stuttgart', 4);
insert into hotels (name, city, stars) 
values ('ibis Budget Stuttgart City Nord', 'Stuttgart', 4);

insert into rooms (nr, hotel, beds, price, available, features) 
values (1, 'ibis Styles Aalen', 1, 100.00, true, {'Vergolteter Toilettensitz', 'Klimaanlage'});
insert into rooms (nr, hotel, beds, price, available, features) 
values (2, 'ibis Styles Aalen', 1, 49.99, true, {'Klimaanlage'});
insert into rooms (nr, hotel, beds, price, available, features) 
values (3, 'ibis Styles Aalen', 1, 49.99, true, {'Klimaanlage'});
insert into rooms (nr, hotel, beds, price, available, features) 
values (4, 'ibis Styles Aalen', 2, 88.97, true, {'Klimaanlage'});
insert into rooms (nr, hotel, beds, price, available, features) 
values (1, 'ibis Stuttgart City', 1, 37.97, true, {});
insert into rooms (nr, hotel, beds, price, available, features) 
values (2, 'ibis Stuttgart City', 2, 75.94, true, {'Meerblick'});
insert into rooms (nr, hotel, beds, price, available, features) 
values (1, 'ibis Budget Stuttgart City Nord', 1, 12.94, true, {});

insert into guests (userid, joined, vorname, nachname, geburtstag) 
values (uuid(), now(), 'Moritz', 'Berger', '1998-07-24');
insert into guests (userid, joined, title, vorname, nachname) 
values (uuid(), now(), 'Prof. Dr.', 'Christian', 'Heinlein');
insert into guests (userid, joined, vorname, nachname) 
values (uuid(), now(), 'David', 'Sugar');

insert into bookings (hotel, room, guest, f, t) 
values ('ibis Styles Aalen', 1, 7745a39f-efda-4737-bceb-6e40e63e2d57, '2021-05-14', '2021-05-15');
insert into bookings (hotel, room, guest, f, t) 
values ('ibis Styles Aalen', 4, e12df9dc-9deb-404c-a5e1-f81526f41c54, '2021-06-01', '2021-07-01');
insert into bookings (hotel, room, guest, f, t) 
values ('ibis Styles Aalen', 4, e12df9dc-9deb-404c-a5e1-f81526f41c54, '2021-12-31', '2022-01-01');
insert into bookings (hotel, room, guest, f, t) 
values ('ibis Stuttgart City', 1, 7745a39f-efda-4737-bceb-6e40e63e2d57, '2021-07-14', '2021-07-17');
insert into bookings (hotel, room, guest, f, t) 
values ('ibis Stuttgart City', 2, d5d37d20-c383-422b-ab78-a506356c75a5 , '2021-06-03', '2021-06-05');
APPLY BATCH;
```

Mit `SELECT * FROM system_schema.columns WHERE keyspace_name = 'ex2'`
lassen sich alle erstellten Columns, mit der dazugehörigen Tabelle (Column Family) anzeigen.

#### 5. Queries

1. Finde alle Hotelzimmer des ibis Styles Aalen, für die Gäste am heutigen
Tag (14.05.2021) anreisen, damit diese gereinigt werden können.

```
select room from bookings where hotel = 'ibis Styles Aalen' and f = toTimeStamp(toDate(now()));
```

2. Lassen Sie sich alle Räume mit 2 Betten unter 100.00 Euro anzeigen.

```
select * from rooms where hotel = 'ibis Styles Aalen' and beds = 2 and price < 100.0;
```

3. Lassen Sie sich alle Hotels in Stuttgart anzeigen.

```
select name, stars from hotels where city = 'Stuttgart';
```

4. Listens Sie für alle Hotels die Gesammtzahl der Buchungen auf.

```
select hotel, count(\*) as bookings from bookings group by hotel;
```

5. Finde alle Buchungen des Gastes mit dem Nachnamen Sugar.

```
select userid from guests where nachname = 'Sugar';

 userid
--------------------------------------
 d5d37d20-c383-422b-ab78-a506356c75a5

select * from bookings where guest = d5d37d20-c383-422b-ab78-a506356c75a5;
```

