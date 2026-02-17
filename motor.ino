/*
 * Code d'exemple pour un capteur à ultrasons HC-SR04.
 */
 
/* Constantes pour les broches */
const byte TRIGGER_PIN = 12; // Broche TRIGGER
const byte ECHO_PIN = 11;    // Broche ECHO
 
/* Constantes pour le timeout */
const unsigned long MEASURE_TIMEOUT = 25000; // 25ms = ~8m à 340m/s
 
/* Vitesse du son dans l'air en mm/us */
const float SOUND_SPEED = 340.0 / 1000;
 
// Servo moteur //
#include <Servo.h>  // on inclut la bibliothèque pour piloter un servomoteur
 
Servo servoMotor; //  Créez un objet servo
int i=0;
void setup() {
  servoMotor.attach(9); // Indiquez la broche à laquelle le servo est connecté (ici : broche 9)
     
  /* Initialise le port série */
  Serial.begin(115200);
   
  /* Initialise les broches */
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, LOW); // La broche TRIGGER doit être à LOW au repos
  pinMode(ECHO_PIN, INPUT);
}
 
 
void loop()
{
  for (i=0;i<=180;i=i+10)
  {
    servoMotor.write(i); // Envoyez le servo à la position de 0 degré
      /* 1. Lance une mesure de distance en envoyant une impulsion HIGH de 10µs sur la broche TRIGGER */
    digitalWrite(TRIGGER_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_PIN, LOW);
   
    /* 2. Mesure le temps entre l'envoi de l'impulsion ultrasonique et son écho (si il existe) */
    long measure = pulseIn(ECHO_PIN, HIGH, MEASURE_TIMEOUT);
   
    /* 3. Calcul la distance à partir du temps mesuré */
    float distance_mm = measure / 2.0 * SOUND_SPEED;
   
    /* Affiche les résultats en mm, cm et m */
    Serial.print(i);
    Serial.print(",");
    Serial.println(distance_mm);
 
    delay(1000);
  }
 
}