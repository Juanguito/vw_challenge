import os
from typing import List, Optional
from uuid import UUID, uuid4

from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import Column, String, create_engine
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.domain.models.match import Match
from src.domain.models.status import Status
from src.domain.repositories.match_repository import MatchRepository

# from src.infra.repositories.models.match import MatchDB

# # Cargar variables de entorno
# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# # Crear motor de base de datos
# engine = create_engine(DATABASE_URL)

# # Crear sesión de base de datos
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cargar variables de entorno
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Base para modelos
Base = declarative_base()


class MatchDB(Base):
    __tablename__ = "matches"

    id = Column(UUID_PG(as_uuid=True), primary_key=True, default=uuid4, index=True)
    status = Column(String, nullable=False)
    turn = Column(String, nullable=False)
    board = Column(String, nullable=False)

    def to_db_board(self, board: List[List[Optional[str]]]) -> str:
        return "".join(
            "".join(str(cell) if cell is not None else " " for cell in row)
            for row in board
        )

    @classmethod
    def from_db_board(cls, board_str: str) -> List[List[Optional[str]]]:
        size = int(len(board_str) ** 0.5)  # Asumiendo tablero cuadrado
        board = []
        for i in range(size):
            row = []
            for j in range(size):
                cell = board_str[i * size + j]
                row.append(cell if cell != " " else None)
            board.append(row)
        return board


# Definición del repositorio
class PostgreSQLRepository:

    def __init__(self):
        # Crear motor de base de datos
        self.engine = create_engine(DATABASE_URL)

        # self.engine = create_engine(database_url)  # Inyecta la URL de la base de datos
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)  # Crea las tablas si no existen

    def save_match(self, match: Match) -> Match:
        db = self.SessionLocal()
        try:
            match_db = MatchDB(
                id=match.id,
                status=match.status.value,
                turn=match.turn,
                board=MatchDB().to_db_board(match.board),
            )
            db.add(match_db)
            db.commit()
            db.refresh(match_db)
            match.board = MatchDB.from_db_board(match_db.board)
            return match
        except Exception as e:
            print(f"Error al guardar el partido: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    def update_match(self, match: Match) -> Match:
        db = self.SessionLocal()
        try:
            if (
                match_db := db.query(MatchDB).filter(MatchDB.id == match.id).first()
            ):  # Busca si ya existe un partido con ese ID # Si existe, actualiza sus campos
                match_db.status = match.status.value
                match_db.turn = match.turn
                match_db.board = MatchDB().to_db_board(match.board)
                db.commit()
                db.refresh(
                    match_db
                )  # Refresca para obtener los valores actualizados de la base de datos
                match.board = MatchDB.from_db_board(
                    match_db.board
                )  # Recupera el tablero como lista

                return match  # Retorna el objeto Match original (dominio) con los datos actualizados
            else:
                print(f"Error al obtener el partido: {e}")
                db.rollback()
                return None

        except Exception as e:
            print(f"Error al guardar el partido: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    def get_match(self, match_id: UUID) -> Match:  # Cambio el tipo a UUID
        db = self.SessionLocal()
        try:
            match_db = db.query(MatchDB).filter(MatchDB.id == match_id).first()
            if match_db:
                match = Match(
                    id=match_db.id,
                    status=match_db.status,
                    turn=match_db.turn,
                    board=MatchDB.from_db_board(match_db.board),
                )
                return match
            return None
        except Exception as e:
            print(f"Error al obtener el partido: {e}")
            db.rollback()
            return None
        finally:
            db.close()


# # Dependencia para obtener sesión en rutas
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# class PostgreSQLRepository(MatchRepository):

#     def get_match(self, match_id: str) -> Match:
#         db = SessionLocal()
#         try:
#             match_db = db.query(MatchDB).filter(MatchDB.id == match_id).first()
#             if match_db:
#                 match = (
#                     Match(  # Crea una instancia de Match (dominio) a partir de MatchDB
#                         id=match_db.id,
#                         status=Status(match_db.status),  # Convierte el string a enum
#                         turn=match_db.turn,
#                         board=MatchDB.from_db_board(match_db.board),
#                     )
#                 )
#                 return match
#             return None
#         except Exception as e:
#             print(
#                 f"Error when retrieving match: {e}"
#             )  # Imprime el error para depuración
#             db.rollback()  # Es importante hacer rollback en caso de error para mantener la integridad de la base de datos
#             return None  # o raise la excepción si quieres propagarla
#         finally:
#             db.close()

#     def save_match(self, match: Match) -> Match:
#         db = SessionLocal()
#         try:
#             match_db = MatchDB(  # Crea una instancia de MatchDB
#                 id=match.id,
#                 status=match.status.value,  # Accede al valor del enum
#                 turn=match.turn,
#                 board=MatchDB().to_db_board(
#                     match.board
#                 ),  # Usa el método del modelo de BD
#             )

#             db.add(match_db)
#             db.commit()
#             db.refresh(
#                 match
#             )  # Refresca el objeto 'match' para obtener los valores generados por la base de datos (como el ID si es autoincrementable)
#             return match
#         except Exception as e:
#             print(f"Error when saving match: {e}")  # Imprime el error para depuración
#             db.rollback()
#             return None  # o raise la excepción si quieres propagarla
#         finally:
#             db.close()
