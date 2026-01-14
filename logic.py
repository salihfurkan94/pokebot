import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import asyncio

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.level = random.randint(1, 100)
        self.power = random.randint(30, 60)
        self.health = random.randint(200, 400)   
        self.name = None
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name}, Pokemon Sağlığı: {self.hp}, Pokemon Gücü: {self.power}"

    
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
    def battle(self, other_pokemon):
        type_advantage = {"fire":"grass", "water":"fire", "grass":"water", "electric":"water"}
        my_attack = self.attack_power + random.randint(-5,5)
        other_attack = other_pokemon.attack_power + random.randint(-5,5)
        if type_advantage.get(self.type) == other_pokemon.type:
            my_attack *= 1.2
        elif type_advantage.get(other_pokemon.type) == self.type:
            other_attack *= 1.2
        my_total = my_attack * self.level
        other_total = other_attack * other_pokemon.level
        if my_total > other_total:
            winner = self
        elif other_total > my_total:
            winner = other_pokemon
        else:
            winner = None
        return f"{winner.pokemon_trainer}'s {winner.name or 'Pokémon'} kazandı!" if winner else "Berabere!"
    async def show_img(self):

        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
                async with session.get(url) as response:  # GET isteği gönderme
                    if response.status == 200:
                        data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                        return data['sprites']['front_default']  #  Pokémon adını döndürme
                    else:
                        return None  # İstek başarısız olursa varsayılan adı döndürür
                    
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
                
                    
class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self_power += super_power
        result = await super().attack(enemy)
        self_power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"
    

#‼️TEST
async def main():
    wizard = Wizard("deniz")
    fighter= Fighter("xxxx")

    print(await wizard.info())
    print("#" * 10)
    print(await fighter.info())
    print("#" * 10)
    print(await wizard.attack(fighter))
    print(await fighter.attack(wizard))

# Asenkron main fonksiyonunu çalıştırıyoruz
asyncio.run(main())
                

