# Architecture Overview

This repository is a Django-based multi-app web platform that exposes several services through a single entrypoint. The core application is the `Train_Of_Thought` Django project, which routes traffic to feature apps, stores data in SQLite, and uses Redis for async messaging via Channels.

```mermaid
flowchart LR
    U[User / Browser] --> B[Web Frontend\nHTML, CSS, JS]
    B --> D[Django App\nTrain_Of_Thought]

    D --> R[URL Router\nTrain_Of_Thought/urls.py]
    R --> PS[personal_site\nLanding page / site content]
    R --> BL[Blog_app\nBlog service]
    R --> TD[to_do_list\nTask management]
    R --> CH[Chat\nRealtime chat / auth]

    D --> DB[(SQLite Database\ndb.sqlite3)]
    D --> ST[Static Assets / Templates]
    CH --> RC[Channels + Redis\nRedisChannelLayer]
    D --> ASGI[Daphne / ASGI Server]

    subgraph Deployment
        DC[Docker Compose]
        WEB[web container]
        REDIS[redis container]
    end

    DC --> WEB
    DC --> REDIS
    WEB --> D
    REDIS --> RC

    classDef app fill:#e6f4ff,stroke:#1f78b4,color:#111;
    classDef data fill:#e8f5e9,stroke:#2e7d32,color:#111;
    classDef infra fill:#fff3e0,stroke:#ef6c00,color:#111;

    class PS,BL,TD,CH app;
    class DB,ST data;
    class D,ASGI,RC,WEB,REDIS,DC infra;
```

## Component Summary

- `personal_site`: main site pages and public landing experience.
- `Blog_app`: blog-related routes and functionality.
- `to_do_list`: task-list application.
- `Chat`: chat feature using Django Channels with custom user support.
- `Train_Of_Thought`: Django project settings, routing, and integration layer.
- `db.sqlite3`: primary application database for local persistence.
- `Redis`: message broker used by Channels for real-time communication.
- `Docker Compose`: containerizes the web app and Redis service.

## Runtime Flow

1. Requests arrive from the browser to the Django app.
2. The main URL router forwards requests to the correct app.
3. App-level views and templates render the requested page or service.
4. Data is persisted in SQLite.
5. Realtime chat traffic is mediated through Redis via Django Channels.
6. The app is deployed in Docker using a web container and Redis container.
