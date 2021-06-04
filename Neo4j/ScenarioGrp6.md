# Vorlesung Modern Data Technologies - Exercise 4 (Neo4j)

### Gruppe 6

| Name | Matr. Nr. |
|:-----|----------:|
| David Sugar | 76050 |
| Moritz Berger| 76265 |
| Daniel Pawita| 70751 |

### Scenario

Sie entwickeln für den Posaunenchor XYZ eine Eventmanagement Applikation. In
dieser soll der Verein seine Auftritte verwalten können. Mitglieder können
mehreren Gruppen (Stimmen) z.B. erste Stimme, Bass, etc. zugewiesen sein und
pro Auftritt für eine dieser Positionen zusagen. Sie
wollen sich die Möglichkeit offen halten, die Applikation später global
anzubieten und sind sich bewusst, dass die Daten durch ihre Verknüpfungen
untereinander definiert sind und entscheiden sich deswegen für die Neo4j
Grafdatenbank. Dabei wurden Teile des Backends bereits fertiggestellt.

* Ein Verein/ Team besteht aus Gruppen, denen Mitglieder zugewiesen sind.
  Mitglieder müssen dabei nicht unbedingt einer Gruppe angehören und Gruppen
  müssen umgekehrt auch keine Mitglieder enthalten.
* Erstelle einen Verein mit Gruppen und mehreren Mitgliedern.
* Speichere die Verbindungen der Knoten untereinander: Teams sind in Gruppen
  eingeteilt und Mitglieder sind sowohl dem Team als auch mind. einer Gruppe
  zugeordnet.

```
CREATE 
    (ersteStimme:Group {name: "Erste Stimme"}), 
    (zweiteStimme:Group {name: "Zweite Stimme"}), 
    (bass:Group {name: "Bass"}), 
    (sarah:Member {name: "Sarah"}), 
    (david:Member {name: "David"}), 
    (franzi:Member {name: "Franzi"}), 
    (tobias:Member {name: "Tobias"}), 
    (pc:Team {name: "Posaunenchor XYZ"}), 
    (ersteStimme)-[:BELONGS_TO]->(pc), 
    (zweiteStimme)-[:BELONGS_TO]->(pc), 
    (bass)-[:BELONGS_TO]->(pc), 
    (sarah)-[:MEMBER_OF]->(pc), 
    (david)-[:MEMBER_OF]->(pc), 
    (franzi)-[:MEMBER_OF]->(pc), 
    (tobias)-[:MEMBER_OF]->(pc), 
    (sarah)-[:ASSIGNED_TO]->(ersteStimme), 
    (franzi)-[:ASSIGNED_TO]->(ersteStimme), 
    (tobias)-[:ASSIGNED_TO]->(zweiteStimme), 
    (david)-[:ASSIGNED_TO]->(zweiteStimme), 
    (david)-[:ASSIGNED_TO]->(bass)
```

* Erstelle als nächstes zwei Auftritte für den Verein mit einem Ort, sowie 
  einer Anfangs- und Endzeit.
* Stelle die Zusagen der Mitglieder als Verknüpfungen dar.

```
CREATE 
(event1:Event {name: "Event 1", 
    location: "Aalen", 
    start: datetime('2021-06-06T11:30:00'), 
    duration: duration({hours: 1, minutes: 30})}),
(event2:Event {name: "Event 2", 
    location: "Stuttgart", 
    start: datetime('2021-06-13T14:15:00'), 
    duration: duration({hours: 2, minutes: 15})})
```

```
MATCH (franzi:Member {name: "Franzi"}) 
MATCH (sarah:Member {name: "Sarah"}) 
MATCH (david:Member {name: "David"}) 
MATCH (tobias:Member {name: "Tobias"}) 
MATCH (ersteStimme:Group {name: "Erste Stimme"}) 
MATCH (zweiteStimme:Group {name: "Zweite Stimme"}) 
MATCH (bass:Group {name: "Bass"})  
MATCH (event1:Event {name: "Event 1"}) 
MATCH (event2:Event {name: "Event 2"}) 
CREATE
    (franzi)-[:CONFIRMS]->(fa:Assignment)<-[:FOR]-(ersteStimme), 
    (event1)-[:ASSIGNED]->(fa),
    (david)-[:CONFIRMS]->(fd:Assignment)<-[:FOR]-(bass), 
    (event1)-[:ASSIGNED]->(fd),
    (tobias)-[:CONFIRMS]->(ft:Assignment)<-[:FOR]-(zweiteStimme), 
    (event1)-[:ASSIGNED]->(ft),
    (sarah)-[:CONFIRMS]->(sa:Assignment)<-[:FOR]-(ersteStimme), 
    (event2)-[:ASSIGNED]->(sa),
    (david)-[:CONFIRMS]->(fd:Assignment)<-[:FOR]-(zweiteStimme), 
    (event2)-[:ASSIGNED]->(fd),
    (tobias)-[:CONFIRMS]->(ft:Assignment)<-[:FOR]-(zweiteStimme), 
    (event2)-[:ASSIGNED]->(ft)
```

* Lassen Sie sich die Namen aller Mitglieder anzeigen, 
  die an einem der erstellten Events teilnehmen, sowie die Gruppe
  in der sie spielen.

```
MATCH (members:Member)-[:CONFIRMS]->(a:Assignment)<-[ASSIGNED]-(:Event {name: "Event 1"}) 
MATCH (a)<-[:FOR]-(g:Group) 
return members.name as Name, g.name as Group
```

* Zählen Sie die Mitglieder eines der Teams.


