# TTRPG-Character-Creation-Application
A tool for character creation to be used with D&amp;D 5e.


Description: Tool for creating and managing characters for Dungeons & Dragons 5e. Includes the ability to fully customize new characters in a quick and easy fashion. For even quicker results, the application can automatically generate a random character.

Table of Contents:
- Installation
- Usage
-- Main Menu
-- Character Creation
-- Character Sheet
-- Dice Roller
-- Character Lists
- Administrator Account
- Roadmap
- Support

------------------

Installation

- Download the zipped file "RPG-Char-App.zip."
- Windows Defender does not typically allow downloads of .exe files. This is for very good reason. However, in order to run this application you must go into Windows Defender and allow "RPG-Char-App" on your device. 
- Unzip the file and place it in your desired directory.
- In the RPG-Char-App folder, search for and double click on "main.exe" to run the application.
- Windows Defender SmartScreen may prevent the .exe from running. Click on "More info" and then "Run anyway."

------------------
Usage
------------------
On first time usage, you will be required to register a user. Your username, password, and email address are currently only used within the application and stored on your PC. No information is currently collected and sent outside of the application.
- Usernames and Emails are unique per database. Emails must be formated as email@email.com for validation.

After registering a new user account, log in with your valid credentials. This will bring you into the Main Menu.

Main Menu
 - Character Creation - Takes the user to the Character Creation screen to create, generate, and save new characters.
 - Dice Roller - Opens the Dice Roller frame that allows for the rolling of D&D 5e dice, coin flips, and % rolls.
 - Character Lists - Takes the user to the complete list of characters associated with their account. Clicking on a character will open that character's completed Character Sheet.
 - Logout - Logs the user out and returns to the Login/Registration window.

Character Creation
 - Follow along with the instructions in the "Description" frame to create a new character for D&D 5e. The "Description" frame will update at each item selection with descriptions of that item. To go back and review a description, simply click on the item you wish to review.
 - Enter a name, select a race, background, starting class, the amount of levels taken into that class, and a subclass if you have at least 3 levels in that class.
 - The "Select Subclass" dropdown will only populate if you have at least 3 levels taken in a given class. 
 - You may select multiple classes by clicking the "Add Multiclass" button.
 - Use the "Select Skills" checkboxes to select your skills. Your class selection may change the amount of skills you can select. See the "Description" frame for more information.
- Either manually enter your ability scores as your local Dungeon Master dictates or click the "Roll Stats" button on the bottom right section of the Character Creation window. This button rolls 4 6-sided dice and removes the lowest value a total if 6 times, as dictated by the D&D 5e character creation rules. It then uses your class selection to dictate where those values are placed under in your ability scores. Feel free to move those values around as you wish.
- Alternatively, those who are short on time or patience may simply click the "You Do It" button to randomly generate a brand new character. However, this method does not select your skills, levels, subclass, and feats for you so make sure you take that into account when you choose this method.
- When you are finished, click the "Save Character" button to open their character sheet.

Character Sheet
The Character Sheet holds all playable information for your character. 
- It displays your character's name, class, levels, and subclasses as well as automatically calculating the correct modifiers, AC, Health, Initiative, and Proficiency Bonus.
- Your skills are on the left side of the sheet and are displayed next to their associated modifier. Skills you selected that you are proficient in during character creation are notified with a "*". Some classes will allow you to pick skills to gain expertise in at higher levels. You may do this by checking the box next to the associated skill. Bards get an ability at level 2 that increase the modifier for all non-proficient skills by half of their proficiency bonus. This is also taken into account when modifiers are calculated. Click the skill to roll the dice with your associated modifiers. 
- The Dice Roller simmulates rolling dice and displays the totals in the Dice Roll Results. Use the dropdown to select the number of dice you want to roll when clicking the button.
- The Inventory pane allows you to select different armor types which is used to calculate your AC. If you do not choose an armor, your AC will default to 10 + your dexterity modifier. Feel free to add in extra AC if you have items or need for it in the "Shield/AC Bonus" dropdown. The armor values are calculated as show below:
 No Armor: Default
 Light Armor: AC = Armor Value + Dex Mod + Shield/ AC Bonus
 Medium Armor: AC = Armor Value + Dex Mod(with a maximum of +2) + Shield/ AC Bonus
 Heavy Armor: AC = Armor Value + Shield/ AC Bonus
- Your character is saved to your character list which is accessible from the Main Menu

Dice Roller
- Simmulates dice rolls for D&D games and more.
- Use the dropdown to select the number of dice to roll and click a button.
- the "Flip Coin" button displays either a 1 or a 2.
	1 = Heads
	2 = Tails

Character List
- The Character List holds a list of all of the current user's characters. It displays them in the format "Name - Classes Levels - Race, background"
- Click on the "New Character" button to create a new character and add it to the list.
- Click on a character to access their character sheet.
- Click on the "Delete Character" button to delete the character from the user's account. This is not reversable.

------------------

Administrator Account
- There is currently only 1 administrator account. It is used to remove users and characters from the application. In order to add another administrator, or give administrator privilages to another user, the database must be edited directly. I will not be providing instructions on that aspect of the application.
- To access the admin panel, use the following login credentials.

	Username: rrucio
	Password: pass

- The Main Menu will appear as normal but there will be an additional "Admin Panel" button. Clic it to access the admin panel.
- The UI color will change to green and a list of users on the local instance of the application will be displayed. These users may be delted by clicking on the "Delete" button.
- Clicking on a user displays a list of their characters on the right. Delete those characters by clicking on the associated character button.

------------------
Roadmap
------------------
Future updates will include additional improvements to UI, accessibilty, security, and functionality. Below are currently planned updates to be implemented before live distribution.
- Add all D&D 5e classes, subclasses, races, backgrounds, and feats.
- Add increased functionality to Character Sheet
-- Skill Saves, Skill Checks, Customizable Inventory, Savable Notes, Character Level-Up/Edit, Character Art and Bio
- Incrase credential security
-- More in-depth password encryption and email validation.
- UI Art and Icon
- Discord API integration
- Mobile application conversion

------------------
Credits
------------------
Nathan Storey - Author, Artist, Developer
UI Libraries - tkinter, customtkinter
Programming Language - Pyton
Platform - Visual Studio Code

Capstone Project - Davenport University
CSCI
------------------
Support
------------------

Nathan Storey - Developer
email: rruciogames@gmail.com

