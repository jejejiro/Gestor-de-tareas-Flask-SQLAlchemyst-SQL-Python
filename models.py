from sqlalchemy import Integer, Column, String, Boolean
import db

class Tarea(db.Base):
    __tablename__ = "tarea"
    #__table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True) # Automaticamente sabe que es incremental
    contenido = Column(String(200), nullable=False)
    hecha = Column(Boolean)
    importante = Column(Boolean) # Atrubitoboleano para determinar si es importante
    fecha = Column(String(200), nullable=False) # Atributo de fecha

    def __init__(self,contenido,hecha,importante,fecha):
        self.contenido = contenido
        self.hecha = hecha
        self.importante = importante
        self.fecha = fecha

    def __str__(self):
        return "Tarea {} : {} ({}) {}".format(self.id, self.contenido, self.hecha, self.importante)