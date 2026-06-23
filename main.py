import fastapi
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="PokéDex de Josue")

Pokedex = {
    1: {"nombre": "Bulbasaur", "tipo": ["Planta", "Veneno"], "nivel": 5, "habilidad" : "Dormir", "ataque" : 9, "defensa": 10},
    4: {"nombre": "Charmander", "tipo": ["Fuego"], "nivel": 5 , "habilidad" : "Gritar","ataque" :10,  "defensa": 10 },
    7: {"nombre": "Squirtle", "tipo": ["Agua"], "nivel": 5 , "habilidad" : "Saltar","ataque" :  2,  "defensa": 10}
}

class Pokemon(BaseModel):
    nombre : str | None = None
    tipo : List[str]| None= None
    nivel : int| None= None
    habilidad : str| None= None
    movimeinto: list[str]| None= None
    ataque: int| None= None
    defensa: int | None= None

@app.get("/")
def leer_raiz():
    return {"mensaje": "Soy Josue y mi Pokemón favorito es Pichu"}

@app.get("/pokemons")
def obtener_todos_los_pokemon(habilidad: str = None, tipo: str = None):
    if habilidad is None and tipo is None:
        return Pokedex

    elif habilidad is not None and tipo is not None:
        pokemon_filtrados = {}
        for pokemon_id, datos in Pokedex.items():
            if tipo.capitalize() in datos["tipo"] and habilidad.capitalize() == datos["habilidad"].capitalize():
                pokemon_filtrados[pokemon_id] = datos


        if not pokemon_filtrados:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Pokémon de tipo '{tipo}' con la habilidad '{habilidad}' en la PokéDex."
            )
        return pokemon_filtrados

    elif tipo is not None:
        pokemon_filtrados = {}
        for pokemon_id, datos in Pokedex.items():
            if tipo.capitalize() in datos["tipo"]:
                pokemon_filtrados[pokemon_id] = datos


        if not pokemon_filtrados:
            raise HTTPException(status_code=404, detail=f"No existe ningún Pokémon de tipo '{tipo}' en la PokéDex.")
        return pokemon_filtrados

    elif habilidad is not None:
        pokemon_filtrados = {}
        for pokemon_id, datos in Pokedex.items():
            if habilidad.capitalize() == datos["habilidad"].capitalize():
                pokemon_filtrados[pokemon_id] = datos


        if not pokemon_filtrados:
            raise HTTPException(status_code=404, detail=f"No existe ningún Pokémon con la habilidad '{habilidad}' en la PokéDex.")
        return pokemon_filtrados


@app.get("/pokemons/{pokemon_id}")
def obtener_Pokemon_por_id(pokemon_id: int):
    if pokemon_id not in Pokedex:
        raise HTTPException(status_code=404, detail=f"Este Pokemón (Pokémon ID: {pokemon_id}) Es paraguayo.")

    return Pokedex[pokemon_id]

#endpoint para registrar un nuevo pokemon
@app.post("/pokemons/{pokemon_id}", status_code=201)
def añadir_nuevo_pokemon(pokemon_id: int, nuevo_pokemon: Pokemon):
    if pokemon_id in Pokedex:
        raise HTTPException(status_code= 400, detail=f"Ya existe un pokemon registrado con el ID#: {pokemon_id}, con nombre de {Pokedex[pokemon_id]['nombre']}")

    #Añadir el pokemon
    Pokedex[pokemon_id] = nuevo_pokemon.model_dump()
    return {
        "mensaje": f"Pokemon exitosamente registrado con el ID{pokemon_id}",
        "datos": Pokedex[pokemon_id]
    }

#endpoint para actualizar por completo un endpoint de la pokedex
@app.put("/pokemons/{pokemon_id}")
def actualizar_pokemon_completo(pokemon_id: int, pokemon_actualizados: Pokemon):
    if pokemon_id not in Pokedex:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail  = f"No existe ningun pokemon con el id {pokemon_id}")
    pokedex[pokemon_id] = pokemon_actualizados.model_dump()
    return {
        "mensaje": f"Pokemon actualizado con el ID{pokemon_id}",
        "datos": pokemon_actualizados
    }


#endpoint para actualizar parcialemnte un pokemon en la pokedex
@app.patch("/pokemons/{pokemon_id}")
def actualizar_pokemon_parcial(pokemon_id : int, datos_actualizados: PokemonParcial):
    if pokemon_id not in Pokedex:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail  = f"No existe ningun pokemon con el id {pokemon_id}")

    datos_a_actualizar = datos_actualizados.model_dump(exclude_unset=True)

    for llave, valor in datos_a_actualizar.items():
        pokedex[pokemon_id][llave] = valor

        pokedex[pokemon_id] = pokemon_actualizados.model_dump()
    return {
        "mensaje": f"Pokemon actualizado con el ID{pokemon_id}",
        "datos": pokemon_actualizados
    }


@app.delete("/pokemons/{pokemon_id}")
def liberar_pokemon(pokemon_id : int):
    if pokemon_id not in pokedex:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"No existe ningun pokemon con el ID{pokemon_id}")

    pokemon_liberado = pokedex.pop(pokemon_id)
    nombre = pokemon_liberado['nombre']

    return{
        "mensaje" : f"Adios {pokemon_liberado['nombre']} ",
    }






















































