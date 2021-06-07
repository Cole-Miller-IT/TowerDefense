from Layers import UnitLayer
import pygame
import math
from pygame.math import Vector2
from pygame.locals import *

import GameState

pygame.init()

#https://www.letsdevelopgames.com/2020/10/entity-component-system-in-python-code.html
#Entity Component System-------------------------------------------------
#The EntitiyManager adds, deletes and keeps track of all entities


class EntityManager():
    def __init__(self):
       self.entityCounter = 0  # Used to assign a unique ID to entities
       self.entities = []  # Holds all entities

    def addEntity(self, entity):
        self.entities.append(entity)

    def destroyEntity(self, entity):
        self.entities.remove(entity)

#Fundamental game object, this could be a player, monster, rock, book, etc... that is made of components


class Entity():
    def __init__(self, EM, componentList):
        self.ID = EM.entityCounter
        EM.entityCounter += 1
        EM.addEntity(self)

        self.components = {}
        for component in componentList:
           self.components[component.name] = component

        #Initialize textures
        if self.components.get("TextureComponent"):
            self.components["TextureComponent"].prepareSurfaces(self)

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

    def increaseSize(self):
        pass

    def decreaseSize(self):
        pass

    def run(self):
        pass

#Store info about a texture for an Entity


class TextureObject():
    def __init__(self, origin, name=None):
        self.name = name
        self.angle = 0
        self.origin = origin  # Holds the origin points to select the texture from a spritesheet
        self.originRect = None      #
        self.Rect = None            #
        self.surface = None  # Is a surface that contains the texture


class TextureComponent(Component):
    def __init__(self, textureFile, textureOriginList):
        self.name = "TextureComponent"
        self.spritesheet = pygame.image.load(textureFile)
        #self.texture.convert()  # This loads the image faster when drawing

        # Origin points for chosing the correct texture(s)
        self.textureOriginList = textureOriginList
        self.textureSurfaceList = []
        self.textureObjects = []

        #For every origin point/every texture create a texture object and store it in a list
        for origin in self.textureOriginList:
            textureObject = TextureObject(origin)
            self.textureObjects.append(textureObject)

    #Creates a list of surfaces/textures that can be rendered to create the visible entity on the screen
    def prepareSurfaces(self, entity):
        width = entity.components["SizeComponent"].width
        height = entity.components["SizeComponent"].height
        posX = entity.components["PositionComponent"].x
        posY = entity.components["PositionComponent"].y

        #For every texture, create a surface
        for texture in entity.components["TextureComponent"].textureObjects:
            #This Rect holds the values to choose the correct texture from the spritesheet
            texture.originRect = pygame.Rect(
                texture.origin.x, texture.origin.y, width, height)
            texture.surface = pygame.Surface((width, height), pygame.SRCALPHA)

            #Blits the spritesheet onto the Surface at point (0,0). originRect controls what part
            # of the spritesheet is choosen to blit to the surface
            texture.surface.blit(self.spritesheet, (0, 0), texture.originRect)

            #Create a copy of the surface
            originalTextureSurface = texture.surface.copy()

            #Create a Rect() that holds the current texture's position
            texture.Rect = pygame.Rect(posX, posY, width, height)

            #Check if the texture should be rotated
            if texture.angle != 0:
                #Rotate surface
                texture.surface, texture.Rect = self.rotateSurface(
                    originalTextureSurface, texture.angle, texture.Rect)

    #
    def rotateSurface(self, surface, angle, rect):
        #Rotate a surface by angle in degrees
        rotated_image = pygame.transform.rotate(surface, angle)

        #Compute the new Rect by setting it's center to the center of the pre-rotated surface's
        new_rect = rotated_image.get_rect(center=rect.center)

        return rotated_image, new_rect

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
    def __init__(self, EM):
        pass

    #Move an entity
    def move(self, entity):
        if entity.components.get("MoveComponent") and entity.components.get("PositionComponent"):
            moveVector = entity.components["MoveComponent"].move
            posX = entity.components["PositionComponent"].x
            posY = entity.components["PositionComponent"].y
            #print(posY)
            newPos = Vector2()
            newPos.x = posX + int(moveVector.x)
            print(int(moveVector.x))
            print(type(posX))
            
            worldSize = Vector2(500, 500)  # Get from gamestate, change later

            #Check if the entity would go outside the worldSize
            if newPos.x < 0 or newPos.x > worldSize.x \
                or newPos.y < 0 or newPos.y > worldSize.y:
                print(newPos)
                return

            #Check if the entity collides with another unit
            #if unit collids with another unit:
            #collision

            #Check if the entity collides with a wall

            #If the newPos doesn't conflict with anything update position
            entity.components["PositionComponent"].x = entity.components["PositionComponent"].x + int(moveVector.x)
            entity.components["PositionComponent"].y = entity.components["PositionComponent"].y + int(moveVector.y)

    def run(self):
        pass

    def debug(self):
        for entity in self.entities:
            if entity.componets.get("MoveComponent"):
                print("MoveComponent Initialized")


class RenderSystem(System):
    def __init__(self, EM, window):
        self.EM = EM
        self.entities = EM.entities
        self.window = window
        self.layers = []

    #Draw the entity on the screen
    def renderEntity(self, entity):
        for textureObject in entity.components["TextureComponent"].textureObjects:
            #Draw tile surface to the window surface
            self.window.blit(textureObject.surface, textureObject.Rect)

    #Render a layer, such as all the ground or units entities
    def renderLayer(self, layer):
        for entity in layer:
            self.renderEntity(entity)

    #Creates a 2D list that contains entities
    def create2DLayer(self, positionList, spritesheet):
        layer = []

        #Get variables from gamestate later
        worldSize = Vector2(3, 2)
        cellSizeX = 64
        cellSizeY = 64

        for y in range(int(worldSize.y)):
            for x in range(int(worldSize.x)):
                originPoint = positionList[y][x]
                posX = x * cellSizeX
                posY = y * cellSizeY
                if originPoint is not None:
                    layer.append(Entity(self.EM, [PositionComponent(posX, posY),
                                                  SizeComponent(cellSizeX, cellSizeY), TextureComponent(spritesheet, [originPoint]), RenderComponent()]))

        return layer

    #Draw all entities to the screen for the current game loop
    def run(self):
        pass

    def debug(self):
        for entity in self.entities:
            if entity.componets.get("RenderComponent"):
                print("RenderComponet Initialized")


class TargetSystem(System):
    def __init__(self, EM):
        pass

    def run(self, entity):
        pass

    #Computes the angle (in degrees) based on where the point is on the 2D plane
    def target(self, entity):
        if entity.components.get("TargetComponent") and entity.components.get("TextureComponent") \
                and entity.components.get("PositionComponent"):

            entityX = entity.components["PositionComponent"].x
            entityY = entity.components["PositionComponent"].y
            targetX = int(entity.components["TargetComponent"].target.x)
            targetY = int(entity.components["TargetComponent"].target.y)

            #Computes the angle in radians based on the unit's position and where it's looking
            theta = math.atan2(targetY - entityY, targetX - entityX)
            angle = math.degrees(theta)  # Convert to degrees

            return angle

        else:
            print("Component not installed. Target system")

    def debug(self):
        for entity in self.entities:
            if entity.components.get("TargetComponent"):
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


'''

https://en.wikipedia.org/wiki/Observer_pattern
class Observable:
    def __init__(self) -> None:
        self._observers = []
    
    def register_observer(self, observer) -> None:
        self._observers.append(observer)
    
    def notify_observers(self, *args, **kwargs) -> None:
        for observer in self._observers:
            observer.notify(self, *args, **kwargs)

class Observer:
    def __init__(self, observable) -> None:
        observable.register_observer(self)
    
    def notify(self, observable, *args, **kwargs) -> None:
        print("Got", args, kwargs, "From", observable)


subject = Observable()
observer = Observer(subject)
subject.notify_observers("test")'''


class GameMode():
    def processInput(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()

    def quitGame(self):
        pass


class PlayGameMode(GameMode):
    def __init__(self):
        super().__init__()  # Inherit all the properties and methods of the parent class
        self.EM = EntityManager()
        self.RS = RenderSystem(self.EM, window)
        self.MS = MovementSystem(self.EM)
        self.TS = TargetSystem(self.EM)

        self.running = True
        self.counterChange = False
        ground = [
            [Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)],
            [Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)],
        ]

        layer = self.RS.create2DLayer(ground, "Assets\Ground.png")
        self.RS.layers.append(layer)

        self.player1 = Entity(self.EM, [PositionComponent(200, 200), TargetComponent(), ShootComponent(), SizeComponent(
            32, 32), TextureComponent("Assets\\Units.png", [Vector2(32, 0), Vector2(64, 0)]), RenderComponent(), MoveComponent(Vector2(0, 0))])

        self.e1 = Entity(self.EM, [PositionComponent(400, 200), TargetComponent(), ShootComponent(), SizeComponent(
            64, 64), TextureComponent("Assets\Ground.png", [Vector2(128, 0), Vector2(160, 0)]), RenderComponent()])

        unitLayer = []
        unitLayer.append(self.player1)
        self.RS.layers.append(unitLayer)

    def processInput(self):
        for event in pygame.event.get():
            # If the user has clicked on the 'X' box, close the game
            if event.type == pygame.QUIT:
                self.running = False
            # If the user has pressed down on the keyboard, handle the input
            elif event.type == pygame.KEYDOWN:
                #Move up
                if event.key == pygame.K_w:
                    self.player1.components["MoveComponent"].move = Vector2(0, -10)
                #Move left
                elif event.key == pygame.K_a:
                    self.player1.components["MoveComponent"].move = Vector2(-10, 0)
                #Move down
                elif event.key == pygame.K_s:
                    self.player1.components["MoveComponent"].move = Vector2(0, 10)
                #Move right
                elif event.key == pygame.K_d:
                    self.player1.components["MoveComponent"].move = Vector2(10, 0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player1.components["TargetComponent"].targetedPoint = pygame.mouse.get_pos()
                self.counterChange = True
            else:
                pass

    def update(self):
        #Move player
        self.MS.move(self.player1)

        #Rotate turret
        if self.counterChange:
            angle = self.TS.target(self.player1)
            self.player1.components["TextureComponent"].textureObjects[1].angle = angle
            self.player1.components["TextureComponent"].prepareSurfaces(
                self.player1)
            self.counterChange = False

    def render(self):
        #Clear the previous frame
        window.fill((0, 0, 0))

        #Render layers
        for layer in self.RS.layers:
            self.RS.renderLayer(layer)

        pygame.display.update()


window = pygame.display.set_mode((500, 500))
game = PlayGameMode()
while game.running:
    game.processInput()

    game.update()

    game.render()


pygame.quit()
