from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

# =============================
# CONFIGURACION BASE DE DATOS
# =============================

Base = declarative_base()

engine = create_engine("sqlite:///personas.db", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

# =============================
# CLASE PERSONA
# =============================

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)

# ================================
# CLASE LOG (RELLENO)
# ================================

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    accion = Column(String)    


# ================================
# CREAR TABLAS
# ================================

Base.metadata.create_all(engine)


# ================================
# FUNCION PRINCIPAL
# ================================

def interpretar_texto(texto):
    """
    Interpreta instrucciones en texto simple.

    Ejemplos:
    - agrega persona joel 25
    - muestra todas las personas
    - borra persona joel
    """

    palabras = texto.lower().split()

    # ================================
    #   AGREGAR PERSONA 
    # ================================

    if palabras[0] == "agrega" and palabras[1] == "persona":

        nombre = palabras[2]
        edad = int(palabras[3])

        nueva = Persona(nombre=nombre, edad=edad)

        session.add(nueva)
        session.commit()

        return f"Persona '{nombre}' agregada con edad {edad}"
    
# ================================
# MOSTRAR PERSONAS
# ================================

    elif texto.lower() == "muestra todas las personas":

        personas = session.query(Persona).all()

        if personas:
            return "\n".join(
                [f"{p.id}. {p.nombre} - {p.edad} años" for p in personas]
            )

        else:
            return "No Hay Personas Registradas."


# =============================
# BORRAR PERSONA
# =============================

    elif texto.lower().startswith("borra persona"):

        nombre = palabras[2]

        persona = session.query(Persona).filter_by(nombre=nombre).first()

        if persona:

            session.delete(persona)
            session.commit()

            return f"'{nombre}' fue eliminado."

        else:
            return f"No se encontro '{nombre}'."
        
# =============================
# ERROR
# =============================

    else:
        return "No se Reconoce como una Instruccion"
    
# =============================
# PROGRAMA PRINCIPAL
# =============================


if __name__ == "__main__":

    print("=== Sistema Text-to-SQL Básico ===")
    print("Ejemplos:")
    print("- agrega persona Joel 17")
    print("- muestra todas las personas")
    print("- borra persona Joel")
    print("- salir\n")

    while True:

        comando = input("Escribe tu instrucción: ")

        if comando.lower() == "salir":
            break

        resultado = interpretar_texto(comando)

        print(resultado)