import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.pokemon_type = None
        self.weight = None
        self.height = None
        self.abilities = None
        self.level = 1  # Başlangıç seviyesi
        self.is_legendary = False  # Nadir Pokémon kontrolü için eklenen özellik
        self.is_mythical = False   # Mitolojik Pokémon kontrolü için eklenen özellik

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name']
                    self.pokemon_type = [type['type']['name'] for type in data['types']]
                    self.weight = data['weight']
                    self.height = data['height']
                    self.abilities = [ability['ability']['name'] for ability in data['abilities']]
                    # Nadirlik durumlarını kontrol et
                    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{self.pokemon_number}"
                    async with session.get(species_url) as species_response:
                        if species_response.status == 200:
                            species_data = await species_response.json()
                            self.is_legendary = species_data.get('is_legendary', False)
                            self.is_mythical = species_data.get('is_mythical', False)
                    return self.name
                else:
                    return "Pikachu"

    async def get_pokedex_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon-species/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['flavor_text_entries'][0]['flavor_text']  # Pokémon hakkında metin
                else:
                    return "Veri alınamadı."

    async def info(self):
        if not self.name:
            await self.get_name()
        bonus_message = ''
        if self.is_legendary or self.is_mythical:
            bonus_message = f"BONUS: {self.name} nadir bir Pokémon! Seviyeniz artıyor!"
            self.level += 5  # Nadir Pokémonlar için seviyeye bonus ekleniyor
        return f"""
        Pokémonunuzun ismi: {self.name}
        Türü: {', '.join(self.pokemon_type)}
        Ağırlığı: {self.weight / 10} kg
        Boyu: {self.height / 10} m
        Yetenekleri: {', '.join(self.abilities)}
        Seviyesi: {self.level}
        {bonus_message}
        """

    async def besle(self):
        self.level += 1
        return f"{self.name} beslendi! Seviyesi {self.level} oldu."

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['sprites']['front_default']
                else:
                    return None
