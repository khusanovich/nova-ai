gitGraph
    commit id: "Init main" tag: "origin/main"
    branch Dev
    commit id: "Dev setup"
    branch QA
    commit id: "QA tests"
    checkout Dev
    commit id: "Bugfix #12"
    branch feature/pdf-extractor
    commit id: "Add PDF extraction prototype"
    commit id: "Improve table parsing"
    checkout Dev
    merge feature/pdf-extractor tag: "Merge MR → Dev"
    checkout QA
    merge Dev tag: "QA approved"
    checkout main
    merge QA tag: "Release v1.0"

💡 So läuft der typische Workflow

Branch aus Dev erstellen → git checkout -b feature/pdf-extractor Dev

Code entwickeln & committen

Push auf GitLab → git push --set-upstream origin feature/pdf-extractor

Merge Request (MR) → von feature/pdf-extractor → Dev

Nach QA-Tests → Dev → QA → main

Kurze Zusammenfassung

| Ziel                             | Befehl                           |
| -------------------------------- | -------------------------------- |
| Remote prüfen                    | `git remote -v`                  |
| Alle Branches holen              | `git fetch --all`                |
| Remote-Branches sehen            | `git branch -a`                  |
| Remote-Branch lokal auschecken   | `git checkout -b Dev origin/Dev` |
| Unnötige lokale Branches löschen | `git branch -d dev1`             |
| Branch pushen (falls behalten)   | `git push origin dev1`           |



