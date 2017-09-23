#include <Adafruit_NeoPixel.h>
#define PIN 6

struct Color{
  byte red;
  byte blue;
  byte green;
} legalMove, illegalMove, engineMove, check;

struct Square{
  Color color;
  bool on;
} isquare[64];

int moveAnimation[28]={0,1,2,3,4,5,6,7,8,23,24,39,40,55,56,57,58,59,60,61,62,63,48,47,32,31,16,15};

Adafruit_NeoPixel strip = Adafruit_NeoPixel(64, PIN, NEO_GRB + NEO_KHZ800);
String current_board_state = "";
char pi;
String state = "";
String temp = "";

void setup(){
  strip.begin();
  strip.show();
  for (uint16_t i = 0; i<64;i++)
  {
    isquare[i].color.red = random(0,255);
    isquare[i].color.blue = random(0,255);
    isquare[i].color.green = random(0,255);
    isquare[i].on = false;
  }
  legalMove.red = 0;
  legalMove.green = 255;
  legalMove.blue = 0;
  
  engineMove.red = 0;
  engineMove.blue = 255;
  engineMove.green = 0;
  
  check.red = 255;
  check.green = 255;
  check.blue = 51;
  
  illegalMove.red = 255;
  illegalMove.green = 0;
  illegalMove.blue = 0;
  Serial.begin(9600);
}

void loop() {
  int l = 0;
  if (Serial.available()){
    int i=1;
    current_board_state = "";
    state = "";
    while(Serial.available()>0){
      
        pi=Serial.read();
        if (pi =='$'|| pi=='v' || pi=='i' || pi=='@'|| pi=='c' || pi =='C'){
          current_board_state = (String)pi;
          break;
        }
        delay(2.5);
        current_board_state+=pi;
      }
     l=1;
     state = current_board_state;  
  }
  if(l==1){
    //Serial.println(state);
    if(state[0]=='$'){
      opening();
      //while(Serial.available() <=0){
      //Serial.println('R');
      //delay(30);
      //}
      //resetPixels();
      //boardDark();
      moveVerified(legalMove,50);
      Serial.println('R');
    }
    if (state[0]=='v'){
      //Serial.println(state);
      moveVerified(legalMove,25);
      Serial.println('R');
    }
    else if (state[0]=='i'){
      moveVerified(illegalMove,25);
      Serial.println('R');
    }
    else if (state[0]=='@'){
      moveVerified(engineMove,25);
      Serial.println('R');
    }
    else if (state[0]=='c'){
      moveVerified(check,30);
      Serial.println('R');
    }
    else if (state[0]=='C'){
        opening();
        closing();
        Serial.println('R');
    }
    else{
      //if (state.length() <64){Serial.println(state);}
      if (state.length()>64){
        for (int i = 0;i<64;i++)
          {
            temp += state[i+64];
          }
        //Serial.println(temp);
        state = "";
        state = temp;
        temp = "";
        }
       //else if(state.length()==63){
       //(state+='r');
     //}
        //Serial.println(state);
    
      for(int i = 0; i<strip.numPixels(); i++)
      {
        //White Team
        if (state[i]=='P'){strip.setPixelColor(i,strip.Color(0,0,255));}
        else if (state[i]=='R'){strip.setPixelColor(i,strip.Color(100,0,255));}
        else if (state[i]=='N'){strip.setPixelColor(i,strip.Color(100,10,255));}
        else if (state[i]=='B'){strip.setPixelColor(i,strip.Color(10,90,255));}
        else if (state[i]=='Q'){strip.setPixelColor(i,strip.Color(13,13,255));}
        else if (state[i]=='K'){strip.setPixelColor(i,strip.Color(200,5,255));}
      
        //Black Team
        else if (state[i]=='p'){strip.setPixelColor(i,strip.Color(0,255,0));}
        else if (state[i]=='r'){strip.setPixelColor(i,strip.Color(100,255,0));}
        else if (state[i]=='n'){strip.setPixelColor(i,strip.Color(100,255,10));}
        else if (state[i]=='b'){strip.setPixelColor(i,strip.Color(10,255,50));}
        else if (state[i]=='q'){strip.setPixelColor(i,strip.Color(13,255,13));}
        else if (state[i]=='k'){strip.setPixelColor(i,strip.Color(200,255,5));}
      
        else if (state[i]=='3'){strip.setPixelColor(i,strip.Color(255,255,255));}
        else if (state[i]=='0'){strip.setPixelColor(i,strip.Color(0,0,0));}
        else if (state[i]=='A'){strip.setPixelColor(i,strip.Color(225,0,0));}
        else if (state[i]=='E'){strip.setPixelColor(i,strip.Color(252,110,39));}
      }
      strip.show();  
    }
  }
}

void boardDark(){
  for (int i=0;i<strip.numPixels();i++){
    strip.setPixelColor(i,strip.Color(0,0,0));
  }
  strip.show();
}

void resetPixels(){
  for (int i = 0; i<64;i++){
    isquare[i].on = false;
  }
}

void opening(){
  for (int i = 0; i < strip.numPixels();i++)
  {
    bool searching = true;
    int randnum = random(0,64);
    while (searching)
    {
    if (isquare[randnum].on == false){
        isquare[randnum].on = true;
        searching = false;
        strip.setPixelColor(randnum,strip.Color(isquare[randnum].color.red,isquare[randnum].color.blue,isquare[randnum].color.green));
    }
    else
    {
      randnum++;
      if(randnum>63){randnum=0;}
    } 
    }
    delay(random(0,150));
    strip.show();
  }
}  

void closing(){
  for (int i = 0; i< strip.numPixels();i++)
  {
    bool searching = true;
    int randnum = random(0,64);
    while (searching)
    {
      if (isquare[randnum].on == true){
        isquare[randnum].on = false;
        searching = false;
        strip.setPixelColor(randnum, strip.Color(0,0,0));
      }
      else{
         randnum++;
        if (randnum>63){randnum = 0;} 
      }
      
    }
    delay(random(0,150));
    strip.show();
  }
}

  
void moveVerified(struct Color& color, int wait){
  for (int i = 0;i<28;i++){
    strip.setPixelColor(moveAnimation[i],strip.Color(color.red,color.green,color.blue));
    if (i>0){strip.setPixelColor(moveAnimation[i-1],strip.Color(color.red,color.green,color.blue+30));}
    if (i>1){strip.setPixelColor(moveAnimation[i-2],strip.Color(color.red,color.green,color.blue+50));}
    if (i>2){strip.setPixelColor(moveAnimation[i-3],strip.Color(color.red,color.green,color.blue+100));}
    if (i>3){strip.setPixelColor(moveAnimation[i-4],strip.Color(color.red,color.green,color.blue+150));}
    if (i==0){
      strip.setPixelColor(moveAnimation[24],strip.Color(color.red,color.green,color.blue+150));
      strip.setPixelColor(moveAnimation[25],strip.Color(color.red,color.green,color.blue+100));
      strip.setPixelColor(moveAnimation[26],strip.Color(color.red,color.green,color.blue+50));
      strip.setPixelColor(moveAnimation[27],strip.Color(color.red,color.green,color.blue+30));
    }
    if (i==1){
      strip.setPixelColor(moveAnimation[24],strip.Color(0,0,0));
      strip.setPixelColor(moveAnimation[25],strip.Color(color.red,color.green,color.blue+150));
      strip.setPixelColor(moveAnimation[26],strip.Color(color.red,color.green,color.blue+100));
      strip.setPixelColor(moveAnimation[27],strip.Color(color.red,color.green,color.blue+500));
    }
    if (i==2){
      strip.setPixelColor(moveAnimation[25],strip.Color(0,0,0));
      strip.setPixelColor(moveAnimation[26],strip.Color(color.red,color.green,color.blue+150));
      strip.setPixelColor(moveAnimation[27],strip.Color(color.red,color.green,color.blue+100));
    }
    if (i==3){
    strip.setPixelColor(moveAnimation[26],strip.Color(0,0,0));
    strip.setPixelColor(moveAnimation[27],strip.Color(color.red,color.green,color.blue+100));
    }
    if (i==4){strip.setPixelColor(moveAnimation[27],strip.Color(0,0,0));}
    
    strip.show();
    delay(wait);
    strip.setPixelColor(moveAnimation[i],strip.Color(0,0,0));
    if (i>0){strip.setPixelColor(moveAnimation[i-1],strip.Color(0,0,0));}
    if (i>1){strip.setPixelColor(moveAnimation[i-2],strip.Color(0,0,0));}
    if (i>2){strip.setPixelColor(moveAnimation[i-3],strip.Color(0,0,0));}
    if (i>3){strip.setPixelColor(moveAnimation[i-4],strip.Color(0,0,0));}
    strip.show();
  }
}

