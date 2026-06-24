import fastapi
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="PokéDex de Josue")

pokedex = {
    1: {"nombre": "Bulbasaur", "tipo": ["Planta", "Veneno"], "nivel": 5, "habilidad": "Piel verde", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5},
    2: {"nombre": "Ivysaur", "tipo": ["Planta", "Veneno"], "nivel": 16, "habilidad": "Piel verde", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5},
    3: {"nombre": "Venusaur", "tipo": ["Planta", "Veneno"], "nivel": 32, "habilidad": "Piel verde", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5},
    4: {"nombre": "Charmander", "tipo": ["Fuego"], "nivel": 5, "habilidad": "Piel roja", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5},
    5: {"nombre": "Charmeleon", "tipo": ["Fuego"], "nivel": 16, "habilidad": "Piel roja", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5},
    6: {"nombre": "Charizard", "tipo": ["Fuego", "Volador"], "nivel": 32, "habilidad": "Piel roja", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5},
    7: {"nombre": "Squirtle", "tipo": ["Agua"], "nivel": 5, "habilidad": "Piel azul", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5},
    8: {"nombre": "Wartortle", "tipo": ["Agua"], "nivel": 5, "habilidad": "Piel azul", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5},
    9: {"nombre": "Blastoise", "tipo": ["Agua"], "nivel": 5, "habilidad": "Piel azul", "movimientos": ["Placaje", "Gruñido", "Arañazo", "Látigo"], "ataque": 10, "defensa": 5}
    }

class Pokemon(BaseModel):
    nombre : str | None = None
    tipo : List[str]| None= None
    nivel : int| None= None
    habilidad : str| None= None
    movimientos: list[str]| None= None # <- CORREGIDO: Pluralizado para coincidir con la Pokedex
    ataque: int| None= None
    defensa: int | None= None

@app.get("/")
def leer_raiz():
    return {"mensaje": "Soy Josue y mi Pokemón favorito es Pichu"}

# Ejemplo de Query Parameter
@app.get("/pokemons")
def obtener_todos_los_pokemon(tipo: str = None, habilidad: str = None, limit: int = 5, offset : int = 0):


    resultados = pokedex

    if tipo:
        tipo_existe = any(tipo.capitalize() in p["tipo"] for p in pokedex.values())
        if not tipo_existe:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Pokémon de tipo {tipo.capitalize()} en la PokéDex..."
            )
        resultados = {id: p for id, p in resultados.items() if tipo.capitalize() in p["tipo"]}

    if habilidad:
        hab_existe = any(habilidad.lower() == p["habilidad"].lower() for p in pokedex.values())
        if not hab_existe:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Pokémon con la habilidad '{habilidad}' en la PokéDex..."
            )
        resultados = {id: p for id, p in resultados.items() if habilidad.lower() == p["habilidad"].lower()}

    if not resultados:
        mensaje_error = "No se encontraron Pokémon"
        if tipo:
            mensaje_error += f" de tipo {tipo.capitalize()}"
        if habilidad:
            mensaje_error += f" con la habilidad '{habilidad}'"
        raise HTTPException(
            status_code=404,
            detail=f"{mensaje_error} en la PokéDex..."
        )

    pokedex_a_lista = list(resultados.items())

    resultados_paginados = dict(pokedex_a_lista[offset : limit + offset])

    return{
        "total_coincidencias": len(resultados),
        "limit_pagina": limit,
        "desplazamiento": offset,
        "resultados": resultados_paginados,
    }


@app.get("/pokemons/{pokemon_id}")
def obtener_Pokemon_por_id(pokemon_id: int):
    if pokemon_id not in pokedex:
        raise HTTPException(status_code=404, detail=f"Este Pokemón (Pokémon ID: {pokemon_id}) Es paraguayo.")

    return pokedex[pokemon_id]

# Endpoint para registrar un nuevo pokemon
@app.post("/pokemons/{pokemon_id}", status_code=201)
def añadir_nuevo_pokemon(pokemon_id: int, nuevo_pokemon: Pokemon):
    if pokemon_id in pokedex:
        raise HTTPException(status_code= 400, detail=f"Ya existe un pokemon registrado con el ID#: {pokemon_id}, con nombre de {Pokedex[pokemon_id]['nombre']}")

    # Añadir el pokemon al diccionario
    pokedex[pokemon_id] = nuevo_pokemon.model_dump()

    # MODIFICADO: Mensaje personalizado con nombre y retorno con movimientos, ataque y defensa incluidos
    return {
        "mensaje": f"Pokémon {nuevo_pokemon.nombre} exitosamente registrado con el ID {pokemon_id}",
        "datos": pokedex[pokemon_id]
    }

# Endpoint para actualizar por completo un pokemon de la pokedex
@app.put("/pokemons/{pokemon_id}")
def actualizar_pokemon_completo(pokemon_id: int, pokemon_actualizados: Pokemon):
    if pokemon_id not in pokedex: # CORREGIDO: Pokedex
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail  = f"No existe ningun pokemon con el id {pokemon_id}")

    pokedex[pokemon_id] = pokemon_actualizados.model_dump() # CORREGIDO: Pokedex
    return {
        "mensaje": f"Pokemon actualizado con el ID {pokemon_id}",
        "datos": pokedex[pokemon_id]
    }


# Endpoint para actualizar parcialmente un pokemon en la pokedex
@app.patch("/pokemons/{pokemon_id}")
def actualizar_pokemon_parcial(pokemon_id : int, datos_actualizados: Pokemon): # CORREGIDO: PokemonParcial -> Pokemon
    if pokemon_id not in pokedex: # CORREGIDO: Pokedex
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail  = f"No existe ningun pokemon con el id {pokemon_id}")

    datos_a_actualizar = datos_actualizados.model_dump(exclude_unset=True)

    for llave, valor in datos_a_actualizar.items():
        pokedex[pokemon_id][llave] = valor # CORREGIDO: Pokedex y lógica simplificada

    return {
        "mensaje": f"Pokemon actualizado parcialmente con el ID {pokemon_id}",
        "datos": pokedex[pokemon_id]
    }


@app.delete("/pokemons/{pokemon_id}")
def liberar_pokemon(pokemon_id : int):

        if pokemon_id not in pokedex: # CORREGIDO: Pokedex
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"No existe ningun pokemon con el ID {pokemon_id}")

        if pokemon_id in [1, 4, 7]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,)
            return {
                "mensaje" : f"El pokemon con el id: {pokemon_id} no es posible de eliminar.",
                "datos": pokedex[pokemon_id]
            }
        else:
            pokemon_liberado = pokedex.pop(pokemon_id) # CORREGIDO: Pokedex

            return {
                "mensaje" : f"Adios {pokemon_liberado['nombre']} ",
            }

