try:
    import sys
    import pygame
    import math
    from pygame.math import Vector2
    from pygame.locals import *
    
except ImportError as er:
    print("Error importing modules")
    print(er)
    sys.exit(2)

#Entity Component System-------------------------------------------------
#The EntitiyManager adds, deletes and keeps track of all entities
class EntityManager():
    def __init__(self):
       self.entityCounter = 0                   #Used to assign a unique ID to entities
       self.entities = []                       #Holds all entities
       self.texturedEntitiesNotPrepared = []    #Holds entities whose textures are not yet loaded

    def addEntity(self, entity, array):
        array.append(entity)

    def destroyEntity(self, entity, array):
        array.remove(entity)

#Fundamental game object, this could be a player, monster, rock, book, etc... that is made of components
class Entity():
    def __init__(self, EM, componentList):
        self.ID = EM.entityCounter
        EM.entityCounter += 1
        EM.addEntity(self, EM.entities)

        self.components = {}
        for component in componentList:
           self.components[component.name] = component

        #Entity is added to a list to initialize textures
        if self.components.get("TextureComponent"):
            EM.addEntity(self, EM.texturedEntitiesNotPrepared)


#Components are added to entities to give them functionality, such as movement or health
class Component():
    def __init(self):
        self.name = ""

    def run(self):
        pass


class MoveComponent(Component):
    def __init__(self, moveVector):
        self.name = "MoveComponent"
        self.move = moveVector

    def run(self):
        print(self.move)


class PositionComponent(Component):
    def __init__(self, x, y):
        self.name = "PositionComponent"
        #x and y refer to the center points of the entity
        self.x = x
        self.y = y

    def run(self):
        pass


class TargetComponent(Component):
    def __init__(self):
        self.name = "TargetComponent"
        self.targetedPoint = None

    def run(self):
        pass


class ShootComponent(Component):
    def __init__(self):
        self.name = "ShootComponent"
        self.fireRate = 1

    def run(self):
        pass


class HealthComponent(Component):
    def __init__(self, health):
        self.name = "HealthComponent"
        self.health = health

    def run(self):
        pass


class SizeComponent(Component):
    def __init__(self, width, height):
        self.name = "SizeComponent"
        self.width = width
        self.height = height

    def run(self):
        pass

#Store info about a texture for an Entity
class TextureObject():
    def __init__(self, origin, name=None):
        self.name = name            #Used to update certain textures, eg. the name is "turret" so when
                                    #rotateTurret() is called it applies to this specific textureObject
        self.angle = 0              #What angle the texture should be rotated at (in degrees)
        self.origin = origin        #Holds the origin points to select the texture from a spritesheet
        self.originRect = None      #Use to select an area in the spritesheet for the texture
        self.Rect = None            #Contains the location info needed to draw it to the main window
        self.surface = None         #A surface that contains the texture

class TextureComponent(Component):
    def __init__(self, textureFile, textureOriginDict):
        self.name = "TextureComponent"
        self.spritesheet = pygame.image.load(textureFile)
        #self.texture.convert()  # This loads the image faster when drawing

        #Origin points for chosing the correct texture(s)
        self.textureOriginDict = textureOriginDict
        self.textureObjects = []

        #For every origin point/every texture in the dict, create a texture object and store it in a list
        for key in self.textureOriginDict:
            textureObject = TextureObject(self.textureOriginDict[key], key)
            self.textureObjects.append(textureObject)

    def run(self):
        pass


class RenderComponent(Component):
    def __init__(self):
        self.name = "RenderComponent"

    def run(self):
        pass
