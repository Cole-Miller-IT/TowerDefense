try:
    import sys
    import pygame
    import math
    from pygame.math import Vector2
    from pygame.locals import *

    #My modules
    from entitycomponent import *
    
except ImportError as er:
    print("Error importing modules")
    print(er)
    sys.exit(2)

#Systems use an Entity's components and apply logic to change the gamestate
class System():
    def __init__(self):
        pass

    def run(self):
        pass

class MovementSystem(System):
    def __init__(self, EM, gamestate):
        self.gs = gamestate

    #Moves an entity's position and texture if applicable
    def move(self, entity):
        if entity.components.get("MoveComponent") and entity.components.get("PositionComponent"):
            moveVector = entity.components["MoveComponent"].move
            posX = entity.components["PositionComponent"].x
            posY = entity.components["PositionComponent"].y
            newPos = Vector2((posX + moveVector.x),(posY + moveVector.y))

            #Check if the entity would go outside the world bounds
            if newPos.x < 0 or newPos.x > self.gs.worldSize.x \
                or newPos.y < 0 or newPos.y > self.gs.worldSize.y:
                return

            #Check if the entity collides with another unit
            #if unit collids with another unit:
            #
            #collision

            #Check if the entity collides with a wall

            #If the newPos doesn't conflict with anything update position
            entity.components["PositionComponent"].x = newPos.x
            entity.components["PositionComponent"].y = newPos.y
            
            if entity.components["TextureComponent"]:
                self.moveTextureObjects(entity)
                
        else:
            print("The entity is misssing one or more components for this function, move()")
    
    #Updates an entity's textureobjects to its current position
    def moveTextureObjects(self, entity):
        for textureObj in entity.components["TextureComponent"].textureObjects:
            textureObj.Rect.center = (entity.components["PositionComponent"].x, entity.components["PositionComponent"].y)
        
    def run(self):
        pass

    def debug(self):
        for entity in self.entities:
            if entity.componets.get("MoveComponent"):
                print("MoveComponent Initialized")

class TextureSystem(System):
    def __init__(self, EM, gamestate):
        self.EM = EM
        self.gs = gamestate
        self.updateList = []    #List used to determine which entity's textures should be updated each game loop
                              
    #Update the surface and Rect of a single TextureObject
    def updateTextureObj(self, entity, textureObj, init=False):
        #Check if the entity has the correct components
        if not entity.components["SizeComponent"]:
            print("Entity missing SizeComponent, Entity ID: "  + str(entity.ID))
            return
        elif not entity.components["PositionComponent"]:
            print("Entity missing PositionComponent, Entity ID: "  + str(entity.ID))
            return
        elif not entity.components["TextureComponent"]:
            print("Entity missing TextureComponent, Entity ID: "  + str(entity.ID))
            return
        
        width = entity.components["SizeComponent"].width
        height = entity.components["SizeComponent"].height
        posX = entity.components["PositionComponent"].x
        posY = entity.components["PositionComponent"].y    
        
        #If the textureObj has not yet been initalized, initalize it
        if init:
            #This Rect holds the values to choose the correct texture from the spritesheet
            #print(textureObj.name)
            #print(textureObj.origin)
            textureObj.originRect = pygame.Rect(textureObj.origin.x, textureObj.origin.y, width, height) 
            textureObj.surface = pygame.Surface((width, height), pygame.SRCALPHA)

            #Blits the spritesheet onto the Surface at point (0,0). originRect controls what part
            # of the spritesheet is choosen to blit to the surface
            textureObj.surface.blit(entity.components["TextureComponent"].spritesheet, (0, 0), textureObj.originRect)  
        
        #Create a Rect() that holds the current texture's position
        textureObj.Rect = pygame.Rect(0, 0, width, height)
        textureObj.Rect.center = (posX, posY)
            
        #Check if the texture should be rotated
        if textureObj.angle != 0:
            #Create a copy of the surface
            originalTextureSurface = textureObj.surface.copy()
            
            #Rotate surface
            textureObj.surface, textureObj.Rect = self.rotateSurface(
                originalTextureSurface, textureObj.angle, textureObj.Rect)
                
    #
    def rotateSurface(self, surface, angle, rect):
        #Rotate a surface by angle in degrees
        rotated_image = pygame.transform.rotate(surface, angle)

        #Compute the new Rect by setting it's center to the center of the pre-rotated surface's
        new_rect = rotated_image.get_rect(center=rect.center)

        return rotated_image, new_rect
        
    def run(self):
        pass
        
    def debug(self):
        for entity in self.entities:
            if entity.components.get("RenderComponent"):
                print("TextureComponent Initialized")
        
class RenderSystem(System):
    def __init__(self, EM, gamestate):
        self.EM = EM
        self.gs = gamestate
        self.window = gamestate.window
        self.layers = []

    #Draw the entity on the screen
    def renderEntity(self, entity):
        for textureObj in entity.components["TextureComponent"].textureObjects:
            #Draw tile surface to the window surface
            if textureObj.surface is not None and textureObj.Rect is not None:
                self.window.blit(textureObj.surface, textureObj.Rect)
            else:
                print("renderEntity() texture or surface is not given. ID: " + str(entity.ID))

    #Render a layer, such as all the ground or units entities
    def renderLayer(self, layer):
        for entity in layer:
            self.renderEntity(entity)

    #Creates a 2D list that contains entities
    def create2DLayer(self, positionList, spritesheet):
        layer = []
        for y in range(int(self.gs.worldSize.y)):
            for x in range(int(self.gs.worldSize.x)):
                originPoint = positionList[y][x]
                #The position is going to be the tile coordinates eg. (0,0) * how big the cell is + an offset to center it
                posX = x * self.gs.cellSize.x + (self.gs.cellSize.x / 2)
                posY = y * self.gs.cellSize.y + (self.gs.cellSize.y / 2)
                if originPoint is not None:
                   layer.append(Entity(self.EM, [PositionComponent(posX, posY),
                                                 SizeComponent(self.gs.cellSize.x, self.gs.cellSize.y), TextureComponent(spritesheet, {"base": Vector2(originPoint.y, originPoint.x)}), RenderComponent()]))
        return layer
    
    def run(self):
        pass

    def debug(self):
        for entity in self.entities:
            if entity.components.get("RenderComponent"):
                print("RenderComponent Initialized")


class TargetSystem(System):
    def __init__(self, EM):
        pass

    def run(self, entity):
        pass

    #Computes the angle (in degrees) based on where the targeted point is on the 2D plane
    def getTargetAngle(self, entity):
        if not entity.components.get("TargetComponent"):
            print("TargetComponent not found. getTargetAngle()")
            return
        if not entity.components.get("PositionComponent"):
            print("PositionComponent not found. getTargetAngle()")
            return
            
        entityX = entity.components["PositionComponent"].x
        entityY = entity.components["PositionComponent"].y
        targetX = int(entity.components["TargetComponent"].target.x)
        targetY = int(entity.components["TargetComponent"].target.y)

        #Computes the angle in radians based on the unit's position and where it's looking
        theta = math.atan2(targetY - entityY, targetX - entityX)
        angle = math.degrees(theta)  # Convert to degrees

        return angle          
    
    #Targets a position on the screen using the Entity's position and updates the turret's texture angle
    def turretTarget(self, entity, target):
        if not entity.components.get("TargetComponent"):
            print("TargetComponent not found. turretTarget()")
            return
            
        entity.components["TargetComponent"].targetedPoint = target
        angle = self.getTargetAngle(entity)
        
        #Find the turret textureObject and set the angle
        for textObj in entity.components["TextureComponent"].textureObjects:
            if textObj.name == "turret":
                textObj.angle = angle
                return True
            else:
                print("turret textureObj not found.")
        
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
            if entity.components.get("ShootComponent"):
                print("Shooting Initialized")
