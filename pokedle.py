import requests
import random
import sys
LAST_ID = 1025
base_url="https://pokeapi.co/api/v2/"
def get_pokemon_info_by_name(name):
    url=f"{base_url}/pokemon/{name}"
    response=requests.get(url)
    p_data=None
    if response.status_code==200:
        p_data=response.json()
    return p_data
def get_pokemon_info_by_id(id):
    url=f"{base_url}/pokemon/{id}"
    response=requests.get(url)
    p_data=None
    if response.status_code==200:
        p_data=response.json()
    return p_data
def pokedle():
    random_id=random.randint(1,LAST_ID)
    random_pkm=get_pokemon_info_by_id(random_id)
    pkm_name=random_pkm['name']
    pkm_gen_info=requests.get(f"{base_url}/pokemon-species/{pkm_name}").json()
    pkm_gen=pkm_gen_info['generation']['name']
    pkm_abilities=[]
    pkm_hidden_ability=""
    for ability in random_pkm['abilities']:
        pkm_abilities.append(ability['ability']['name'])
        if ability['is_hidden']:
            pkm_hidden_ability=ability['ability']['name']
    #print(pkm_name)
    guess_count=0
    try:
        gen = "???"
        types = []
        abilities = []
        if pkm_hidden_ability!="":
            hidden_ability = "???"
        else:
            hidden_ability = "None"
        for i in range(len(random_pkm['types'])):
            types.append("???")
        if len(types) == 1:
            types.append("None")
        guess=""
        #random_pkm['types'][0]['type']['name']
        while guess!=pkm_name:
            print(f"\nGeneration = {gen}\t  Primary Type={types[0]}\t Secondary Type={types[1]}\t Abilities={abilities}\t Hidden Ability={hidden_ability}")
            guess=input("Guess the pokemon! ")
            if(guess==pkm_name):
                guess_count+=1
                print(f"Correct! The pokemon was {pkm_name}. It took you {guess_count} guesses.")
                break
            guessed_pkm=get_pokemon_info_by_name(guess)
            if(guessed_pkm!=None):
                guess_count+=1
                if gen=="???":
                    guessed_gen_info=requests.get(f"{base_url}/pokemon-species/{guess}").json()
                    if guessed_gen_info['generation']['name']==pkm_gen:
                        gen=pkm_gen[11:]
                if types[0]=="???":
                    if guessed_pkm['types'][0]['type']['name']==random_pkm['types'][0]['type']['name'] or (len(guessed_pkm['types'])==2 and guessed_pkm['types'][1]['type']['name']==random_pkm['types'][0]['type']['name']):
                        types[0]=random_pkm['types'][0]['type']['name']
                if types[1]=="???":
                    if guessed_pkm['types'][0]['type']['name']==random_pkm['types'][1]['type']['name'] or (len(guessed_pkm['types'])==2 and guessed_pkm['types'][1]['type']['name']==random_pkm['types'][1]['type']['name']):
                        types[1]=random_pkm['types'][1]['type']['name']
                for ability in guessed_pkm['abilities']:
                    if ability['ability']['name'] not in abilities and ability['ability']['name'] in pkm_abilities:
                        if(ability['ability']['name']==pkm_hidden_ability):
                            hidden_ability=ability['ability']['name']
                        else:
                            abilities.append(ability['ability']['name'])
            else:
                print("Sorry, couldn't recognize that pokemon\n")
    except KeyboardInterrupt:
        print(f"The pokemon was {pkm_name}")
        sys.exit()
try:
    response = "y"
    while response == "y":
        pokedle()
        response = input("Do you want to play again? (y/n)\n")
except KeyboardInterrupt:
    sys.exit()
