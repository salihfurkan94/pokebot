import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import asyncio
# 📌 1. GEKELİ KÜTÜPHANELER İMPORT EDİLMELİ
from datetime import datetime , timedelta
class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        # 📌 2. POKEMONUN SON BESLNEME ZAMANINI SAKLAYAN NİTELİK EKLE
        self.last_feed_time = datetime.now()
        self.power = random.randint(30,60)
        self.hp = random.randint(200,400)
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
        return f"""Pokémon ismi: {self.name}
                Pokémon gücü: {self.power}
                Pokémon sağlığı: {self.hp}""" 
        

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['sprites']['front_default']
                    
                else:
                    return None
    

   
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1,5)     
            if chance == 1:
                    return "Sihirbaz pokemon savaşta bir kalkan kullanıdı"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

    #📌 3. feed mehodunu düzneleyerek ekleyin

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon sağlığı geri yüklenir. Mevcut sağlık: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {current_time+delta_time}"
  
class Wizard(Pokemon):
    async def attack(self, enemy):
        magic_power = random.randint(5, 15)  
        self.power +=magic_power
        result = await super().attack(enemy)  
        self.power -= magic_power
        return result + f"\nSihirbaz Pokémon süper sihir kullandı. Eklenen güç: {magic_power}"
    # 📌 4.  Wizard sınıfI için feed() metodunu uygulayın.
    def feed(self):
        return super().feed(hp_increase=20)

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)  
        self.power += super_power
        result = await super().attack(enemy)  
        self.power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"

     # 📌 4. Fighter  sınıfI için feed() metodunu uygulayın.
    def feed(self):
        return super().feed(feed_interval=10)




#‼️TEST
async def main():
    wizard = Wizard("deniz")
    fighter= Fighter("dorukata")

    print(await wizard.info())
    print("#" * 10)
    print(await fighter.info())
    print("#" * 10)
    print(await wizard.attack(fighter))
    print(await fighter.attack(wizard))

# Asenkron main fonksiyonunu çalıştırıyoruz
asyncio.run(main())

