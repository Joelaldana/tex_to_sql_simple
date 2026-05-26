from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración base de datos
Base = declarative_base()

engine = create_engine("sqlite:///personas.db", echo=True)

Session = sessionmaker(bind=engine)
session = Session()


# Clase Persona
class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)


# Crear tablas
Base.metadata.create_all(engine)


# Función principal
def interpretar_texto(texto):
    """
    Interpreta instrucciones en texto simple.

    Ejemplos:
    - agrega persona Juan 25
    - muestra todas las personas
    - borra persona Juan
    """

    palabras = texto.lower().split()

    # AGREGAR PERSONA
    if palabras[0] == "agrega" and palabras[1] == "persona":

        nombre = palabras[2]
        edad = int(palabras[3])

        nueva = Persona(nombre=nombre, edad=edad)

        session.add(nueva)
        session.commit()

        return f"Persona '{nombre}' agregada con edad {edad}"

    # MOSTRAR PERSONAS
    elif texto.lower() == "muestra todas las personas":

        personas = session.query(Persona).all()

        if personas:
            return "\n".join(
                [f"{p.id}. {p.nombre} - {p.edad} años" for p in personas]
            )

        else:
            return "No hay personas registradas."

    # BORRAR PERSONA
    elif texto.lower().startswith("borra persona"):

        nombre = palabras[2]

        persona = session.query(Persona).filter_by(nombre=nombre).first()

        if persona:

            session.delete(persona)
            session.commit()

            return f"Persona '{nombre}' eliminada."

        else:
            return f"No se encontró la persona '{nombre}'."

    # ERROR
    else:
        return "Instrucción no reconocida."


# Programa principal
if __name__ == "__main__":

    print("=== Sistema Text-to-SQL Básico ===")
    print("Ejemplos:")
    print("- agrega persona Juan 25")
    print("- muestra todas las personas")
    print("- borra persona Juan")
    print("- salir\n")

    while True:

        comando = input("Escribe tu instrucción: ")

        if comando.lower() == "salir":
            break

        resultado = interpretar_texto(comando)

        print(resultado)