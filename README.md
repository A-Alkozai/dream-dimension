- main.py: main entry-point of the project
- GameState.py: Class that manages the whole game. It is in charge of drawing & updating all entities as well as managing ui screens
- vector.py: Class that handles all the positioning and velocity of all 'game objects'
- interaction.py: This handles collision between entities
- entity.py: This is the class which every 'game object' inherits from. It contains important variables such as position, velocity, img_url, etc
- state.py: This file contains entity states
- player.py: This is the class that manages player behaviour, animation, movement, etc
- enemy.py: This is the class that manages enemy behaviour, animation, movement, etc
- projectile.py: This is the class that manages projectile behaviour, animation, movement, etc
- effects.py: This is the class that manages sfx behaviour, animation, etc
- portal.py: This is the class that manages portal behaviour, animation, map change, etc

- map.py: Class that reads the map.json file and creates the map of chosen level
- map.json: In this file is an array of room layouts defining the game map

- welcome_screen.py: This is the main menu that displays when first running the game. It is managed fully by this class
- story_screen.py: This is the story presented before the game begins
- highscore_screen.py: This is the screen that shows your highscore and previous scores  
- control_screen.py: This is the screen that shows the controls to play the game
- credit_screen.py: This is the screen that shows the name of our team members

- scorecounter.py: Class the tracks and displays the score & level during gameplay
- healthbar.py: Class that displays the health of player during gameplay
- mana_bar.py: Class that displays the health of player during gameplay
- slot.py: Class that displays the current attack move the player has selected