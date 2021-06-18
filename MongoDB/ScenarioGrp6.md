# Vorlesung Modern Data Technologies - Exercise 3 (MongoDB)

### Gruppe 6

| Name          | Matr. Nr. |
|:------------- | ---------:|
| David Sugar   | 76050     |
| Moritz Berger | 76265     |
| Daniel Pawita | 70751     |

### Scenario

Sie benötigen eine Lösung für die Organisation Ihrer Projekte. Folgende Eigenschaften benötigt ein Projekt: 

* Einen Titel 
* Eine Deadline 
* Status des Projektes 
* Zugriffsschutz (Lesen/Schreiben)
* Aufgabenverteilung (Mit Priorität, Status und Deadline)
* Dateimanagement (Mit Tags)
  * Dateien, welche nur das Projekt hat 
  * Dateien, welche referenziert werden 

Um eine gute Übersicht über die IDs zu behalten, werden diese in den Beispielen vordefiniert. Den Autoren ist klar, dass dies kein optimales Vorgehen ist und manuelles setzten von ObjectIDs zu Kollisionen führen kann. Personen-IDs beginnen mit 0 und Projekte beginnen mit einer 1.

1. Alle Personen werden in ein eigenes Document Namens "persons" ausgelagert:

```
people = 
[
    { 
        "_id" : ObjectId("000000000000000000000001"), 
        "name" : "David Sugar", 
        "projects" : [ ] 
    },
    { 
        "_id" : ObjectId("000000000000000000000002"), 
        "name" : "Moritz Berger", 
        "projects" : [ ] 
    },
    { 
        "_id" : ObjectId("000000000000000000000003"), 
        "name" : "Daniel Pawlita", 
        "projects" : [ ] 
    }
]
db.persons.insert(people);
```

2. Für die Projekte wird ein Document "projects" angelegt: 

```
project1 = 
{
    "_id" : ObjectId("100000000000000000000001"),
    "title" : "Exercise 3",
    "due_date" : new Date("2021-06-11"),
    "status" : "finished",
    "access" : {
        "read" : [
            { 
                "id" : ObjectId("000000000000000000000001"), 
                "name" : "David Sugar" 
            },
            { 
                "id" : ObjectId("000000000000000000000002"), 
                "name" : "Moritz Berger" 
            },
            { 
                "id" : ObjectId("000000000000000000000003"), 
                "name" : "Daniel Pawlita" 
            }
            ],
        "write" : [
            { 
                "id" : ObjectId("000000000000000000000001"), 
                "name" : "David Sugar" 
            },
            { 
                "id" : ObjectId("000000000000000000000002"), 
                "name" : "Moritz Berger" 
            },
            { 
                "id" : ObjectId("000000000000000000000003"), 
                "name" : "Daniel Pawlita" 
            }
            ]
    },
    "tasks" : [
        { 
            "name" : "Read the Lecture Script", 
            "status" : "finished", 
            "assigned_to" : [ ObjectId("000000000000000000000001"), 
                ObjectId("000000000000000000000002"), 
                ObjectId("000000000000000000000003") ], 
            "due_date" : new Date("2021-06-01"), 
            "priority" : NumberInt(1) 
        },
        { 
            "name" : "Make up a valid scenario", 
            "status" : "finished", 
            "assigned_to" : [ ObjectId("000000000000000000000001") ], 
            "due_date" : new Date("2021-06-05"), 
            "priority" : NumberInt(2) 
        },
        { 
            "name" : "Write the queries", 
            "status" : "finished", 
            "assigned_to" : [ ObjectId("000000000000000000000002"), 
                ObjectId("000000000000000000000003") ], 
            "due_date" : new Date("2021-06-11"), 
            "priority" : NumberInt(3) 
        },
        { 
            "name" : "Check score", 
            "status" : "pending", 
            "assigned_to" : [ ], 
            "due_date" : null, 
            "priority" : NumberInt(1) 
        }
    ],
    "own_files" : [
        { "name" : "MDT Exercise3.pdf", "tags" : [ "MDT", "Exercise 3" ] },
        { "name" : "Lösung.md", "tags" : [ "Lösung" ] }
    ],
    "ref_files" : [
        { "name" : "04-Document Databases.pdf", 
            "location" : 
                "Hochschule Aalen/Semester 6/Moderne Datentechnologien/Skripte" }
    ]
}
db.projects.insert(project1);
```

Zweites Projekt: 

```
project2 = 
{
    "_id" : ObjectId("100000000000000000000002"),
    "title" : "Project ITS",
    "due_date" : new Date("2021-07-14"),
    "status" : "working",
    "access" : {
        "read" : [
            { "id" : ObjectId("000000000000000000000003"), 
                "name" : "Daniel Pawlita" }
            ],
        "write" : [
            { "id" : ObjectId("000000000000000000000003"), 
                "name" : "Daniel Pawlita" }
            ]
    },
    "tasks" : [
        { "name" : "Research Topic", "status" : "finished", 
            "assigned_to" : [ ObjectId("000000000000000000000001") ], 
            "due_date" : new Date("2021-03-15"), 
            "priority" : NumberInt(1) },
        { "name" : "Write down Roadmap", "status" : "finished", 
            "assigned_to" : [ ObjectId("000000000000000000000001") ], 
            "due_date" : new Date("2021-03-20"), "priority" : NumberInt(2) },
        { "name" : "Analyze Algorithm", "status" : "working", 
            "assigned_to" : [ ObjectId("000000000000000000000001") ], 
            "due_date" : new Date("2021-04-10"), "priority" : NumberInt(3) },
        { "name" : "Write Report", "status" : "working", 
            "assigned_to" : [ ObjectId("000000000000000000000001") ], 
            "due_date" : new Date("2021-07-01"), "priority" : NumberInt(4) }
    ],
    "own_files" : [
        { "name" : "Algorithm Description.pdf", "tags" : [ "Algorithm", "Description", "PDF" ] },
        { "name" : "Project Report.tex", "tags" : [ "Latex", "Report" ] }
    ],
    "ref_files" : [
        { "name" : "04-Document Databases.pdf", 
            "location" : "Hochschule Aalen/Semester 6/Moderne Datentechnologien/Skripte" }
    ]
}
db.projects.insert(project2);
```

Zur Erklärung: 

* Der String "name" im Document "access" ist Denormalisiert. 
  Der Grund dafür ist, dass alle wichtigen Projektdaten mit einer Abfrage zur Verfügung stehen sollen. 
  Damit spart man sich eine N-N-Abfrage. 
* Die ObjectId "id" im Document "access" ist zur eindeutigen Bestimmung der Personen gedacht, da es Namensdoppelungen geben kann. 
* Die Einträge in "assigned_to" im Document "tasks" sind Normalisiert, da die Namen der Personen bereits mit dem document "access" dabei sind. 

### Queries

1. Aktualisieren des Personen-Documents von Pawlita mit den beiden Project-Referenzen: 

```
db.persons.update({"_id" : ObjectId("000000000000000000000001")}, 
    { "$addToSet" : {"projects" : 
        { $each: [ "100000000000000000000001", 
            "100000000000000000000002" ]}}});
```

2. Die Deadline vom Projekt "Projekt ITS" ändern: 
   
   ```
   db.projects.update(
    {
        "title" : "Project ITS"
    },
    {
        "$set" : {  
            "due_date" : new Date("2021-07-15")
        }
    }
   );
   ```

3. Einen neuen Task zu "Project ITS" hinzufügen:
   
   ```
   db.projects.update(
    { 
        "title" : "Project ITS"
    },
    {
        "$push" : { 
            "tasks" : { 
                "name" : "Quellenverzeichnis prüfen", 
                "status" : 
                "pending", 
                "assigned_to" : 
                    [ 
                        ObjectId("000000000000000000000001") 
                    ], 
                    "due_date" : new Date("2021-06-30"), 
                    "priority" : NumberInt(2) } 
        }
    }
   );
   ```

4. Eine Reihe an Dateien dem Projekt "Exercise 3" hinzufügen:

```
db.projects.update(
    {
        "title" : "Exercise 3"
    },
    { "$push" : { 
        "own_files" : {
            "name" : "Zwischenstand.md", 
            "tags" : [ "Stand" ]
        }
    }}
);
```

5. Auflistung aller zu einer Person zugewiesenen Tasks. Es soll der Projektname, Taskname und Deadline ausgegeben werden und nach Datum aufsteigend sortiert werden:

```
db.projects.aggregate([
    {
        "$unwind" : { "path" : "$tasks"} 
    },
    {
        "$match" : { "tasks.assigned_to" : ObjectId("000000000000000000000001"), 
            "tasks.status" : { "$in" : [ "working" ] } }
    },
    {
        "$project" : {
            "tasks" : {
                "name" : 1,
                "due_date" : 1
            },
        "title" : 1,
        "_id" : 0
        }
    },
    {
        "$sort" : { "tasks.due_date" : 1 } 
    }
]).pretty();
```
