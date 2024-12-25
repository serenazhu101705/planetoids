"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in 
the Planetoids game. Instances of Wave represent a single level, and should 
correspond to a JSON file in the Data directory. Whenever you move to a new 
level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on 
screen. These are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a 
complicated issue. If you do not know, ask on Ed Discussions and we will answer.

# Serena Zhu (srz24) and Aerin Upadhyay (agu2)
# Wednesday, December 11, 2024
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets 
    on screen. It animates all of these by adding the velocity to the position 
    at each step. It checks for collisions between bullets and asteroids or 
    asteroids and the ship (asteroids can safely pass through each other). A 
    bullet collision either breaks up or removes a asteroid. A ship collision 
    kills the player. 
    
    The player wins once all asteroids are destroyed. The player loses if they 
    run out of lives. When the wave is complete, you should create a NEW instance 
    of Wave (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not 
    update. See subcontrollers.py from Lecture 25 for an example. This class 
    will be similar to than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be 
    accessed without going through a getter/setter first. However, just because 
    you have an attribute does not mean that you have to have a getter for it. 
    For example, the Planetoids app probably never needs to access the attribute 
    for the bullets, so there is no need for a getter there. But at a minimum, 
    you need getters indicating whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def set_lives(self, value):
        """
        Sets self._lives
        Parameter: value is the number of lives
        Precondition: value must be an int > 0
        """
        assert isinstance(value, int) and value > 0
        self._lives = value

    def set_lives_label_text(self, text):
        """
        Sets self._lives_label.text
        Parameter: text is the new text
        Precondition: none
        """
        self._lives_label.text = text

    def set_asteroid_label_text(self, text):
        """
        Sets self._asteroid_label.text
        Parameter: text is the new text
        Precondition: none
        """
        self._asteroid_label.text = text

    def set_score_label_text(self, text):
        """
        Sets self._score_label.text
        Parameter: text is the new text
        Precondition: none
        """
        self._score_label.text = text

    def get_lives(self):
        """
        Returns self._lives
        """
        return self._lives
    
    def get_score(self):
        """
        Returns self._score
        """
        return self._score
    
    def get_asteroid_count(self):
        """
        Returns len(self._asteroids)
        """
        return len(self._asteroids)
    
    def get_hit(self):
        """
        Returns self._hit
        """
        return self._hit
    
    def get_lives_label(self):
        """
        Returns self._lives_label
        """
        return self._lives_label
    
    def get_asteroid_label(self):
        """
        Returns self._asteroid_label
        """
        return self._asteroid_label

    
    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self, data):
        """
        Initializes Wave object
        Parameter
        """
        self._data = data
        self._ship = Ship(position = self._data['ship']['position'], \
                          angle = self._data['ship']['angle'])
        self._asteroids = []
        self.create_asteroids(self._data['asteroids']) 
        self._bullets = []
        self._last_shot = BULLET_RATE
        self._lives = SHIP_LIVES
        self._hit = False
        self._reset_ship_time = 0
        self._life_lost = False
        self._score = 0
        self._asteroid_label = GLabel(text = f"Asteroids\n Left: \n{len(self._asteroids)}", \
                                font_size = 20, font_name = MESSAGE_FONT, x = 50, y = 650)
        self._lives_label = GLabel(text = f"Lives\n Left: \n{self._lives}", \
                                font_size = 20, font_name = MESSAGE_FONT, x = 750, y = 650)
        self._score_label = GLabel(text = f"Score: \n{self._score}", \
                                font_size = 20, font_name = MESSAGE_FONT, x = 400, y = 650)

    def create_asteroids(self, data):
        for i in data:
            size = i['size']
            position = i['position']
            direction = i['direction']    
        
            if size == 'small':
                image, width, height, speed = SMALL_IMAGE, SMALL_RADIUS*2,\
                      SMALL_RADIUS*2, SMALL_SPEED
                            
            if size == 'medium':
                image, width, height, speed = MEDIUM_IMAGE, MEDIUM_RADIUS*2, \
                    MEDIUM_RADIUS*2, MEDIUM_SPEED
                
            if size == 'large':
                image, width, height, speed = LARGE_IMAGE, LARGE_RADIUS*2, \
                    LARGE_RADIUS*2,  LARGE_SPEED

            a = Asteroid(size=size, position = position, \
                        direction = direction, image = image, width = width, \
                            height = height)
            
            self._asteroids.append(a)
    
    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self, dt, input):
        self._ship.turn(dt, input)
        self._ship.update(dt)
        for i in self._asteroids:
            i.update(dt)

        if input.is_key_down('spacebar') and self._last_shot >= BULLET_RATE:
            p = (self._ship.x, self._ship.y)
            f = (self._ship.get_facing().x, self._ship.get_facing().y)
            b = (p[0] + f[0] * SHIP_RADIUS, p[1] + f[1] * SHIP_RADIUS)
            v = (f[0] * BULLET_SPEED, f[1] * BULLET_SPEED)
            self._bullets.append(Bullet(b, v))
            self._last_shot = 0

        self.collide()
            
        if self._last_shot < BULLET_RATE:
            self._last_shot += 1

        self.remove_bullets(dt)

        if self._reset_ship_time < 200:
            self._reset_ship_time += 1

        if self._reset_ship_time == 200:
            self._life_lost = False        
        
    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self, view):
        self._ship.draw(view)
        for i in self._asteroids:
            i.draw(view)
        for i in self._bullets:
            i.draw(view)
        self._asteroid_label.draw(view)
        self._lives_label.draw(view)    
        self._score_label.draw(view)    

    def remove_bullets(self, dt):
        i = 0
        while i < len(self._bullets):
            b = self._bullets[i]
            b.update(dt)
            #horizontal wrapping
            if b.x < -DEAD_ZONE or b.x > GAME_WIDTH + DEAD_ZONE or \
                b.y < -DEAD_ZONE or b.y > GAME_WIDTH + DEAD_ZONE:
                self._bullets.remove(b)
            else:
                i += 1

    def overlap(self, one, two):
        d = math.sqrt((two.x - one.x)**2 + (two.y - one.y)**2)
        r1 = one.width / 2
        r2 = two.width / 2
        r = r1 + r2
        return d < r
    
    def collide(self):
        db = []
        da = []
        hit = False
        for i in self._bullets:
            for el in self._asteroids:
                if self.overlap(i, el):
                    db.append(i)
                    da.append(el)
                    hit = True
                    if el.width > SMALL_RADIUS * 2:
                        self.break_ast(el, i._velocity)
                    break
        if hit:
            self._score += 1

        self._bullets = [i for i in self._bullets if i not in db]
        self._asteroids = [i for i in self._asteroids if i not in da]

        if self._ship:
            for i in self._asteroids:
                if self.overlap(self._ship, i):
                    if not self._life_lost:
                        self._lives -= 1
                        self._hit = True
    
    def break_ast(self, asteroid, velocity):
        size = 'medium' if asteroid._size == 'large' else 'small'
        radius = MEDIUM_RADIUS if asteroid._size == 'large' else SMALL_RADIUS
        speed = MEDIUM_SPEED if asteroid._size == 'large' else SMALL_SPEED
        image = MEDIUM_IMAGE if asteroid._size == 'large' else SMALL_IMAGE

        collision = Vector2(velocity[0], velocity[1]).normalize()
        resultants = [collision]

        for i in [120, -120]:
            theta = math.radians(i)
            x = collision.x * math.cos(theta) - collision.y * math.sin(theta)
            y = collision.x * math.sin(theta) + collision.y * math.cos(theta)
            resultants.append(Vector2(x, y).normalize())

        for i in resultants:
            position = (asteroid.x + i.x * radius, asteroid.y + i.y * radius)
            velocity = (i.x * speed, i.y * speed)
            self._asteroids.append(Asteroid(size, position, (i.x, i.y), image, radius * 2, \
                                            radius * 2))
    
    # RESET METHOD FOR CREATING A NEW LIFE
    def reset_ship(self):
        self._ship = Ship(position = self._data['ship']['position'], \
                          angle = self._data['ship']['angle'])
        
        self._hit = False
        self._reset_ship_time = 0
        self._life_lost = True

    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION        

