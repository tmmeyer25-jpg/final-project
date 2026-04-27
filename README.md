Fish vs Sharks
A simple arcade-style shooter built with Python and Pygame. You play as a small fish defending yourself against a wave of sharks descending from above.
Gameplay
Pilot your fish left and right across the bottom of the screen and shoot bubbles upward to take out the sharks before they reach you. The longer you survive, the faster and more frequently the sharks appear — so stay sharp.
A-Move left→ / D-Move right/ Space-Shoot
Scoring
You earn 10 points per shark destroyed. Your final score is shown on the game over screen.
Tips
Sharks spawn at random horizontal positions and swim straight down — learn to prioritize the ones heading directly for you.
You don't have unlimited bullets on screen, so shoot steadily rather than spamming.
The game gets progressively harder as your score climbs, so an early lead helps.
What I Enjoyed
The most satisfying part was drawing the characters entirely with primitive shapes — ellipses, polygons, and circles. It's a small thing, but seeing a flat grey rectangle transform into a recognisable shark with a dorsal fin, a beady eye, and a pale belly stripe felt genuinely rewarding. The same goes for the fish: giving it a tail, a top fin, and a little glinting eye made the player character feel alive in a way a plain ellipse never could. There's something charming about lo-fi pixel-art style creatures built out of basic geometry.
Challenges
The trickiest part was the enemy movement redesign. The original sharks moved side-to-side and bounced off walls, which gave the game a classic Space Invaders feel. Switching to top-to-bottom movement meant rethinking the spawn logic entirely — sharks no longer needed a starting Y range or a lateral direction, just a random X position and a downward speed. Simple in the end, but it required careful cleanup to avoid leftover bounce logic causing weird behaviour.
What I Learned
How much game feel comes from speed tuning rather than content. Halving a few numbers made the game feel like a completely different experience.
