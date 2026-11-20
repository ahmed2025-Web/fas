from hand_control import HandControl
from game_logic import Game
import time
import simpleaudio as sa
import turtle

def main():
    # Initialisation
    hand_control = HandControl()
    game = Game()
    last_score = 0

    sound_played = False  

    try:
        while True:
            # Obtenir la position de la main
            hand_y, frame = hand_control.get_hand_position()

            # Vérifier si le dinosaure est en train de sauter
            if game.trex.is_jumping:
                if not sound_played:
                    wave_obj = sa.WaveObject.from_wave_file("sonsauter.wav")
                    wave_obj.play()
                    sound_played = True  

            if hand_y is not None and hand_y < 0.5:
                if not game.trex.is_jumping:  # Sauter seulement si le dino n'est pas déjà en train de sauter
                    game.trex.jump()
                    if not sound_played:
                        wave_obj = sa.WaveObject.from_wave_file("sonsauter.wav")
                        wave_obj.play()
                        sound_played = True  
                    print("Dino started jumping") 

            if not game.trex.is_jumping and sound_played:
                sound_played = False  

            game.update_obstacles()
            game.update_dino()
            game.update_score()
            game.update_difficulty()
            game.afficher_score()
            game.show_previous_score()
            

            if game.check_collisions():
                wave_obj = sa.WaveObject.from_wave_file("sonmort.wav")
                wave_obj.play()
                print(f"Game Over! Score final : {game.score}")

                # Affichage du message GAME OVER avec turtle
                game_over_display = turtle.Turtle()
                game_over_display.hideturtle()
                game_over_display.penup()
                game_over_display.goto(0, 0)
                game_over_display.write(f"GAME OVER\nScore final: {game.score}", align="center", font=("Arial", 20, "normal"))

                # Afficher une instruction pour quitter
                quit_display = turtle.Turtle()
                quit_display.hideturtle()
                quit_display.penup()
                quit_display.goto(0, -30)
                quit_display.write("Appuyez sur 'q' pour quitter.", align="center", font=("Arial", 16, "normal"))

                # Attendre que l'utilisateur appuie sur 'q' pour quitter
                game.screen.listen()
                game.screen.onkey(game.screen.bye, "q")  # Fermer l'écran avec 'q'
                game.screen.mainloop()  # Bloque l'exécution ici jusqu'à ce que l'utilisateur appuie sur 'q'

                game.reset_score()
                break

            if time.time() - game.last_obstacle_time > 1.5:
                game.obst.create_obstacle()
                game.last_obstacle_time = time.time()

            if game.score // 100 > last_score // 100:
                last_score = game.score
                wave_obj = sa.WaveObject.from_wave_file("son100.wav")
                wave_obj.play()

            game.screen.update()

    finally:
        # Cette partie est ajoutée pour s'assurer que l'écran est bien fermé
        hand_control.release()  # Libère la caméra

if __name__ == "__main__":
    main()
 