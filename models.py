from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import INTEGER, JSON, VARCHAR

Base = declarative_base()


class Interface(Base):
    """Interface model in database."""
    __tablename__ = "interfaces"
    id = Column("id", INTEGER, primary_key=True, autoincrement=True)
    connection = Column("connection", INTEGER)
    name = Column("name", VARCHAR(255), nullable=False)
    description = Column("description", VARCHAR(255))
    config = Column("config", JSON)
    type = Column("type", VARCHAR(50))
    infra_type = Column("infra_type", VARCHAR(50))
    port_channel_id = Column("port_channel_id", INTEGER)
    max_frame_size = Column("max_frame_size", INTEGER)

    def __repr__(self) -> str:
        return super().__repr__(
            f"<Interface(id='{self.id}', connection='{self.connection}', name='{self.name}', \
                description='{self.description}', config='{self.config}', type='{self.type}', \
                infra_type='{self.infra_type}', port_channel_id='{self.port_channel_id}', \
                max_frame_size='{self.max_frame_size}')>")
