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


