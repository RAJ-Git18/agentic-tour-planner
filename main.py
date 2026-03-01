from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.database_setup import Base, engine
from routes import classify_route, vector_db_route, user_register_route, database_route
from services.manager import Manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = Manager.get_instance()
    manager.load_all_instances()

    Base.metadata.create_all(bind=engine)

    yield

    await manager.redis_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(classify_route.router)
app.include_router(vector_db_route.router)
app.include_router(user_register_route.router)
app.include_router(database_route.router)
