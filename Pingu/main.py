from settings import *
from pingu import pingu
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from random import randint, choice 
import sys

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Snowy Pingu Adventure')
        self.clock = pygame.time.Clock()
        self.running = True
        
        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
            
        # gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100 
        
        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 2000)
        self.spawn_positions = []
        
        #setup
        self.load_images()
        self.setup()
    
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'snowball.png')).convert_alpha()
        self.enemy_surf = pygame.image.load(join('images','snowman1.png')).convert_alpha()
          
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:   
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction,(self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
    
    def setup(self):
        map = load_pygame(join('maps', 'Village.tmx'))
          
        for x, y, image in map.get_layer_by_name('Ground').tiles():
           Sprite((x * TILE_SIZE , y*TILE_SIZE), image, self.all_sprites)  
       
        for x, y, image in map.get_layer_by_name('Water').tiles():
           Sprite((x * TILE_SIZE , y*TILE_SIZE), image, self.all_sprites)
           
        for x, y, image in map.get_layer_by_name('RockSlopes_Auto').tiles():
           Sprite((x * TILE_SIZE , y*TILE_SIZE), image, self.all_sprites)
           
        for x, y, image in map.get_layer_by_name('RockSlopes').tiles():
           Sprite((x * TILE_SIZE , y*TILE_SIZE), image, self.all_sprites)
           
        for x, y, image in map.get_layer_by_name('Road').tiles():
           Sprite((x * TILE_SIZE , y*TILE_SIZE), image, self.all_sprites)  
                 
        for obj in map.get_layer_by_name('Object Layer 1'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.pingu = pingu((obj.x,obj.y),  self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.pingu, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))
                
    def bullet_collision(self):
         if self.bullet_sprites:
             for bullet in self.bullet_sprites:
                 collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                 if collision_sprites:
                     for sprite in collision_sprites:
                         sprite.destroy()
                     bullet.kill()    

    def player_collision(self):     
        if pygame.sprite.spritecollide(self.pingu, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def draw_instructions(self):
        instructions = [
            "Use arrow keys or WASD to move.",
            "Press right-click to shoot.",
            "Try not to get caught by snowmans",
            "Good luck!",
            "Press any key to start."
        ]
        white = (255, 255, 255)
        for i, line in enumerate(instructions):
            text_surface = pygame.font.Font(None, 36).render(line, True, white)
            self.display_surface.blit(text_surface, (20, 20 + i * 40))
             
    def run(self):    
        show_instructions = True
        while self.running:
            #dt
            dt = self.clock.tick() / 1000
            
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), self.enemy_surf, (self.all_sprites, self.enemy_sprites), self.pingu, self.collision_sprites)
                if event.type == pygame.KEYDOWN:
                    show_instructions = False
            
            #update
            if not show_instructions:
                self.gun_timer()
                self.input()
                self.all_sprites.update(dt)
                self.bullet_collision()
                self.player_collision()
            
            #draw
            self.display_surface.fill('black')
            if show_instructions:
                self.draw_instructions()
            else:
                self.all_sprites.draw(self.pingu.rect.center)
           
            pygame.display.update()
        pygame.quit()    

if __name__ == '__main__':
    game = Game()
    game.run()