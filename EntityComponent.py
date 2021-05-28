import pygame
from pygame.math import Vector2

pygame.init()

#Entity Component System-------------------------------------------------
#The EntitiyManager adds, deletes and keeps track of all entities
class EntityManager():
    def __init__(self):
       self.entityCounter = 0  # Used to assign a unique ID to entities
       self.entities = []  # Holds all entities

    def addEntity(self, entity):
        self.entities.append(entity)

    def destroyEntity(self, entity):
        # Add the ID to a list to be reused for future entities
        self.entities.remove(entity)

#Fundamental game object, this could be a player, monster, rock, book, etc...
class Entity():
    def __init__(self, EM, componentList):
        self.ID = EM.entityCounter
        EM.entityCounter += 1
        EM.addEntity(self)

        self.components = {}
        for component in componentList:
           self.components[component.name] = component


#Components are added to entities to give them functionality, such as movement or health
class Component():
    def __init(self):
        self.name = ""

    def run(self):
        pass

class MoveComponent(Component):
    def __init__(self, move):
        self.name = "MoveComponent"
        self.move = move

    def run(self):
        print(self.move)


class PositionComponent(Component):
    def __init__(self, position):
        self.name = "PositionComponent"
        self.position = position

    def run(self):
        print(self.pos)


class TargetComponent(Component):
    def __init__(self):
        self.name = "TargetComponent"
        self.target = Vector2()
        self.angle = 0

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
    def __init__(self, size):
        self.name = "SizeComponent"
        self.width = size.x
        self.height = size.y

    def increaseSize(self):
        pass

    def decreaseSize(self):
        pass

    def run(self):
        pass


class TextureComponent(Component):
    def __init__(self, textureFile, textureOriginList):
        self.name = "TextureComponent"
        self.texture = pygame.image.load(textureFile)
        #self.texture.convert()  # This loads the image faster when drawing

        # Origin points for chosing the correct texture(s)
        self.textureOriginList = textureOriginList
        self.textureSurfaceList = []

    def run(self):
        pass


class RenderComponent(Component):
    def __init__(self):
        self.name = "RenderComponent"

    def run(self):
        pass


#Systems use an Entity's componets and apply logic to change the gamestate
class System():
    def __init__(self):
        pass

    def run(self):
        pass


class MovementSystem(System):
    def __init__(self, EM, entities):
        self.entities = entities

    def run(self):
        for entity in self.entities:
            if entity.componets.get("MoveComponent"):
                #Move the unit
                pass

    def debug(self):
        for entity in self.entities:
            if entity.componets.get("MoveComponent"):
                print("MoveComponet Initialized")


class RenderSystem(System):
    def __init__(self, EM):
        self.entities = EM.entities
        self.position = None
        self.surface = None

    def prepareSurface(self, entity):
        #Position
        self.position = entity.components["PositionComponent"].position

        #Texture surfaces
        for origin in self.textureOriginList:
            width = entity.components["SizeComponent"].width
            height = entity.components["SizeComponent"].height
            texture = pygame.Rect(int(origin.x), int(origin.y), width, height)
            self.textureSurfaceList.append(texture)

        #Surface/texture
        self.surface = 0

    def renderTile(self, pos, tile, gamestate):
	    cellSize = gamestate.cellSize
	    window = gamestate.window

	    #Position, scaled to the games cell size
	    tilePos = pos.elementwise() * cellSize

	    #Texture
	    textureOrigin = tile.elementwise() * cellSize
	    textureRect = pygame.Rect(int(textureOrigin.x), int(textureOrigin.y), cellSize.x, cellSize.y)

	    #Draw tile to the pygame surface
	    window.blit(self.texture, tilePos, textureRect)

    def render(self, window):
        #Draw tile surface to the window surface
	    window.blit(self.surface, self.position)

    def run(self):
        for layer in self.layers:
            self.prepareSurface()
            self.render()

    def debug(self):
        for entity in self.entities:
            if entity.componets.get("RenderComponent"):
                print("RenderComponet Initialized")


class TargetSystem(System):
    def __init__(self, EM, entities):
        self.entities = entities

    def run(self):
        pass

    def debug(self):
        for entity in self.entities:
            if entity.componets.get("TargetComponent"):
                print("Targeting Initialized")


class ShootingSystem(System):
    def __init__(self, EM, entities):
        self.entities = entities

    def run(self):
        for entity in self.entities:
            if entity.componets.get("ShootComponent"):
                #Determine if the unit can shoot
                pass

    def debug(self):
        for entity in self.entities:
            if entity.componets.get("ShootComponent"):
                print("Shooting Initialized")

EM = EntityManager()
e1 = Entity(EM, [PositionComponent(Vector2(200, 200)), TargetComponent(), ShootComponent(), SizeComponent(Vector2(64, 64)), TextureComponent("Assets\\units.png", [Vector2(0, 0)]), RenderComponent()])

RS = RenderSystem(EM)
RS.prepareSurface(e1)
