# Space Defense
Space Defense is a fun and easy-to-understand 2D defense game. Your goal is to protect your base from waves of enemies by placing defenses. Defeat enemies to gather resources, build more defenses, and survive through levels.

# How to Play
Start the game using a Python interpreter with Pygame library support.
Your base is on the left side, and enemies appear from the right.
Enemies move from right to left, attempting to reach your base. Stop them by setting up defenses.
To place a defense, press 1, 2, or 3 to choose a defense type. Each type has a different resource cost: 50, 200, or 500 resources.
After picking a defense, click on the screen to position it.
Defenses attack enemies automatically when they come within range.
When all enemies are defeated, press Enter to start the next level.
The game ends if your base health reaches 0.

# Game Features
Enemies: Three enemy types with different health and speeds. Stronger and faster enemies appear in higher levels.

Defenses: Three types of defenses with various attributes like attack range, damage, burst damage, and burst rate. Choose the right defense for each situation.

Resources: Collect resources by defeating enemies. Use resources to build defenses and keep your base safe.

Health: Your base health decreases when an enemy reaches it. The game ends when your base health is 0.

# Level class: This class is responsible for generating, moving, and drawing enemies. It also handles level progression and updating enemy health.
generate_enemies(): Creates a specific number of enemies for the current level.

move_enemies(): Updates the position of enemies based on their speed.

draw_enemies(): Draws the enemies on the screen.

next_level(): Starts the next level by increasing the level count and generating new enemies.

# Defense class: This class manages the placement and attacking behavior of defenses.
draw(): Draws the defense on the screen, along with its attack radius.

is_inside_radius(): Checks if an enemy is within the defense's attack range.

The game features simple 2D graphics for the base, enemies, defenses, and background.
