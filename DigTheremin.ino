#include <Button.h>
#include <RunningAverage.h>
#include "MegunoLink.h"
#include "Filter.h"

const int buttonPin = 12;     // the number of the pushbutton pin
const int ledPin =  13;       // led pin output 
const int inputPin = A0;


const int numReadings = 5;
int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int msg=0;
int total = 0;                  // the running total
int average = 0;                // the average
int range=1;

Button button=Button(12,PULLUP);
ExponentialFilter<long> ExpFilter(10, 0);               //create expo filter   

void setup()
{
  Serial.begin(9600);                                     // starts the serial monitor
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }  
  pinMode(ledPin, OUTPUT);                              // initialize the LED pin as an output:
}

void loop()
{
   if(button.uniquePress())                            //button for frequency range        
   {   
    digitalWrite(ledPin, HIGH);                       // turn LED off:
      if(range==3)
       range=1;                                       //range=0 
      else 
       range=range+1;                                //increase range by 1
    } 
    else 
    {
       digitalWrite(ledPin, LOW);  
   }
  
  readings[readIndex] = analogRead(inputPin);            // read from the sensor:
  if(readings[readIndex]>510)
    readings[readIndex]=510;
  else if(readings[readIndex]<50)                         // basic filter to cutoff too low or high volatges
    readings[readIndex]=50;

  ExpFilter.Filter(readings[readIndex]);                  //exponential filter
  int exp= ExpFilter.Current();
  total=total+exp;
  readIndex+=1;     
  if(readIndex==numReadings){                             // take average of 5 readings  
     average=total/numReadings;
     total=0;
     msg=map(average,50,510,10,255);                     //map between 10 to 255
     Serial.println(msg);
     average=0;
     readIndex=0;
    Serial.write(msg);
    Serial.write(range);                                // send it to the computer as ASCII digits
  }
 delay(10); 
}

