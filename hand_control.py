import cv2
import mediapipe as mp

class HandControl:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=detection_confidence, 
            min_tracking_confidence=tracking_confidence
        )
        self.cap = cv2.VideoCapture(0)
    
    def get_hand_position(self):
        """Renvoie la position verticale de la main ou None si aucune main détectée."""
        ret, frame = self.cap.read()
        if not ret:
            return None, frame

        frame = cv2.flip(frame, 1)  # Miroir pour correspondre aux mouvements
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                y = hand_landmarks.landmark[9].y  # Position verticale (Landmark 9)
                return y, frame

        return None, frame

    def release(self):
        """Libère la caméra."""
        self.cap.release()
        cv2.destroyAllWindows()
