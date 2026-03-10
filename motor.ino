/*
* Code d'exemple pour un capteur à ultrasons HC-SR04.
*/
/* Constantes pour les broches */
const byte TRIGGER1_PIN = 12; // Broche TRIGGER1
const byte ECHO1_PIN = 11;    // Broche ECHO1
const byte TRIGGER2_PIN = 13; // Broche TRIGGER2
const byte ECHO2_PIN = 10;    // Broche ECHO2
/* Constantes pour le timeout */
const unsigned long MEASURE_TIMEOUT = 25000; // 25ms = ~8m à 340m/s
/* Vitesse du son dans l'air en mm/us */
const float SOUND_SPEED = 340.0 / 1000;
// Servo moteur //
#include <Servo.h>  // on inclut la bibliothèque pour piloter un servomoteur
Servo servoMotor; //  Créez un objet servo
float i=0;
int n=0;
float m=10.0;
void setup() {
  servoMotor.attach(9); // Indiquez la broche à laquelle le servo est connecté (ici : broche 9)
  /* Initialise le port série */
  Serial.begin(115200);
  /* Initialise les broches */
  pinMode(TRIGGER1_PIN, OUTPUT);
  digitalWrite(TRIGGER1_PIN, LOW); // La broche TRIGGER doit être à LOW au repos
  pinMode(ECHO1_PIN, INPUT);
  pinMode(TRIGGER2_PIN, OUTPUT);
  digitalWrite(TRIGGER2_PIN, LOW); // La broche TRIGGER doit être à LOW au repos
  pinMode(ECHO2_PIN, INPUT);
}

void loop()
{
  if (n!=3)
  {
    for (i=0;i<=180;i=i+m)
    {
    servoMotor.write(i); // Envoyez le servo à la position de 0 degré
    Serial.print("A");
    Serial.println(i);
    /* Capteur ultrason 1:*/
    digitalWrite(TRIGGER1_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER1_PIN, LOW);
    long measure1 = pulseIn(ECHO1_PIN, HIGH, MEASURE_TIMEOUT);
    float distance1_mm = measure1 / 2.0 * SOUND_SPEED;
    delay(50);
    /* Capteur ultrason 2:*/
    digitalWrite(TRIGGER2_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER2_PIN, LOW);
    long measure2 = pulseIn(ECHO2_PIN, HIGH, MEASURE_TIMEOUT);
    float distance2_mm = measure2 / 2.0 * SOUND_SPEED;
    /* Affiche les résultats en mm, cm et m */
    Serial.print("B");
    Serial.println(distance1_mm);
    Serial.print("C");
    Serial.println(distance2_mm);
    delay(1000);
    }
    m=m/2.0;
    n+=1;
  }
  else
  {
    servoMotor.write(0);
  } 
}