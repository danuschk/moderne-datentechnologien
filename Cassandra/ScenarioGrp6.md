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
    name text,
    city text,
    stars int,
    primary key (name, city)
);

insert into hotels (name, city, stars) values ('ibis Styles Aalen', 'Aalen', 3);
insert into hotels (name, city, stars) values ('ibis Stuttgart City', 'Stuttgart', 4);
insert into hotels (name, city, stars) values ('ibis Budget Stuttgart City Nord', 'Stuttgart', 4);
```

#### 2. Erstelle Zimmer mit Preis, zugehörigem Hotel und ob es belegt ist

```sql
create table rooms (
	nr int,
    hotel, text,
	beds int,
	price float,
	available boolean,
	features set<text>,
	primary key (nr, hotel, beds, price)
);

insert into rooms (nr, hotel, beds, price, available, features) values (1, 'ibis Styles Aalen', 1, 100.00, true, {'Vergolteter Toilettensitz', 'Klimaanlage'});
insert into rooms (nr, hotel, beds, price, available, features) values (2, 'ibis Styles Aalen', 1, 49.99, true, {'Klimaanlage'});
insert into rooms (nr, hotel, beds, price, available, features) values (3, 'ibis Styles Aalen', 1, 49.99, true, {'Klimaanlage'});
insert into rooms (nr, hotel, beds, price, available, features) values (4, 'ibis Styles Aalen', 2, 88.97, true, {'Klimaanlage'});
	
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

insert into guests (userid, joined, vorname, nachname, geburtstag) values (uuid(), now(), 'Moritz', 'Berger', '1998-07-24');
insert into guests (userid, joined, title, vorname, nachname) values (uuid(), now(), 'Prof. Dr.', 'Christian', 'Heinlein');

```

#### 4. Erstelle Buchungen mit einer Referenz auf Hotel, den Gast und das Zimmer, sowie Übernachtungszeitraum.

```sql
create table bookings ( 
    hotel text, 
    room int, 
    f timestamp, 
    t timestamp, 
    guest uuid, 
    primary key ((hotel, room), f, t, guest) 
) with clustering oder by (f asc, t asc, guest desc);

BEGIN BATCH
insert into bookings (hotel, room, guest, f, t) values ('ibis Styles Aalen', 1, 7745a39f-efda-4737-bceb-6e40e63e2d57, '2021-05-14', '2021-05-15');
insert into bookings (hotel, room, guest, f, t) values ('ibis Styles Aalen', 4, e12df9dc-9deb-404c-a5e1-f81526f41c54, '2021-06-01', '2021-07-01');
APPLY BATCH;
```

Mit `SELECT * FROM system_schema.columns WHERE keyspace_name = 'ex2'`
lassen sich alle erstellten Columns, mit der dazugehörigen Tabelle (Column Family) anzeigen.

#### 5. Queries

Finde alle Hotelzimmer des ibis Styles Aalen, für die für den heutigen 
Tag gebucht sind.

```
select room from bookings where hotel = 'ibis Styles Aalen' and f = toTimeStamp(toDate(now())) allow filtering;
```
