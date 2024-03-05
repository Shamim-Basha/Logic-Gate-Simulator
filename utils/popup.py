import pygame
from utils.colors import COLORS

class Popup:
    def __init__(self,x,y,screen,items) -> None:
        self.x = x
        self.y = y
        self.items = self.create_items(items)
        self.width = 200
        self.height = 20 * (len(items)) 
        self.screen = screen
        self.focused = -1
        self.font = pygame.font.SysFont("arial",15)
    
    def create_items(self,items):
        tmp = []
        for idx,(item,fun) in enumerate(items) :
            tmp.append(PopupItem(self.x,self.y+idx*20,item,fun))
        return tmp
    
    def get_index(self):
        x,y = pygame.mouse.get_pos()
        if (self.x<=x<=self.x+self.width and self.y<=y<=self.y+self.height):
            idx = (y-self.y)//20
            return idx
        return -1
    
    def draw(self):
        pygame.draw.rect(self.screen,COLORS["WHITE"],(self.x,self.y,self.width,self.height))
        for idx,item in enumerate(self.items):
            if idx == self.focused:
                pygame.draw.rect(self.screen,COLORS["FOCUSED"],(item.x,item.y,self.width,20))
            text = self.font.render(item.title,1,COLORS["BLACK"])
            self.screen.blit(text,(item.x+10,item.y+2))
        
    def move(self,x,y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
    
    def mouse_hovered(self):
        x,y = pygame.mouse.get_pos()
        return x>self.x and x<self.x+self.width and y>self.y and y<self.y+self.height

    def mouse_in_bound(self,x,y,obj):
        return (x>obj.width/2 and x<self.screen.get_width()-(obj.width/2) and y>obj.height/2+50 and y<self.screen.get_height()-(obj.height/2))
    
    def event_handler(self,event,selected_menu,to_remove,sub_popup):
        x,y = pygame.mouse.get_pos()
        l,_,r = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            idx = self.get_index()
            if l and idx!= -1:
                to_remove = self.items[idx].function()
                if type(to_remove) == Popup:
                    sub_popup = to_remove
                    to_remove = None
            
            if l and not self.mouse_hovered():
                selected_menu = None
              
        if event.type == pygame.MOUSEBUTTONUP:
            if l and not self.mouse_hovered():
                selected_menu = None
        
        if event.type == pygame.MOUSEMOTION:
            self.focused = self.get_index()
                
        return selected_menu,to_remove,sub_popup
    
class PopupItem:
    def __init__(self,x,y,title,function) -> None:
        self.x = x
        self.y = y
        self.title = title
        self.function = function
        