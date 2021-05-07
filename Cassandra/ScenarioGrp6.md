# Lecture Modern Data Technologies - Exercise 1 (Redis)

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
	beds int,
	price int,
	available boolean,
	features set<text>,
	primary key (nr)
	);
	
insert into 
rooms (nr, beds, price, available, features)
values (1, 1, 100, true, {'Vergoldeter Toilettensitz', 'Klimaanlage'});
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

insert into 
guests (uuid, joined, vorname, nachname, geburtstag) 
values (uuid(), now(), Moritz, Berger, '1998-07-24');

insert into 
guests (uuid, joined, titel, vorname, nachname) 
values (uuid(), now, Prof. Dr, Christop, Heinlein);
```

#### 4. Erstelle Buchungen mit einer Referenz auf Hotel, den Gast und das Zimmer, sowie Übernachtungszeitraum

```sql
create table bookings ( 
    hotel text, 
    room int, 
    guest uuid, 
    f timestamp, 
    t timestamp, 
    primary key ((hotel, room), guest, f, t) 
);
```
