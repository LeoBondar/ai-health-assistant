from dependency_injector import containers, providers

from app.infrastructure.db import Database, SessionContext
from app.repositories.uow import IUnitOfWork, UnitOfWork
from app.settings import Settings


class WebAppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.api", __name__])
    settings = providers.Singleton(Settings)
    database: providers.Singleton[Database] = providers.Singleton(
        Database, settings=settings.provided.database
    )
    session_context = providers.Factory(SessionContext)

    unit_of_work: providers.ContextLocalSingleton[
        IUnitOfWork
    ] = providers.ContextLocalSingleton(
        UnitOfWork, session_context=session_context, database=database
    )

    # HTTP Clients

    # Adapters