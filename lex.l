%{
#include <stdio.h>
#include <conio.h>
#include <iostream>

#define Booleano 300
#define Capturar 302
#define Caso 304
#define Constructor 306
#define Clase 308
#define Continuar 310
#define DECIMAL 312
#define Defecto 314
#define Vacio 316
#define Enumeracion 318
#define ENTERO 320
#define Escribir 322
#define Iniciar 324
#define Asincrono 326
#define Falso 328
#define Fin 330
#define Funcion 332
#define Crear 334
#define Hilo 336
#define Inicio 338
#define Intentar 340
#define Leer 342
#define Lista 344
#define Incrementa 346
#define Decrementa 348
#define Diccionario 350
#define Mientras 352
#define Nulo 354
#define Para 356
#define Principal 358
#define Privado 360
#define Protegido 362
#define Publico 364
#define Retornar 366
#define Romper 368
#define Seleccionar 370
#define Propio 372
#define Sino_si 374
#define Sino 376
#define Si 378
#define TEXTO 380
#define Verdadero 382
#define Identificador 384
#define Entero 386
#define Decimal 388
#define Modulo 390
#define Menor_igual 392
#define Marca_Fin 394
#define Marca_Inicio 396
#define Desigualdad 398
#define Xor 400
#define Not 402
#define Or 404
#define And 406
#define Asignador 408
#define Mayor_igual 410
#define Potencia 412
#define Cadena 414
#define Igualdad 500
using namespace std;
%}

%option noyywrap
%option yylineno

ignora [ |\t|\n|\r]
letra [a-zA-Z]
digito [0-9]
identificador "@"{letra}({letra}|{digito}|[_])*
numero {digito}+ 
real {digito}+\.{digito}+ 
cadena \".*\" 
comentario_linea "//".* 
comentario_bloque "/*"([^*]|\*+[^*/])*\*+"/"

%%

{ignora}+                   {;}

"booleano"                  {return (Booleano);}
"capturar"                  {return (Capturar);}
"caso"                      {return (Caso);}
"constructor"               {return (Constructor);}
"clase"                     {return (Clase);}
"continuar"                 {return (Continuar);}
"decimal"                   {return (DECIMAL);}
"defecto"                   {return (Defecto);}
"vacio"              {return (Vacio);}
"enumeracion"               {return (Enumeracion);}
"entero"                    {return (ENTERO);}
"escribir"                  {return (Escribir);}
"iniciar"            {return (Iniciar);}
"asincrono"                {return (Asincrono);}
"falso"                     {return (Falso);}
"fin"                       {return (Fin);}
"funcion"                   {return (Funcion);}
"crear"                     {return (Crear);}
"hilo"                      {return (Hilo);}
"inicio"                    {return (Inicio);}
"intentar"                  {return (Intentar);}
"leer"                      {return (Leer);}
"lista"                     {return (Lista);}
"mas"                       {return (Incrementa);}
"menos"                     {return (Decrementa);}
"diccionario"               {return (Diccionario);}
"mientras"                  {return (Mientras);}
"nulo"                      {return (Nulo);}
"para"                      {return (Para);}
"principal"                 {return (Principal);}
"privado"                   {return (Privado);}
"protegido"                 {return (Protegido);}
"publico"                   {return (Publico);}
"retornar"                  {return (Retornar);}
"romper"                    {return (Romper);}
"seleccionar"               {return (Seleccionar);}
"self."                     {return (Propio);}
"si"                        {return (Si);}
"sino"                      {return (Sino);}
"sino_si"                   {return (Sino_si);}
"texto"                     {return (TEXTO);}
"verdadero"                 {return (Verdadero);}
"%%"                        {return (Modulo);}
"<="                        {return (Menor_igual);}
"<-"                        {return (Marca_Fin);}
"->"                        {return (Marca_Inicio);}
"<>"                        {return (Desigualdad);}
"^^"                        {return (Xor);}
"~~"                        {return (Or);}
"!!"                        {return (Not);}
"&&"                        {return (And);}
":="                        {return (Asignador);}
">="                        {return (Mayor_igual);}
"**"                        {return (Potencia);}
"*"                         {return ('*');}
"+"                         {return ('+');}
"%"                         {return ('%');}
">"                         {return ('>');}
"<"                         {return ('<');}
"-"                         {return ('-');}
"/"                         {return ('/');}
"("                         {return ('(');}
")"                         {return (')');}
"{"                         {return ('{');}
"}"                         {return ('}');}
"["                         {return ('[');}
"]"                         {return (']');}
";"                         {return (';');}
","                         {return (',');}
"."                         {return ('.');}
":"                         {return (':');}
{numero}                    {return (Entero);}
{real}                      {return (Decimal);}
{cadena}                    {return (Cadena);}
{identificador}             {return (Identificador);}
{comentario_linea}          {;}
{comentario_bloque}         {;}
"=="                      {return(Igualdad);}
.                           {printf(">|%d|%s\n",yylineno,yytext);}


%%

// Arreglo con los nombres de los tokens
const char* nombres_tokens[] = {
    "Desconocido",       
    "Booleano",        
    "Capturar",        
    "Caso",             
    "Constructor",       
    "Clase",             
    "Continuar",         
    "DECIMAL",           
    "Defecto",          
    "Vacio",      
    "Enumeracion",    
    "ENTERO",            
    "Escribir",         
    "Iniciar",    
    "Asincrono",        
    "Falso",             
    "Fin",           
    "Funcion",          
    "Crear",             
    "Hilo",           
    "Inicio",          
    "Intentar",          
    "Leer",            
    "Lista",           
    "Incrementa",    
    "Decrementa",        
    "Diccionario",      
    "Mientras",          
    "Nulo",              
    "Para",            
    "Principal",       
    "Privado",           
    "Protegido",         
    "Publico",           
    "Retornar",          
    "Romper",            
    "Seleccionar",       
    "Propio",               
    "Sino_si",           
    "Sino",              
    "Si",                
    "TEXTO",           
    "Verdadero",         
    "Modulo",            
    "Menor_igual",   
    "Marca_Fin",       
    "Marca_Inicio",        
    "Desigualdad",       
    "Xor",               
    "Not",               
    "No",                
    "And",               
    "Asignador",         
    "Mayor_igual",       
    "Potencia",          
    "Cadena",
    "Igualdad",     
    "*"
    "+"
    "%"
    "<"
    ">"
    "-"
    "/"
    "("
    ")"
    "{"
    "}"
    "["
    "]"
    ";"
    ","
    "."
    ":" 
    
};

// Funcion para obtener el nombre del token
const char* obtener_nombre_token(int token) {
    if (token == 300) {
        return "Booleano";  
    } else if (token == 302) {
        return "Capturar";  
    } else if (token == 304) {
        return "Caso";  
    } else if (token == 306) {
        return "Constructor";  
    } else if (token == 308) {
        return "Clase";  
    } else if (token == 310) {
        return "Continuar";  
    } else if (token == 312) {
        return "DECIMAL"; 
    } else if (token == 314) {
        return "Defecto";  
    } else if (token == 316) {
        return "Vacio";  
    } else if (token == 318) {
        return "Enumeracion";  
    } else if (token == 320) {
        return "ENTERO";  
    } else if (token == 322) {
        return "Escribir"; 
    } else if (token == 324) {
        return "Iniciar"; 
    } else if (token == 326) {
        return "Asincrono";  
    } else if (token == 328) {
        return "Falso";
    } else if (token == 330) {
        return "Fin";  
    } else if (token == 332) {
        return "Funcion"; 
    } else if (token == 334) {
        return "Crear"; 
    } else if (token == 336) {
        return "Hilo";  
    } else if (token == 338) {
        return "Inicio"; 
    } else if (token == 340) {
        return "Intentar"; 
    } else if (token == 342) {
        return "Leer";  
    } else if (token == 344) {
        return "Lista";  
    } else if (token == 346) {
        return "Incrementa"; 
    } else if (token == 348) {
        return "Decrementa";  
    } else if (token == 350) {
        return "Diccionario";  
    } else if (token == 352) {
        return "Mientras";  
    } else if (token == 354) {
        return "Nulo";
    } else if (token == 356) {
        return "Para";  
    } else if (token == 358) {
        return "Principal";  
    } else if (token == 360) {
        return "Privado";  
    } else if (token == 362) {
        return "Protegido";  
    } else if (token == 364) {
        return "Publico";  
    } else if (token == 366) {
        return "Retornar"; 
    } else if (token == 368) {
        return "Romper";  
    } else if (token == 370) {
        return "Seleccionar"; 
    } else if (token == 372) {
        return "Propio";  
    } else if (token == 374) {
        return "Sino_si";  
    } else if (token == 376) {
        return "Sino"; 
    } else if (token == 378) {
        return "Si";  
    } else if (token == 380) {
        return "TEXTO";  
    } else if (token == 382) {
        return "Verdadero";  
    } else if (token == 384) {
        return "Identificador";
    } else if (token == 386) {
        return "Entero";
    } else if (token == 388) {
        return "Decimal";
    } else if (token == 390) {
        return "Modulo";
    } else if (token == 392) {
        return "Menor_igual";  
    } else if (token == 394) {
        return "Marca Fin";  
    } else if (token == 396) {
        return "Marca Inicio";  
    } else if (token == 398) {
        return "Desigualdad";  
    } else if (token == 400) {
        return "Xor";  
    } else if (token == 402) {
        return "Not";  
    } else if (token == 404) {
        return "Or";  
    } else if (token == 406) {
        return "And"; 
    } else if (token == 408) {
        return "Asignador";  
    } else if (token == 410) {
        return "Mayor_igual";  
    } else if (token == 412) {
        return "Potencia";  
    } else if (token == 414) {
        return "Cadena";
    } else if (token == 42) {
        return "Multiplicacion";      
    } else if (token == 43) {
        return "Suma";  
    } else if (token == 37) {
        return "Porcentaje";  
    } else if (token == 60) {
        return "Menor_que";  
    } else if (token == 62) {
        return "Mayor_que";  
    } else if (token == 45) {
        return "Resta"; 
    } else if (token == 47) {
        return "Dividir";  
    } else if (token == 40) {
        return "Parentesis_A"; 
    } else if (token == 41) {
        return "Parentesis_C";  
    } else if (token == 123) {
        return "Llaves_A";  
    } else if (token == 125) {
        return "Llaves_C";  
    } else if (token == 91) {
        return "Corchetes_A";  
    } else if (token == 93) {
        return "Corchetes_C";  
    } else if (token == 59) {
        return "Punto_coma"; 
    } else if (token == 44) {
        return "Coma"; 
    } else if (token == 46) {
        return "Punto";  
    } else if (token == 58) {
        return "Dos_puntos"; 
    } else if (token == 500) {
    return "Igualdad";  
}
    return "Desconocido";
}

int main(int argc, char* argv[]) {
if (argc < 2) {
       cout << "Uso: " << argv[0] << " <nombre_archivo>" << endl;
       return 1;
}

yyin = fopen(argv[1], "rt");

    if (yyin == NULL) {
        cout << "ERROR: Archivo no se encuentra!" << endl;
        return 1;
    } 

    int Token;
    while ((Token = yylex()) > 0) {
        cout << "+|" << Token << "|" << yytext << "|" <<obtener_nombre_token(Token)<<endl;
    }

    fclose(yyin);
    return 0;
}
