# environnements .env
PGADMIN_EMAIL="admin@admin.com"
PGADMIN_PASSWORD="postgres"
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/ogtsync

# sicsogt commands pour lancer l'application
chmod +x scripts/build.sh
./scripts/build.sh
docker-compose up 

# nouvelles migrations (mila docker mande ireo)
docker-compose exec backend alembic revision --autogenerate -m "add news tables"
docker-compose exec backend alembic upgrade head


# ireto tsy atao fa commandes hafa:
# tuer le docker
docker-compose down -v

# remonter le docker
docker-compose up -d --build

# initiliaser alembic
docker-compose exec backend alembic init migrations 