import pygame
from utils.colors import COLORS

class Menu:
    def __init__(self,screen,items=[]) -> None:
        self.items = items
        self.screen = screen
        self.width = 50
        self.height = 25
     
    def add_child(self,title,img=""):
        self.items.append(MenuItem(title,img))
    
    def draw(self):
        pygame.draw.rect(self.screen,COLORS["GREY"],(0,0,self.screen.get_width(),self.height))
        for idx,item in enumerate(self.items):
            self.screen.blit(pygame.transform.smoothscale(item.image,(self.width,self.height)),(idx*self.width+10,10))
            
    def event_handler(self,event,selected,item):
        x,y = pygame.mouse.get_pos()
        idx = (x-10)//self.width
        l,_,r = pygame.mouse.get_pressed()
        if y<self.height:
            if event.type == pygame.MOUSEBUTTONDOWN and l:
                selected = self.items[idx] if idx<len(self.items) else None
            if event.type == pygame.MOUSEMOTION:
                item = self.items[idx] if idx<len(self.items) else None
        else:
            item =  None
        return selected,item
            
            

class MenuItem:
    def __init__(self,title,image="") -> None:
        self.title = title
        self.image = image
        self.font = pygame.font.SysFont("arial",12,0)
        
    def draw(self,screen):
        x,y = pygame.mouse.get_pos()
        text = self.font.render(self.title,1,COLORS["BLACK"],COLORS["WHITE"])
        pygame.draw.rect(screen,COLORS["WHITE"],(x+10,y,text.get_width()+10,text.get_height()))
        screen.blit(text,(x+15,y))