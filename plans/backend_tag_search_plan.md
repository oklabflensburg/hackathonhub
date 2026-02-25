# Backend-Änderungen für Tag-Suche

## 1. Datenbank-Änderungen
- Keine Schema-Änderungen erforderlich, da `technologies`-Feld bereits existiert
- Optional: Index auf `technologies` für bessere Suchperformance (falls viele Projekte)

## 2. Repository-Erweiterungen

### `ProjectRepository` neue Methoden:

```python
def get_by_technology(
    self, db: Session, technology: str, skip: int = 0, limit: int = 100
) -> List[Project]:
    """Get projects containing a specific technology."""
    # Case-insensitive partial match in comma-separated technologies
    return db.query(self.model).filter(
        self.model.is_public.is_(True),
        self.model.technologies.ilike(f"%{technology}%")
    ).order_by(
        self.model.created_at.desc()
    ).offset(skip).limit(limit).all()

def get_by_technologies(
    self, db: Session, technologies: List[str], skip: int = 0, limit: int = 100
) -> List[Project]:
    """Get projects containing ALL specified technologies (AND logic)."""
    query = db.query(self.model).filter(
        self.model.is_public.is_(True)
    )
    
    for tech in technologies:
        query = query.filter(self.model.technologies.ilike(f"%{tech}%"))
    
    return query.order_by(
        self.model.created_at.desc()
    ).offset(skip).limit(limit).all()
```

## 3. Service-Erweiterungen

### `ProjectService` neue Methoden:

```python
def get_projects_by_technology(
    self, db: Session, technology: str, skip: int = 0, limit: int = 100
) -> List[ProjectSchema]:
    """Get projects by technology."""
    projects = self.project_repo.get_by_technology(
        db, technology=technology, skip=skip, limit=limit
    )
    return [ProjectSchema.model_validate(p) for p in projects]

def get_projects_by_technologies(
    self, db: Session, technologies: List[str], skip: int = 0, limit: int = 100
) -> List[ProjectSchema]:
    """Get projects by multiple technologies."""
    projects = self.project_repo.get_by_technologies(
        db, technologies=technologies, skip=skip, limit=limit
    )
    return [ProjectSchema.model_validate(p) for p in projects]
```

## 4. API-Routen-Erweiterungen

### Änderung an `GET /projects`-Route:

Parameter hinzufügen:
- `technology: Optional[str] = None` (für einzelne Technologie)
- `technologies: Optional[str] = None` (kommagetrennte Liste für AND-Logik)

Route-Update:
```python
@router.get("", response_model=List[Project])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    user: Optional[int] = None,
    technology: Optional[str] = None,
    technologies: Optional[str] = None,
    db: Session = Depends(get_db),
    locale: str = Depends(get_locale)
):
    """Get all projects, optionally filtered by user or technology."""
    if technology:
        projects = project_service.get_projects_by_technology(
            db, technology=technology, skip=skip, limit=limit
        )
    elif technologies:
        tech_list = [t.strip() for t in technologies.split(",") if t.strip()]
        projects = project_service.get_projects_by_technologies(
            db, technologies=tech_list, skip=skip, limit=limit
        )
    elif user is not None:
        projects = project_service.get_projects(
            db, skip=skip, limit=limit, user_id=user
        )
    else:
        projects = project_service.get_projects(db, skip=skip, limit=limit)
    
    return projects
```

## 5. Testfälle

1. Einzelne Technologie-Suche: `GET /projects?technology=python`
2. Mehrere Technologien: `GET /projects?technologies=python,react`
3. Kombination mit anderen Filtern: `GET /projects?technology=python&user=1`
4. Leere Ergebnisse bei nicht vorhandener Technologie
5. Case-insensitive Suche

## 6. Performance-Überlegungen

- `LIKE '%value%'` ist nicht indexfreundlich, aber bei moderater Datenmenge akzeptabel
- Alternativ: Normalisierte Tag-Tabelle einführen (spätere Iteration)
- Caching von häufigen Suchanfragen erwägen

## 7. Abhängigkeiten

- Keine neuen Abhängigkeiten erforderlich
- Bestehende Tests aktualisieren