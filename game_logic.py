import random
import time
import cv2
from PIL import Image
import os
import numpy as np

class TRex:
    def __init__(self):
        # Dinosaure
        img = Image.open("dinoT.png")  # Ouvrir l'image
        img = img.resize((40, 40))  # Redimensionner l'image
        img.save("resized_dinoT.png")  # Sauvegarder l'image redimensionnée sous un nouveau nom
        self.dino_image = cv2.imread("resized_dinoT.png", cv2.IMREAD_UNCHANGED)
        self.x = 90  # Position du dinosaure
        self.y = 399
        self.is_jumping = False
        self.gravity = -1.6
        self.dino_velocity = 12
        self.speed = 13
    
    def adjust_colors(self, image, background_color):
     #Ajuste les couleurs de l'image en fonction du fond.
     #param image: Image sous forme de tableau NumPy (RGBA).
     #return: Image ajustée sous forme de tableau NumPy.
       
        # Convertir l'image en RGBA si ce n'est pas déjà le cas
        if image.shape[2] == 3:  # Si l'image est en BGR (3 canaux)
           image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        # Créer un masque pour les pixels non transparents
        alpha = image[:, :, 3] != 0                  
        # Ajuster les couleurs en fonction du fond
        if background_color == "black":
            image[alpha, :3] = np.clip(image[alpha, :3] + 100, 0, 255)  # Augmenter la luminosité
            
        return image
    
    
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.dino_velocity = 15  # Vitesse initiale du saut
            
                       
class Obstacles :
    def __init__(self, trex, game):
        self.obstacles = []
        self.trex = trex
        self.game = game
        self.min_gap = 320
        self.resized_images = {
            "small_cactus": self.create_resized_image("CactusT.png", 14, 35),
            "large_cactus": self.create_resized_image("CactusT.png", 20, 50),
            "pteranodon": self.create_resized_image("ptéranodonT.png", 50, 15)
        }
    
        
    def create_obstacle(self):
     if not self.obstacles or self.obstacles[-1]["x"] < 600 - self.min_gap:
        # Toujours définir obstacle_type avant de l'utiliser
        obstacle_type = random.choice(["small", "large", "small_group", "large_group", "hybrid_group", "pteranodon"])

        # Utilisation d'un dictionnaire pour appeler la bonne fonction
        add_obstacle = {
            "small": lambda: self.add_single_obstacle("small_cactus", 400),
            "large": lambda: self.add_single_obstacle("large_cactus", 386),
            "small_group": lambda: self.add_group_obstacles(count=random.randint(2, 3), image_key="small_cactus", y_pos=400, spacing=5),
            "large_group": lambda: self.add_group_obstacles(count=random.randint(2, 3), image_key="large_cactus", y_pos=386, spacing=5),
            "hybrid_group": lambda: self.add_hybrid_group(count=random.randint(2, 3), spacing=6),
            "pteranodon": lambda: self.add_pteranodon(397, 351)
        }

        # Appel de la fonction appropriée
        add_obstacle.get(obstacle_type, lambda: None)()



    def add_single_obstacle(self, image_key, y_pos):
        x_pos = random.randint(600, 800)  # Position aléatoire
        obstacle = {"image": self.resized_images[image_key], "x": x_pos, "y": y_pos}
        self.obstacles.append(obstacle)
    
    def add_group_obstacles(self, count, image_key, y_pos, spacing):
        x_start = random.randint(600, 800)  # Point de départ du groupe
        for i in range(count):
            if i == 0:
                x_pos = x_start  # Premier obstacle
            else:
                previous_obstacle = self.obstacles[-1]
                x_pos = previous_obstacle["x"] + previous_obstacle["image"].shape[1] + spacing
            obstacle = {"image": self.resized_images[image_key], "x": x_pos, "y": y_pos}
            self.obstacles.append(obstacle)


    def add_hybrid_group(self, count, spacing):
     x_start = random.randint(600, 800)  # Point de départ du groupe
     for i in range(count):
        image_key, y_pos = ("small_cactus", 400) if random.choice([True, False]) else ("large_cactus", 386)
        x_pos = x_start if i == 0 else self.obstacles[-1]["x"] + self.obstacles[-1]["image"].shape[1] + spacing
        self.obstacles.append({"image": self.resized_images[image_key], "x": x_pos, "y": y_pos})


    def add_pteranodon(self, y_pos_bas, y_pos_haut):
        x_pos = random.randint(600, 800)
        Y = random.choice([y_pos_bas, y_pos_haut])
        obstacle = {"image": self.resized_images["pteranodon"], "x": x_pos, "y": Y}
        self.obstacles.append(obstacle)

    def create_resized_image(self, pic, width, height):
     return np.array(Image.open(pic).resize((width, height)).convert('RGBA') if Image.open(pic).mode != 'RGBA' else Image.open(pic).resize((width, height)))


class Game:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 600
        self.bg_color, self.window = (255, 255, 255), np.ones((self.screen_height, self.screen_width, 3), dtype=np.uint8) * 255
        self.score, self.previous_score = 0, self.load_highscore()
        # Initialiser last_score_with_color_change à 0
        self.last_score_with_color_change = 0
        # Définir self.trex avant de créer l'objet Obstacles
        self.trex = TRex()
        # Maintenant, tu peux créer l'objet Obstacles
        self.obst = Obstacles(self.trex, self)
        self.start_time, self.last_obstacle_time = time.time(), time.time()
        self.ground_image, self.cloud_image = self.obst.create_resized_image("solT.png", self.screen_width, 50), self.obst.create_resized_image("cloudsT.png", 100, 30)
        self.text_color, self.difficulty_level = (0, 0, 0), 0
        self.background_colors = [(255, 255, 255), (0, 0, 0)]  # Alterner entre blanc et noir
        self.current_background_color, self.background_switch_interval = self.background_colors[0], 100
        self.stars, self.moon_x, self.ground_x = [], self.screen_width - 60, 0
        self.ground_y, self.clouds = self.trex.y + self.trex.dino_image.shape[0] - (self.ground_image.shape[0] // 2), []
        self.generate_clouds()
        

    def load_highscore(self): 
     """Charge le meilleur score depuis un fichier."""
     with open("highscore.txt", "r") as file:
        highscore = int(file.read())
        print(f"High score loaded: {highscore}")
        return highscore


    def save_highscore(self):
     """Sauvegarde le meilleur score dans un fichier."""
     with open("highscore.txt", "w") as file:
        file.write(str(self.previous_score))
        print(f"High score saved: {self.previous_score}")

    def reset_score(self):
        """Réinitialise le jeu en conservant le score précédent."""
        print(f"Current score: {self.score}, Previous score: {self.previous_score}")
        if self.score > self.previous_score:
            self.previous_score = self.score
            print(f"New high score saved: {self.previous_score}")
            self.save_highscore()   
        
        self.score = 0
        self.start_time = time.time()


    def update_score(self):
        """Met à jour le score en fonction du temps écoulé."""
        elapsed_time = time.time() - self.start_time
        self.score = int(elapsed_time * 10)
        
    
    def update_dino(self):
        if self.trex.speed > 10:
            self.trex.gravity = -1.8
        elif self.trex.speed > 6:
            self.trex.gravity = -1.7
        else:
            self.trex.gravity = -1.7
        
        if self.trex.is_jumping:
           self.trex.y -= self.trex.dino_velocity  # Mettre à jour la position verticale
           self.trex.dino_velocity += self.trex.gravity  # Appliquer la gravité
           if self.trex.y >= 399:  # 400 est la position initiale du dinosaure (au sol)
               self.trex.y = 399  # Réinitialiser la position
               self.trex.is_jumping = False  # Arrêter le saut
               
               
    def update_obstacles(self):
        """Met à jour la position des obstacles."""
        obstacles_to_remove = []  # Liste pour stocker les obstacles à supprimer
        for obstacle in self.obst.obstacles:
            obstacle["x"] -= self.trex.speed
            if obstacle["x"] + obstacle["image"].shape[1] < 0:  # Si l'obstacle sort de l'écran, le retirer
                obstacles_to_remove.append(obstacle)
        
        for obstacle in obstacles_to_remove:                # Supprimer les obstacles hors de l'écran
            self.obst.obstacles.remove(obstacle)
            
            
    def update_difficulty(self):
        if self.score % 100 == 0 and self.score != 0:
            self.trex.speed += 0.7
            self.difficulty_level += 1  
            self.update_background()
            cv2.putText(self.window, f"Difficulte : Niveau {self.difficulty_level}", (((self.screen_width) // 2) - 150 , (self.screen_height // 2) - 240 ), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.text_color, 2)
    
    
    def check_collisions(self):
        for obstacle in self.obst.obstacles:
            if (self.trex.x  < obstacle["x"] + obstacle["image"].shape[1]  and
                self.trex.x + self.trex.dino_image.shape[1]  > obstacle["x"] + 1 and
                self.trex.y  < obstacle["y"] + obstacle["image"].shape[0] - 1 and
                self.trex.y + self.trex.dino_image.shape[0] - 1 > obstacle["y"] + 1 ):
                return True
        return False
    

    def update_background(self):
        """Change la couleur du fond en fonction du score."""
        if self.score // 100 != self.last_score_with_color_change // 100 and self.score != 0:
            self.last_score_with_color_change = self.score
            # Alterner entre les deux couleurs
            if self.current_background_color == self.background_colors[0]:
                self.current_background_color = self.background_colors[1]
                
                self.generate_stars()  # Générer des étoiles
                self.moon_x = self.screen_width - 60  # Réinitialiser la position de la lune
            
            else:
                self.current_background_color = self.background_colors[0]
            
            # Appliquer la nouvelle couleur
            self.bg_color = self.current_background_color
            self.adjust_element_colors(self.current_background_color)
            
            
    def adjust_element_colors(self, background_color):
        # Ajuster les couleurs du dinosaure
        self.trex.dino_image = self.trex.adjust_colors(self.trex.dino_image, background_color)
        
        # Ajuster les couleurs des obstacles
        for obstacle in self.obst.obstacles:
            if "image" in obstacle:  # Vérifier si l'obstacle a une image
                obstacle["image"] = self.trex.adjust_colors(obstacle["image"], background_color)
                
        # Ajuster les couleurs du sol
        self.ground_image = self.trex.adjust_colors(self.ground_image, background_color)

        # Ajuster les couleurs des nuages
        self.cloud_image = self.trex.adjust_colors(self.cloud_image, background_color) 
           
        # Ajuster les couleurs des textes
        self.adjust_text_colors(background_color)
        
            
    def adjust_text_colors(self, background_color):
        if  background_color == (0, 0, 0):
            self.text_color = (255, 255, 255)
        else:
            self.text_color = (0, 0, 0)  # Texte noir
    
                   
    def generate_clouds(self):
        """Génère des positions aléatoires pour les nuages avec un espacement minimal."""
        self.clouds = []
        moon_zone = {
        "x_min": self.moon_x - 30,
        "x_max": self.moon_x + 30,
        "y_min": 70,
        "y_max": 110
        }
        for _ in range(3):  # Générer 3 nuages
            # On essaie de placer un nuage en 100 tentatives maximum pour éviter une boucle infinie
            for _ in range(100):  # 100 tentatives max par nuage
                x = random.randint(0, self.screen_width)
                y = random.randint(70, 150)
                if not (any(abs(x - c["x"]) < 200 and abs(y - c["y"]) < 200 for c in self.clouds) or
                    moon_zone["x_min"] <= x <= moon_zone["x_max"] and moon_zone["y_min"] <= y <= moon_zone["y_max"]):
                   self.clouds.append({"x": x, "y": y, "width": self.cloud_image.shape[1], "height": self.cloud_image.shape[0], "speed": self.trex.speed * 0.3 })
                   break

    #===============================#
    # partie sur les details du jeu #
    #===============================#

    def generate_stars(self):
        """Génère des positions aléatoires pour les étoiles."""
        self.stars = []
        for _ in range(30):  # Générer 100 étoiles
            x = random.randint(0, self.screen_width)
            y = random.randint(0, (self.screen_height // 2)-50)  # Étoiles uniquement dans la moitié supérieure
            radius = random.randint(1, 2)  # Taille aléatoire des étoiles
            brightness = random.randint(200, 255)
            self.stars.append((x, y, radius, brightness))

    
    def update_stars(self):
        """Met à jour la luminosité des étoiles pour un effet de scintillement."""
        for i, star in enumerate(self.stars):
            x, y, radius, brightness = star
            # Modifier légèrement la luminosité
            new_brightness = brightness + random.randint(-20, 20)
            # Garder la luminosité dans une plage raisonnable
            new_brightness = max(150, min(255, new_brightness))
            self.stars[i] = (x, y, radius, new_brightness)
    
    
    def draw_moon(self):
        """Dessine la lune en haut à droite de l'écran."""
        moon_radius = 20  # Taille de la lune
        moon_x = int(self.moon_x)  # Position x de la lune
        moon_y = 90  # Position y de la lune

        # Dessiner la lune (cercle blanc)
        cv2.circle(self.window, (moon_x, moon_y), moon_radius, (254, 254, 254), -1)

        # Dessiner un cercle noir pour créer l'effet de croissant
        mask_radius = moon_radius  # Même rayon que la lune
        mask_x = moon_x - 15  # Décaler le cercle masqué vers la gauche
        mask_y = moon_y  # Même position y
        cv2.circle(self.window, (mask_x, mask_y), mask_radius, self.bg_color, -1)  # Couleur du fond pour masquer

        # Ajouter des cratères 
        cv2.circle(self.window, (moon_x - 10, moon_y - 5), 3, (200, 200, 200), -1)  # Petit cratère
        cv2.circle(self.window, (moon_x + 5, moon_y + 10), 4, (200, 200, 200), -1)  # Grand cratère
 
    
    def update_clouds(self):
        """Déplace les nuages et les cailloux vers la gauche."""
        # Déplacer les nuages
        for cloud in self.clouds:
            cloud["x"] -= cloud["speed"]
            if cloud["x"] + cloud["width"] < 0:  # Si le nuage sort de l'écran
                cloud["x"] = self.screen_width  # Réapparaître à droite
                cloud["y"] = random.randint(50, 150)  # Nouvelle position y aléatoire
    
        
    def update_stars_and_moon(self):
     """Déplace les étoiles et la lune lentement vers la gauche en utilisant la vitesse du dinosaure."""
     for i, (x, y, radius, brightness) in enumerate(self.stars):
        x -= self.trex.speed * 0.2
        if x + radius < 0:
            x, y = self.screen_width + radius, random.randint(0, self.screen_height // 2 - 50)
        self.stars[i] = (x, y, radius, brightness)

     if self.current_background_color == (0, 0, 0):  # Mode nuit
        self.moon_x = self.screen_width + 30 if (self.moon_x - self.trex.speed * 0.1) + 30 < 0 else self.moon_x - self.trex.speed * 0.1

    
    def draw_clouds(self):
        """Dessine les nuages avec une image."""
        for cloud in self.clouds:
            adjusted_cloud_image = self.trex.adjust_colors(self.cloud_image, self.bg_color)  # Ajuster les couleurs
            self.window = self.overlay_transparent_image(self.window, adjusted_cloud_image, int(cloud["x"]), int(cloud["y"]))
            

    def draw_ground(self):
        """Dessine le sol en répétant l'image horizontalement."""
        self.ground_y = 406
        x = self.ground_x
        adjusted_ground_image = self.trex.adjust_colors(self.ground_image, self.bg_color)  # Ajuster les couleurs
        while x < self.screen_width:  # Répéter l'image du sol horizontalement
            if x + self.ground_image.shape[1] > 0:  # Si l'image est partiellement visible
                self.window = self.overlay_transparent_image(self.window, adjusted_ground_image, int(x), int(self.ground_y))
            x += self.ground_image.shape[1]  # Passer à la prochaine image du sol
    
    
    def overlay_transparent_image(self, background, overlay, x, y):
        
        
        if x < 0 or y < 0 or x + overlay.shape[1] > background.shape[1] or y + overlay.shape[0] > background.shape[0]:
            return background  # Skip if the overlay is out of bounds
        
        bg_region = background[y:y + overlay.shape[0], x:x + overlay.shape[1]]
        # Extraire le canal alpha (transparence) de l'overlay
        if overlay.shape[2] == 4:  # RGBA
            alpha = overlay[:, :, 3] / 255.0  # Normaliser entre 0 et 1
            alpha_inv = 1.0 - alpha
        else:  # BGR (pas de canal alpha)
            alpha = 1.0  # Pas de transparence
            alpha_inv = 0.0
        # Fusionner les images en tenant compte de la transparence
        for c in range(0, 3):  # Boucler sur les canaux BGR
            bg_region[:, :, c] = (alpha * overlay[:, :, c] + alpha_inv * bg_region[:, :, c])
        
        background[y:y + overlay.shape[0], x:x + overlay.shape[1]] = bg_region
        return background
    
    
    def draw_elements(self):
     """Dessine tous les éléments sur la fenêtre."""
     self.window[:] = self.bg_color
     self.draw_ground()
     self.draw_clouds()

     if self.current_background_color == (0, 0, 0):  # Mode nuit
        self.update_stars()
        for x, y, radius, brightness in self.stars:
            if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                cv2.circle(self.window, (int(x), int(y)), radius, (brightness,) * 3, -1)
        self.draw_moon()

     if self.trex.dino_image is not None:
        try:
            adjusted_dino_image = self.trex.adjust_colors(self.trex.dino_image, self.bg_color)
            if adjusted_dino_image is not None:
                self.window = self.overlay_transparent_image(self.window, adjusted_dino_image, int(self.trex.x), int(self.trex.y))
        except:
            pass

     for obstacle in self.obst.obstacles:
        # Vérification de l'image en tenant compte des tableaux NumPy
        obstacle_image = obstacle.get("image")
        if obstacle_image is not None and isinstance(obstacle_image, np.ndarray) and obstacle_image.size > 0:
            try:
                self.window = self.overlay_transparent_image(self.window, obstacle_image, int(obstacle["x"]), int(obstacle["y"]))
            except:
                pass

    # Afficher le score et autres informations
     cv2.putText(self.window, f"Score: {self.score}", (self.screen_width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.text_color, 1)
     cv2.putText(self.window, f"Best Score: {self.previous_score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.text_color, 1)
     cv2.putText(self.window, f"Difficulte : Niveau {self.difficulty_level}", ((self.screen_width // 2) - 150, (self.screen_height // 2) - 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.text_color, 1)
