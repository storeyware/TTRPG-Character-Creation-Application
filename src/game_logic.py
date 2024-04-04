"""
Module: game_logic.py

Description:
    This module provides the core game logic and functionalities for character creation and interactions in a D&D-style game. 
    It includes mechanisms for rolling character stats, selecting races, classes, and subclasses, and managing character attributes and skills.

Dependencies:
    - random: For generating random numbers to simmulate rolling dice.
    - user_database.py: For interacting with the user database.
    - create_connection from user_database: For establishing database connections.

Usage:
    The functions and classes provided in this module can be used to build character creation and interaction logic
    for D&D 5e. This includes rolling for stats, selecting races/classes/subclasses, managing character
    attributes, and performing various game-specific calculations and interactions.
"""
import random
import ui
import user_database as db
from user_database import create_connection

# Dice Interactions
def roll_stats(dnd_class=None):
    rolled_scores = [sum(sorted([random.randint(1, 6) for _ in range(4)])[1:]) for _ in range(6)]
    
    if dnd_class and hasattr(dnd_class, 'reorder_ability_scores'):
        reordered_scores = dnd_class.reorder_ability_scores(rolled_scores)
        return reordered_scores
    
    return rolled_scores

def get_race_options():
    # Test Sample
    result = [
        "Half-Orc", "Human", "Tiefling"
    ]
    # Actual Result
    """result = [
        "Dragonborn", "Drow", "Dwarf", "Elf", "Gnome", "Half-Elf", "Halfling", "Half-Orc", "Human", "Tiefling", 
        "Aarakocra", "Aasimar", "Air Genasi", "Bugbear", "Centaur", "Changeling", "Deep Gnome", "Duergar", "Earth Genasi", 
        "Eladrin", "Fairy", "Firbolg", "Fire Genasi", "Githyanki", "Githzerai", "Goblin", "Goliath", "Harengon", 
        "Hobgoblin", "Kenku", "Kobold", "Lizardfolk", "Minotaur", "Orc", "Satyr", "Sea Elf", "Shadar-kai", "Shifter", 
        "Tabaxi", "Tortle", "Triton", "Water Genasi", "Yuan-ti", "Kender", "Astral Elf", "Autognome", "Giff", "Hadozee", 
        "Plasmoid", "Thri-kreen", "Owlin", "Lineages", "Leonin", "Satyr (Legacy)", "Changling (Legacy)", "Kalashtar", 
        "Shifter (Legacy)", "Warforged", "Verdan", "Centaur (Legacy)", "Loxodon", "Minotaur (Legacy)", "Simic Hybrid", 
        "Vedalken", "Feral Tiefling", "Tortle (Legacy)", "Locathah", "Grung", "Gith (Legacy)", "Aesimar (Legacy)", 
        "Bugbear (Legacy)", "Firbolg (Legacy)", "Goblin (Legacy)", "Hobgoblin (Legacy)", "Kenku (Legacy)", 
        "Kobold (Legacy)", "Lizardfolk (Legacy)", "Orc (Legacy)", "Tabaxi (Legacy)", "Triton (Legacy)", 
        "Yuan-ti Pureblood (Legacy)", "Aarakocra (Legacy)", "Genasi (Legasy)", "Goliath (Legacy)", "Wood Elf"
    ]"""
    result.sort()
    return result

def get_class_options():
    # Test Sample
    result = [
        "Barbarian", "Bard","Rogue"
    ]

    # Actual Result
    """result = [
        "Artificer", "Barbarian", "Bard", "Blood Hunter", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", 
        "Warlock", "Wizard"
    ]"""

    result.sort()
    return result

def get_subclass_options():
    # Test list
    return {
        "Barbarian": ["Path of the Totem Warrior", "Path of Wild Magic"],
        "Bard": ["College of Lore", "College of Swords"],
        "Rogue": ["Assassin", "Thief"]
    }

    # Actual list
    """return {
        "Artificer": ["Alechemist", "Artillerist", "Battle Smith", "Armorer"],
        "Barbarian": ["Path of the Totem Warrior", "Path of the Battlerager", "Path of the Ancestral Guardian", 
        "Path of the Storm Herald", "Path of the Zealot", "Path of the Beast", "Path of Wild Magic"],
        "Bard": ["College of Lore", "College of Valor", "College of Glamour", "College of Swords", "College of Whispers", 
        "College of Eloquence", "College of Creation"],
        "Blood Hunter": ["Order of the Ghostslayer", "Order of the Lycan", "Order of the Mutant", "Order of the Profane Soul"],
        "Cleric": ["Knowledge Domain", "Life Domain", "Light Domain", "Nature Domain", "Tempest Domain", "Trickery Domain", 
        "War Domain", "Death Domain", "Arcana Domain", "Solidarity Domain", "Strength Domain", "Ambition Domain", "Zeal Domain", 
        "Grave Domain", "Order Domain", "Peace Domain", "Twilight Domain", "Inevitability Domain"],
        "Druid": ["Circle of the Land", "Circle of the Moon", "Circle of the Shepherd", "Circle of Spores", "Circle of Stars", 
        "Circle of Wildfire", "Circle of Whispered Harmony"],
        "Fighter": ["Champion", "Battle Master", "Eldritch Knight", "Purple Dragon Knight", "Arcane Archer", "Cavalier", 
        "Samurai", "Echo Knight", "Psi Warrior", "Rune Knight"],
        "Monk": ["Way of the Open Hand", "Way of Shadow", "Way of the Four Elements", "Way of the Long Death", 
        "Way of the Sun Soul", "Way of the Drunken Master", "Way of the Kensei", "Way of Mercy", "Way of the Astral Self"],
        "Paladin": ["Oath of Devotion", "Oath of the Ancients", "Oath of Vengeance", "Oathbreaker", "Oath of the Crown", 
        "Oath of Conquest", "Oath of Redemption", "Oath of Glory", "Oath of the Watchers"],
        "Ranger": ["Hunter", "Beast Master", "Gloom Stalker", "Horizon Walker", "Monster Slayer", "Fey Wanderer", "Swarmkeeper"],
        "Rogue": ["Thief", "Assassin", "Arcane Trickster", "Mastermind", "Swashbuckler", "Inquisitive", "Scout", "Phantom", 
        "Soulknife"],
        "Sorcerer": ["Draconic Bloodline", "Wild Magic", "Storm Sorcery", "Pyromancer", "Divine Soul", "Shadow Magic", 
        "Aberrant Mind", "Clockwork Soul", "Lunar Sorcery"],
        "Warlock": ["The Archfey", "The Great Old One", "The Undying", "The Celestial", "The Hexblade", "The Fathomless", 
        "The Genie"],
        "Wizard": ["School of Abjuration", "School of Conjuration", "School of Divination", "School of Enchantment", 
        "School of Evocation", "School of Illusion", "School of Necromancy", "School of Transmutation", "Bladesinging", 
        "War Magic", "Chronurgy Magic", "Graviturgy", "Order of Scribes"]
    }"""

def get_background_options():
    # Test Sample
    result = [
        "Acolyte", "Soldier", "Spy"
    ]

    # Actual Result
    """result = [
        "Acolyte", "Anthropologist", "Archaeologist", "Adopted", "Black Fist Double Agent", "Caravan Specialist", "Charlatan", 
        "City Watch", "Clan Crafter", "Cloistered Scholar", "Cormanthor Refugee", "Courtier", "Criminal", "Dissenter", 
        "Dragon Casualty", "Earthspur Miner", "Entertainer", "Faction Agent", "Far Traveler", "Folk Hero", "Gate Urchin", 
        "Gladiator", "Guild Artisan", "Guild Merchant", "Harborfolk", "Haunted One", "Hermit", "Hillsfar Merchant", 
        "Hillsfar Smuggler", "House Agent", "Inheritor", "Initiate", "Inquisitor", "Investigator", "Iron Route Bandit", 
        "Knight of the Order", "Mercenary Veteran", "Mulmaster Aristocrat", "Noble", "Outlander", "Phlan Insurgent", 
        "Phlan Refugee", "Pirate", "Sage", "Sailor", "Secret Identity", "Shade Fanatic", "Soldier", "Spy", "Student Of Magic", 
        "Stojanow Prisoner", "Ticklebelly Nomad", "Trade Sheriff", "Urban Bounty Hunter", "Urchin", "Uthgardt Tribe Member", 
        "Vizier", "Waterdhavian Noble", "D&D Gladiator Arena"
    ]"""
    result.sort()
    return result

def get_background_descriptions(background):
    # from sample
    description = {
        "Acolyte": "You are devote to a specific god or pantheon. As an acolyte you are respected by others of your faith.\n\nSkill Proficiencies: Insight, Religion.\n\nLanguages: 2 of your choice.\n\nEquipment: A holy symbol, a prayer book/wheel, 5 sticks of incense, vestments, a set of common clothes, and a puch of 15 gold peices.",
        "Soldier": "War and battle is what you know best. You've trained your whole life and joined a military service when you came of age.\n\nSkill Proficiencies: Athletics, Intimidation.\n\nTool Proficiencies: One type of gaming set, vehicles (land).\n\nEquipment: Insignia of rank, trophy from a fallen foe, set of bone dice/cards, common clothes, and a puch of 10gp",
        "Spy": "A criminal or perhaps a government official. What ever brought you to the path of stealth and deception has toned your skills of trickery.\n\nSkill Proficiencies: Deception, Stealth.\n\nTool Proficiencies: One type of gaming set, thieves' tools.\n\nEquipment: A crowbar, set of dark common clothes and hood, puch containing 15 gold."
    }
    result = description.get(background, "no background found")
    return result

def get_skills():
    return [
        "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", 
        "Medicine", "Nature", "Perception","Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"
    ]

def get_skill_mods():
    skill_modifiers = {
        "Acrobatics": ability_modifiers["Dexterity"],
        "Animal Handling": ability_modifiers["Wisdom"],
        "Arcana": ability_modifiers["Intelligence"],
        "Athletics": ability_modifiers["Strength"],
        "Deception": ability_modifiers["Charisma"],
        "History": ability_modifiers["Intelligence"],
        "Insight": ability_modifiers["Wisdom"],
        "Intimidation": ability_modifiers["Charisma"],
        "Investigation": ability_modifiers["Intelligence"],
        "Medicine": ability_modifiers["Wisdom"],
        "Nature": ability_modifiers["Intelligence"],
        "Perception": ability_modifiers["Wisdom"],
        "Performance": ability_modifiers["Charisma"],
        "Persuasion": ability_modifiers["Charisma"],
        "Religion": ability_modifiers["Intelligence"],
        "Sleight of Hand": ability_modifiers["Dexterity"],
        "Stealth": ability_modifiers["Dexterity"],
        "Survival": ability_modifiers["Wisdom"]
    }

def get_skill_description(skill):
    descriptions = {
        "Acrobatics": "Acrobatics: Dexterity-based skill used to perform tasks that require finesse and agility, such as flips, rolls, and balancing.",
        "Animal Handling": "Animal Handling: Wisdom-based skill used to calm, train, or communicate with animals.",
        "Arcana": "Arcana: Intelligence-based skill used to recall knowledge about spells, magic items, eldritch symbols, magical traditions, and the planes of existence.",
        "Athletics": "Athletics: Strength-based skill used to perform tasks requiring physical prowess, such as climbing, jumping, and swimming.",
        "Deception": "Deception: Charisma-based skill used to convincingly lie, disguise intentions, or otherwise mislead others.",
        "History": "History: Intelligence-based skill used to recall knowledge about historical events, legendary people, ancient kingdoms, and past cultures.",
        "Insight": "Insight: Wisdom-based skill used to determine the true intentions of a creature, such as detecting lies or predicting someone's next move.",
        "Intimidation": "Intimidation: Charisma-based skill used to influence others through threats, hostile actions, and physical violence.",
        "Investigation": "Investigation: Intelligence-based skill used to look for clues, make deductions, or discern details about puzzles, objects, or environments.",
        "Medicine": "Medicine: Wisdom-based skill used to stabilize the dying, diagnose illnesses, and treat wounds.",
        "Nature": "Nature: Intelligence-based skill used to recall knowledge about terrain, plants and animals, the weather, and natural cycles.",
        "Perception": "Perception: Wisdom-based skill used to spot, hear, or otherwise detect the presence of something.",
        "Performance": "Performance: Charisma-based skill used to entertain others through music, dance, acting, storytelling, or some other form of entertainment.",
        "Persuasion": "Persuasion: Charisma-based skill used to influence someone or negotiate beneficial agreements.",
        "Religion": "Religion: Intelligence-based skill used to recall knowledge about deities, rites and prayers, religious hierarchies, holy symbols, and the practices of secret cults.",
        "Sleight of Hand": "Sleight of Hand: Dexterity-based skill used to perform tasks like pickpocketing, lockpicking, conjuring tricks, or using sleight to prevent being caught.",
        "Stealth": "Stealth: Dexterity-based skill used to hide or move silently.",
        "Survival": "Survival: Wisdom-based skill used to follow tracks, hunt wild game, guide your group through wastelands, predict the weather, or avoid quicksand and other natural hazards."
    }
    result = descriptions.get(skill, "skill not found")
    return result

def get_ability_scores():
    return [
        "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"
    ]

def get_feats():
    # Sample Feats
    return [
        "", "Ability Score Increase", "Alert", "Tough", "Tavern Brawler", "War Caster"
    ]
    # Actual Feats
    """return [
        "Ability Score Increase", "Actor", "Alert", "Artificer Initiate", "Athlete Feat", "Charger", "Chef", 
        "Crossbow Expert", "Crusher", "Defensive Duelist", "Dual Wielder", "Dungeon Dlver", "Durable", 
        "Eldritch Adept", "Elemental Adept", "Fey Touched", "Fighting Initiate", "Grappler", "Great Weapon Master", 
        "Gunner", "Healer", "Heavily Armored", "Heavy Armor Master", "Inspiring Leader", "Keen Mind", 
        "Lightly Armored", "Linguist", "Lucky", "Mage Slayer", "Magic Initiate", "Martial Adept", 
        "Medium Armor Master", "Metamagic Adept", "Mobile", "Moderately Armored", "Mounted Combatant", "Observant", 
        "Piercer", "Poisoner", "Polearm Master", "Resilient", "Ritual Caster", "Savage Attacker", "Sentinel", 
        "Shadow Touched", "Sharpshooter", "Shield Master", "Skilled", "Skulker", "Slasher", "Spell Sniper", 
        "Tavern Brawler", "Telekinetic", "Telepathic", "Tough", "War Caster", "Weapon Master"
    ]"""

def get_feat_descriptions(feat):
    # From Sample Feats
    description = {
        "Ability Score Increase": "Increase an ability score by 2 points or increase 2 ability scores by 1 point.",
        "Alert": "You cannot be surprised while conscious, gain a +5 bonus to initiative, and other creatures don't gain advantage on attack rolls against you as a result of being unseen by you.",
        "Tough": "HP maximum increased by twice your level. Every time you leve your HP max increases by an additional 2 HP.", 
        "Tavern Brawler": "Increase Strength and Constitution by 1 (max of 20), gain proficiency with improvised weapons, unarm strikes use a d4 for damage, and you can attempt to grapple as a bonus action after hitting a creature with an unarmed strike or imporovised weapon.",
        "War Caster": "You have advantage on Constitution saves for spell concentration, have the abiilty to perform somatic components of a spell while holding weapons and shields, and when a hostile provokes an attack of opportunity from you, you can use your reaction to cast a spell instead of the attack (1 action and single target only)."
    }
    result = description.get(feat, "No Feat selected.\n\nUnless your Dungeon Master says otherwise, you man gain a Feat at levels 4, 8, 12, 16, and 19.")
    return result

def get_race_map(race):
    race_mapping = {
        "Human": Human, 
        "Half-Orc": HalfOrc,
        "Tiefling": Tiefling
    }
    result = race_mapping.get(race, "race not found")
    return result

def roll_dice_logic(sides, num_dice=1):
    results = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(results)
    return results, total

def get_armor_data():
    armor_data = {
        "No Armor": [],
        "Light Armor": [("Padded", 11), ("Leather", 11), ("Studded Leather", 12)],
        "Medium Armor": [("Hide", 12), ("Chain Shirt", 13), ("Scale Mail", 14), ("Spiked Armor", 14), ("Breastplate", 14), ("Halfplate", 15)],
        "Heavy Armor": [("Ring Mail", 14), ("Chain Mail", 16), ("Splint", 17),("Plate", 18)]
    }
    return armor_data

def get_armor_type_options():
    armor_type_options = ["No Armor", "Light Armor", "Medium Armor", "Heavy Armor"]
    return armor_type_options

def get_armor_options():
    armor_options = {
        "No Armor": ["", "No Armor"],
        "Light Armor": ["", "Padded", "Leather", "Studded Leather"],
        "Medium Armor": ["", "Hide", "Chain Shirt", "Scale Mail", "Spiked Armor", "Breastplate", "Halfplate"],
        "Heavy Armor": ["", "Ring Mail", "Chain Mail", "Splint", "Plate"]
    }
    return armor_options

def calculate_ac(armor_type, armor_name, dex_modifier, shield_bonus):
    armor_data = get_armor_data()
    base_ac = 10

    if armor_type != "No Armor":
        for armor, ac in armor_data[armor_type]:
            if armor == armor_name:
                base_ac = ac
                break

    if armor_type == "Light Armor":
        total_ac = base_ac + dex_modifier + shield_bonus
    elif armor_type == "Medium Armor":
        total_ac = base_ac + min(dex_modifier, 2) + shield_bonus
    elif armor_type == "Heavy Armor":
        total_ac = base_ac + shield_bonus
    else:
        total_ac = base_ac + dex_modifier + shield_bonus

    return total_ac

# Base User class
class User:
    def __init__(self, user_id, username, password, email, is_admin=False):
        self.user_id = user_id
        self.username = username
        self.password = self.encrypt_password(password)
        self.email = email
        self.characters = []
        self.is_admin = is_admin

    def encrypt_password(self, password):
        self.encrypted_password = password
        return self.encrypted_password
    
    def set_admin(self, admin_status):
        self.is_admin = admin_status
        print("User status: ", admin_status)

    def encrypt_password(self, password):
        # To-Do: Implement password encryption (implementing if published)
        self.encrypted_password = password
        return self.encrypted_password
    
    def set_admin(self, admin_status):
        self.is_admin = admin_status
        print("User status: ", admin_status)

    def add_character(self, character_data):
        user_data = db.get_user(self.username)
        if user_data:
            user_name = user_data[0]
            user_id = user_data[3]
            
            new_character = Character(character_data)
            self.characters.append(new_character)

            db.add_character_to_db(user_name, character_data)
            self.load_characters()

    def remove_character(self, character_id):
        self.characters = [char for char in self.characters if char.character_id != character_id]

    def get_characters(self):
        return self.characters

    def display_characters(self):
        print(f"User: {self.username} has the following characters:")
        for character in self.characters:
            print(f"- Name: {character.name}, Race: {character.race}, Classes: {character.classes}")
            print(f"  Background: {character.background}, Ability Scores: {character.ability_scores}")
            print(f"  Skill Proficiencies: {character.skill_proficiencies}, Selected Feats: {character.selected_feats}")
            print(f"  Inventory: {character.inventory}")
        if not self.characters:
            print("No characters found.")

    def load_characters(self):
        conn = db.create_connection()
        if conn is not None:
            c = conn.cursor()
            c.execute("SELECT CharacterID FROM Characters WHERE UserID = ?", (self.user_id,))
            character_ids = c.fetchall()
            
            self.characters = []
            for character_id in character_ids:
                character_data = db.get_character(character_id[0])
                if character_data:
                    self.characters.append(Character(character_data))
            conn.close()

# Base character class
class Character:
    def __init__(self, character_data):
        self.character_id = character_data.get('character_id')
        self.name = character_data.get('name', '')
        self.race = character_data.get('race', '')
        self.background = character_data.get('background', '')
        self.ability_scores = character_data.get('ability_scores', [])
        self.skill_proficiencies = character_data.get('skill_proficiencies', [])
        self.selected_feats = character_data.get('feats', [])
        self.inventory = character_data.get('inventory', [])
        self.is_jack_of_all_trades = character_data.get('is_jack_of_all_trades', False)
        self.classes = character_data.get('classes', {})

    def display_character(self):
        print(f"{self.name} - Race: {self.race}, Classes: {self.classes}")
        print(f"Background: {self.background}, Ability Scores: {self.ability_scores}")
        print(f"Skill Proficiencies: {self.skill_proficiencies}, Selected Feats: {self.selected_feats}")
        print(f"Inventory: {self.inventory}")

    def __str__(self):
        class_str = ', '.join([f'{cls} {lvl}' for cls, lvl in self.classes.items()])
        return f"{self.name} - {class_str} - Race: {self.race}, Background: {self.background}"

# Base D&D Class class
class DndClass:
    def __init__(self, name, description, hit_die, primary_ability, saving_throws, skills, equipment, class_table):
        self.name = name
        self.description = description
        self.hit_die = hit_die
        self.primary_ability = primary_ability
        self.saving_throws = saving_throws
        self.skills = skills
        self.equipment = equipment
        self.class_table = class_table

    def __str__(self):
        return f"{self.name} class with hit die {self.hit_die} and primary ability {self.primary_ability}"

    # Method to display class table
    def display_class_table(self):
        print(f"Class Table for {self.name}:")
        headers = ["Level"] + list(self.class_table[1].keys())  # Dynamically get the headers from the first entry
        header_row = " | ".join(headers)
        print(f"| {header_row} |")
        print("|" + "|".join(["-" * len(header) for header in headers]) + "|")

        for level, details in self.class_table.items():
            row = [str(level)] + [str(details[key]) for key in details.keys()]  # Dynamically create the row
            print(f"| {' | '.join(row)} |")

    def get_description(self):
        return "{self.name} Description: {self.description}"
        print(f"{self.name} Description: {self.description}")

    def get_class_by_name(class_name):
        classes = {
            'Barbarian': Barbarian(),
            'Bard': Bard(),
            'Rogue': Rogue(),
        }
        return classes.get(class_name)

    def reorder_ability_scores(self, scores):
        sorted_scores = sorted(scores, reverse=True)
        reordered_scores = {ability: score for ability, score in zip(self.ability_priority, sorted_scores)}
        standard_ability_order = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
        final_scores = [reordered_scores[ability] for ability in standard_ability_order]
        return final_scores

def get_class_by_name(class_name):
    classes = {
        'Barbarian': Barbarian(),
        'Bard': Bard(),
        'Rogue': Rogue(),
        # Add other classes here
    }
    return classes.get(class_name)

# DnD Classes
class Barbarian(DndClass):
    def __init__(self):
        description = "If you're gonna be dumb, you gotta be tough. A strong warrior who can shrug off blows without the need for armor. At level 1, you may select 2 skills from the list below..."
        class_table = {
            1: {"Features": "Rage, Unarmored Defense", "Rages": 2, "Rage Damage": 2},
            2: {"Features": "Reckless Attack, Danger Sense", "Rages": 2, "Rage Damage": 2},
            3: {"Features": "Primal Path", "Rages": 3, "Rage Damage": 2},
            4: {"Features": "Ability Score Improvement", "Rages": 3, "Rage Damage": 2},
            5: {"Features": "Extra Attack, Fast Movement", "Rages": 3, "Rage Damage": 2},
            6: {"Features": "Path Feature", "Rages": 4, "Rage Damage": 2},
            7: {"Features": "Feral Instinct", "Rages": 4, "Rage Damage": 2},
            8: {"Features": "Ability Score Improvement", "Rages": 4, "Rage Damage": 2},
            9: {"Features": "Brutal Critical (1 die)", "Rages": 4, "Rage Damage": 3},
            10: {"Features": "Path Feature", "Rages": 4, "Rage Damage": 3},
            11: {"Features": "Relentless Rage", "Rages": 4, "Rage Damage": 3},
            12: {"Features": "Ability Score Improvement", "Rages": 5, "Rage Damage": 3},
            13: {"Features": "Brutal Critical (2 dice)", "Rages": 5, "Rage Damage": 3},
            14: {"Features": "Path Feature", "Rages": 5, "Rage Damage": 3},
            15: {"Features": "Persistent Rage", "Rages": 5, "Rage Damage": 3},
            16: {"Features": "Ability Score Improvement", "Rages": 5, "Rage Damage": 4},
            17: {"Features": "Brutal Critical (3 dice)", "Rages": 6, "Rage Damage": 4},
            18: {"Features": "Indomitable Might", "Rages": 6, "Rage Damage": 4},
            19: {"Features": "Ability Score Improvement", "Rages": 6, "Rage Damage": 4},
            20: {"Features": "Primal Champion", "Rages": "Unlimited", "Rage Damage": 4},
        }
        super().__init__(
            'Barbarian', description, 'd12', ['Strength'], ['Strength', 'Constitution'], 
            ['Animal Handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival'], 
            [('Greataxe', 'Any martial melee weapon'), ('Two handaxes', 'Any simple weapon'), 
            "Explorer's Pack", "Four Javelins"], class_table
        )
        self.ability_priority = ["Strength", "Constitution", "Dexterity", "Wisdom", "Charisma", "Intelligence"]

class Bard(DndClass):
    def __init__(self):
        description = "I seduce the dragon... A charismatic performer and jack-of-all trades. At level 1 you may select 3 skills from the entire skills list! Look at you. You're so talented!..."
        class_table = {
            1: {"Features": "Spellcasting, Bardic Inspiration (d6)", "Cantrips Known": 2, "Spells Known": 4, "Spell Slots": {1: 2}},
            2: {"Features": "Jack of All Trades, Song of Rest (d6)", "Cantrips Known": 2, "Spells Known": 5, "Spell Slots": {1: 3}},
            3: {"Features": "Bard College, Expertise", "Cantrips Known": 2, "Spells Known": 6, "Spell Slots": {1: 4, 2: 2}},
            4: {"Features": "Ability Score Improvement", "Cantrips Known": 3, "Spells Known": 7, "Spell Slots": {1: 4, 2: 3}},
            5: {"Features": "Bardic Inspiration (d8), Font of Inspiration", "Cantrips Known": 3, "Spells Known": 8, "Spell Slots": {1: 4, 2: 3, 3: 2}},
            6: {"Features": "Countercharm, Bard College Feature", "Cantrips Known": 3, "Spells Known": 9, "Spell Slots": {1: 4, 2: 3, 3: 3}},
            7: {"Features": "", "Cantrips Known": 3, "Spells Known": 10, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 1}},
            8: {"Features": "Ability Score Improvement", "Cantrips Known": 3, "Spells Known": 11, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 2}},
            9: {"Features": "Song of Rest (d8)", "Cantrips Known": 3, "Spells Known": 12, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 1}},
            10: {"Features": "Bardic Inspiration (d10), Expertise, Magical Secrets", "Cantrips Known": 4, "Spells Known": 14, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 2}},
            11: {"Features": "", "Cantrips Known": 4, "Spells Known": 15, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1}},
            12: {"Features": "Ability Score Improvement", "Cantrips Known": 4, "Spells Known": 15, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1}},
            13: {"Features": "Song of Rest (d10)", "Cantrips Known": 4, "Spells Known": 16, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1}},
            14: {"Features": "Magical Secrets, Bard College Feature", "Cantrips Known": 4, "Spells Known": 18, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1}},
            15: {"Features": "Bardic Inspiration (d12)", "Cantrips Known": 4, "Spells Known": 19, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1}},
            16: {"Features": "Ability Score Improvement", "Cantrips Known": 4, "Spells Known": 19, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1}},
            17: {"Features": "Song of Rest (d12)", "Cantrips Known": 4, "Spells Known": 20, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1}},
            18: {"Features": "Magical Secrets", "Cantrips Known": 4, "Spells Known": 22, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1, 7: 1, 8: 1, 9: 1}},
            19: {"Features": "Ability Score Improvement", "Cantrips Known": 4, "Spells Known": 22, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 1, 8: 1, 9: 1}},
            20: {"Features": "Superior Inspiration", "Cantrips Known": 4, "Spells Known": 22, "Spell Slots": {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 2, 8: 1, 9: 1}},
        }
        super().__init__(
            'Bard', description, 'd8', ['Charisma'], ['Dexterity', 'Charisma'], 
            ["See the skills frame to the left for a list of skills."], 
            [("a rapier", "a longsword", "any simple weapon"),
             ("a diplomat’s pack", "an entertainer’s pack"),
             ("a lute", "any other musical instrument"),
             "Leather armor", "a dagger"], class_table
        )
        self.ability_priority = ["Charisma", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Strength"]

    def display_class_table(self):
        print(f"Class Table for {self.name}:")
        headers = ["Level", "Features", "Cantrips Known", "Spells Known", "Spell Slots"]
        print("|" + "|".join(f"{header:^15}" for header in headers) + "|")
        print("|" + "|".join(["-" * 15 for _ in headers]) + "|")

        for level, details in self.class_table.items():
            spell_slots = ", ".join(f"{level}st: {slots}" for level, slots in details["Spell Slots"].items())
            print(f"| {level:^15} | {details['Features']:^15} | {details['Cantrips Known']:^15} | {details['Spells Known']:^15} | {spell_slots:^15} |")

class Rogue(DndClass):
    def __init__(self):
        description = "Rogues excel at stealth and deception, using their skills to surprise their enemies and escape danger. At level 1, you may select 4 skills from the options below..."
        class_table = {
            1: {"Features": "Expertise, Sneak Attack, Thieves' Cant", "Sneak Attack": "1d6"},
            2: {"Features": "Cunning Action", "Sneak Attack": "1d6"},
            3: {"Features": "Roguish Archetype, Sneak Attack", "Sneak Attack": "2d6"},
            4: {"Features": "Ability Score Improvement", "Sneak Attack": "2d6"},
            5: {"Features": "Uncanny Dodge", "Sneak Attack": "3d6"},
            6: {"Features": "Expertise", "Sneak Attack": "3d6"},
            7: {"Features": "Evasion", "Sneak Attack": "4d6"},
            8: {"Features": "Ability Score Improvement", "Sneak Attack": "4d6"},
            9: {"Features": "Roguish Archetype feature", "Sneak Attack": "5d6"},
            10: {"Features": "Ability Score Improvement", "Sneak Attack": "5d6"},
            11: {"Features": "Reliable Talent", "Sneak Attack": "6d6"},
            12: {"Features": "Ability Score Improvement", "Sneak Attack": "6d6"},
            13: {"Features": "Roguish Archetype feature", "Sneak Attack": "7d6"},
            14: {"Features": "Blindsense", "Sneak Attack": "7d6"},
            15: {"Features": "Slippery Mind", "Sneak Attack": "8d6"},
            16: {"Features": "Ability Score Improvement", "Sneak Attack": "8d6"},
            17: {"Features": "Roguish Archetype feature", "Sneak Attack": "9d6"},
            18: {"Features": "Elusive", "Sneak Attack": "9d6"},
            19: {"Features": "Ability Score Improvement", "Sneak Attack": "10d6"},
            20: {"Features": "Stroke of Luck", "Sneak Attack": "10d6"},
        }
        super().__init__(
            'Rogue', description, 'd8', ['Dexterity'], ['Dexterity', 'Intelligence'], 
            ['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 
            'Investigation', 'Perception', 'Performance', 'Persuasion', 'Slight of Hand', 
            'Stealth'], 
            [('Rapier', 'Shortsword'), ('Shortbow', 'Shortsword'), 
            ("Burglar's Pack", "Dungeoneer's Pack", "Explorer's Pack"), 
            "Leather Armor", "Dagger", "Dagger", "Thieves' Tools"], 
            class_table
        )
        self.ability_priority = ["Dexterity", "Intelligence", "Constitution", "Wisdom", "Charisma", "Strength"]

# DnD Subclasses
# Barbarian Subclasses
class PathOfTheTotemWarrior(Barbarian):
    def __init__(self):
        super().__init__()
        self.subclass_name = "Path of the Totem Warrior"
        # List subclass features in the description
        self.subclass_description = ("Drawing on the spirits of animals, gaining their powers as a totemic warrior. "
                                     "\n\nFeatures:\n- Spirit Seeker\n- Totem Spirit\n- Aspect of the Beast\n- Spirit Walker\n- Totemic Attunement")

class PathOfWildMagic(Barbarian):
    def __init__(self):
        super().__init__()
        self.subclass_name = "Path of Wild Magic"
        # List subclass features in the description
        self.subclass_description = ("A barbarian infused with wild magic, creating unpredictable magical effects. "
                                     "\n\nFeatures:\n- Wild Surge\n- Magic Awareness\n- Bolstering Magic\n- Unstable Backlash\n- Controlled Surge")

# Bard Subclasses
class CollegeOfLore(Bard):
    def __init__(self):
        super().__init__()
        self.subclass_name = "College of Lore"
        # List subclass features in the description
        self.subclass_description = ("A scholar and a spy, a diplomat and a provocateur, a healer and a slayer. "
                                     "\n\nFeatures:\n- Additional Magical Secrets\n- Bonus Proficiencies\n- Cutting Words\n- Peerless Skill")

class CollegeOfSwords(Bard):
    def __init__(self):
        super().__init__()
        self.subclass_name = "College of Swords"
        # List subclass features in the description
        self.subclass_description = ("Blades perform stunts such as sword swallowing, knife throwing and juggling, and mock combats. "
                                     "\n\nFeatures:\n- Bonus Proficiencies\n- Fighting Style\n- Blade Flourish\n- Extra Attack\n- Master's Flourish")

# Rogue Subclasses
class Assassin(Rogue):
    def __init__(self):
        super().__init__()
        self.subclass_name = "Assassin"
        # List subclass features in the description
        self.subclass_description = ("Specializes in stealth and surprise attacks. Masters of disguise and deadly in their precision. "
                                     "\n\nFeatures:\n- Bonus Proficiencies (disguise kit, poisoner’s kit)\n- Assassinate\n- Infiltration Expertise\n- Impostor\n- Death Strike")

class Thief(Rogue):
    def __init__(self):
        super().__init__()
        self.subclass_name = "Thief"
        # List subclass features in the description
        self.subclass_description = ("Thieves are adept at sneaking, stealing, and using their cunning to gain advantages. "
                                     "\n\nFeatures:\n- Fast Hands\n- Second-Story Work\n- Supreme Sneak\n- Use Magic Device\n- Thief's Reflexes")

# Update get_subclass_by_name function to include Thief
def get_subclass_by_name(subclass_name):
    subclasses = {
        'Path of the Totem Warrior': PathOfTheTotemWarrior(),
        'Path of Wild Magic': PathOfWildMagic(),
        'College of Lore': CollegeOfLore(),
        'College of Swords': CollegeOfSwords(),
        'Assassin': Assassin(),
        'Thief': Thief(),
    }
    return subclasses.get(subclass_name)

# Base character race
class Race:
    def __init__(self, race_name, racial_traits, description):
        self.race_name = race_name
        self.racial_traits = racial_traits
        self.description = description

class Human(Race):
    def __init__(self):
        racial_traits = ["Increase 2 different ability scores by 1", "Gain an additional skill proficiency", "Gain an additional Feat", "Languages: Common and one additional language"]
        description = "Humans are adaptable and amibtious living nearly a centry and reaching adulthood in their late teens. They are Medium creatures at 5-6 feet tall with a walk speed of 30 feet."
        super().__init__("Human", racial_traits, description)

class HalfOrc(Race):
    def __init__(self):
        racial_traits = ["Darkvision", "Menacing", "Relentless Endurance", "Savage Attacks"]
        description = "Half-Orcs inherit a tendency toward chaos from their orc parents and are not strongly inclined toward good.  Larger medium creatures, the half-orcs range from 5 to well over 6 feet tall. Mechanically, they have a cheat-death ability and deal more damate with critical hits."
        super().__init__("Half-Orc", racial_traits, description)

class Tiefling(Race):
    def __init__(self):
        racial_traits = ["Darkvision", "Hellish Resistance", "Infernal Legacy"]
        description = "To be greeted with stares and whispers, to suffer violence and insult on the street, to see mistrust and fear in every eye: this is the lot of the tiefling. They age at the same rate as humans but live a tad longer. They have a walk speed of 30 and are considered Medium creatures."
        super().__init__("Tiefling", racial_traits, description)