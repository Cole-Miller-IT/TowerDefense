class Event():
    def __init__(self):
        self.observers = []
        
    def registerObserver(self, observer):
        self.observers.append(observer)
        
    def unregisterObserver(self, observer):
        self.observers.remove(observer)
        
    def notifyObservers(self, message):
        for observer in self.observers:
            observer.change(message)
 
 
class Observer():
    def __init__(self, event):
        event.registerObserver(self)
        
    def change(self, message):
        print(message)
        
class TextureObserver(Observer):
    def __init__(self, event):
        super().__init__(self, event)
    
    def updateList(self):
        pass
        
    def change(self, message):
        print(message)
        #
        if message == "update":
            pass