from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from sqlalchemy.orm import Session
from json.decoder import JSONDecodeError

from config import DB_STRING
from jsonextractor import JSONExtractor
from models import Base, Interface

# generate database schema
engine = create_engine(DB_STRING)
Base.metadata.create_all(engine)


def add_interfaces_to_database(list_of_interfaces: List) -> None:
    """Adds each interface to database.

    Args:
        list_of_interfaces (List[List[str]]): List with information about interfaces.
                                              Each in separated list.
    """
    session = Session(bind=engine)
    for interface in list_of_interfaces:
        interface_name = interface[0]
        interface_description = interface[1]
        interface_max_frame_size = interface[2]
        interface_config = interface[3]
        interface_port_channel_name = interface[4]
        interface_port_channel_id = None

        if interface_port_channel_name:
            interface_port_channel_id = _get_port_channel_id(
                session, interface_port_channel_name)

        session.add(
            Interface(
                name=interface_name,
                description=interface_description,
                max_frame_size=interface_max_frame_size,
                config=interface_config,
                port_channel_id=interface_port_channel_id,
            )
        )
        session.commit()
    session.close()


def _get_port_channel_id(session: Session, port_channel_name: str) -> int:
    """Helper to link Ethernet interface to Port-channel.

    Args:
        session (Session): Database session.
        port_channel_name (str): Name of Port-channel.

    Returns:
        int: ID of Port-channel in database.
    """
    query = session.query(Interface).filter(
        Interface.name == port_channel_name)
    return query.first().id


if __name__ == "__main__":
    try:
        jsonextractor = JSONExtractor("configClear_v2.json")
        interface_types = [
            "Port-channel",
            "GigabitEthernet",
            "TenGigabitEthernet"]
        list_of_interfaces = jsonextractor.get_interfaces(interface_types)
        add_interfaces_to_database(list_of_interfaces)
    except JSONDecodeError:
        print("Not a valid JSON document.")
    except FileNotFoundError:
        print("File with provided name does not exist.")
    except Exception as e:
        print(f"Exception occured: {e}")
