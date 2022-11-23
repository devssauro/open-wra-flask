from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, Integer, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

db = SQLAlchemy()
migrate = Migrate()


class Base(db.Model):  # type: ignore
    """
    Classe de campos base para uma entidade de banco de dados

    :param __abstract__: indica que a classe serve como base, e não é concreta
    :param id: Chave primária sequencial da tabela
    :param uuid: Chave primária UUID4 da tabela
    :param date_created: Data de criação do registro
    :param date_modified: Data da ultima modificação do registro
    :param active: Indicador de registro

    :type __abstract__: bool
    :type id: int
    :type uuid: UUID4
    :type date_created: datetime.datetime
    :type date_modified: datetime.datetime
    :type active: bool

    note::
        o active indica se o registro foi "apagado" ou não, é através dele que
        é feito a pesquisa no banco para saber quais registros estão disponíveis ou não ao usuário
    """

    __abstract__ = True

    id = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    uuid = Column(UUID(), unique=True, default=func.uuid_generate_v4())
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
    extra = Column(JSONB(), default={})

    active = Column(Boolean, nullable=False, default=True)
