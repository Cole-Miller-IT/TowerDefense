from os import X_OK
import pygame
import math
from pygame.math import Vector2

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

        self.components["TextureComponent"].prepareSurfaces(self)
        #Creates texture surfaces for rendering
        '''if self.components["TextureComponent"] and self.components["SizeComponent"]:
            try:
                self.components["TextureComponent"].prepareSurfaces(self)
            except:
                print("Error preparing texture surfaces.")'''


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
    def __init__(self, x, y):
        self.name = "PositionComponent"
        self.x = x
        self.y = y

    def run(self):
        print(self.pos)


class TargetComponent(Component):
    def __init__(self):
        self.name = "TargetComponent"
        self.target = Vector2()

    #Computes the angle (in degrees) based on where the point is on the 2D plane
    def target(self, entity, targetedPoint):
        entityX = entity.components["PositionComponent"].x
        entityY = entity.components["PositionComponent"].y

        #Computes the angle in radians based on the unit's position and where it's looking
        theta = math.atan2(targetedPoint.y - entityY, targetedPoint.x - entityX)
        angle = math.degrees(theta)  # Convert to degrees
        return angle

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


class TextureObject():
    def __init__(self, origin):
        self.angle = 0
        self.origin = origin
        self.originRect = None
        self.surface = None

    def update(self):
        #update angle
        pass
        #update surface


class TextureComponent(Component):
    def __init__(self, textureFile, textureOriginList):
        self.name = "TextureComponent"
        self.spritesheet = pygame.image.load(textureFile)
        #self.texture.convert()  # This loads the image faster when drawing

        # Origin points for chosing the correct texture(s)
        self.textureOriginList = textureOriginList
        self.textureSurfaceList = []
        self.textures = []

        for origin in self.textureOriginList:
            textureObject = TextureObject(origin)
            self.textures.append(textureObject)

    #Creates a list of surfaces/textures that can be rendered to create the visible entity on the screen
    def prepareSurfaces(self, entity):
        width = entity.components["SizeComponent"].width
        height = entity.components["SizeComponent"].height
        posX = entity.components["PositionComponent"].x
        posY = entity.components["PositionComponent"].y
        rotatedSurface = None

        entity.components["TextureComponent"].textureSurfaceList.clear()

        #For every texture create a surface
        for texture in self.textures:
            #This Rect holds the values to choose the correct texture from the spritesheet
            self.originRect = pygame.Rect(texture.origin.x, texture.origin.y, width, height)
            texture.surface = pygame.Surface((width, height), pygame.SRCALPHA)

            #Blits the spritesheet onto the Surface at point (0,0). originRect controls what part 
            # of the spritesheet is choosen to blit to the surface
            texture.surface.blit(self.spritesheet, (0, 0), self.originRect)

            #Check if the texture should be rotated
            if texture.angle != 0:
                rotatedSurface, newPosRect = self.rotateSurface(texture.surface, width, height, texture.angle, texture, self.originRect, posX, posY)
                entity.components["TextureComponent"].textureSurfaceList.append(rotatedSurface)

            else:
                entity.components["TextureComponent"].textureSurfaceList.append(texture.surface)

    def rotateSurface(self, surface, width, height, angle, texture, textureRect, x, y):
        # Create a pygame surface, then blit the tile/units texture onto the surface at origin (0,0)
        tempSurface = pygame.Surface((width, height), pygame.SRCALPHA)
        tempSurface.blit(surface, (0, 0), textureRect)

        # Rotate the tile
        rotatedSurface = pygame.transform.rotate(tempSurface, angle)

        newPosRect = rotatedSurface.get_rect(center=(x, y))

        return (rotatedSurface, newPosRect)

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

    #Draw the entity on the screen
    def render(self, window, entity):
        for surface in entity.components["TextureComponent"].textureSurfaceList:
            #Draw tile surface to the window surface
            x = entity.components["PositionComponent"].x
            y = entity.components["PositionComponent"].y
            window.blit(surface, (x, y))

    def run(self):
        pass

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


pygame.init()
window = pygame.display.set_mode((500, 500))
running = True

EM = EntityManager()
e1 = Entity(EM, [PositionComponent(200, 200), TargetComponent(), ShootComponent(), SizeComponent(
    64, 64), TextureComponent("Assets\ground.png", [Vector2(0, 0), Vector2(300, 300)]), RenderComponent()])

e2 = Entity(EM, [PositionComponent(200, 200), TargetComponent(), ShootComponent(), SizeComponent(
    64, 64), TextureComponent("Assets\ground.png", [Vector2(0, 0), Vector2(124, 100)]), RenderComponent()])

RS = RenderSystem(EM)

counter = 1
while running:
# Event Handler
    for event in pygame.event.get():
        # If the user has clicked on the 'X' box, close the game
        if event.type == pygame.QUIT:
            running = False
        # If the user has pressed down on the keyboard, handle the input
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            counter = counter + 1
            
        else:
            pass
    
    window.fill((0, 0, 0))


    if counter < 360:
        e1.components["TextureComponent"].textures[0].angle = counter
        e1.components["TextureComponent"].prepareSurfaces(e1)
        #counter = counter + 1

    print(e1.components["TextureComponent"].textureSurfaceList)
    print(e1.components["TextureComponent"].textures)
    print(counter)
    print("---------------------------")

    RS.render(window, e1)



    pygame.display.update()

pygame.quit()
