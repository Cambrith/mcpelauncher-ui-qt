#include <assert.h>
#include <string.h>
#include <stdio.h>
void translate_args(unsigned long*,int);
int main(void){unsigned long r[7]={0,(unsigned long)"File",123,456,789,12,34};translate_args(r,0);assert(!strcmp((char*)r[1],"Arquivo"));assert(r[2]==123&&r[6]==34);
 r[1]=(unsigned long)"%s";r[2]=(unsigned long)"[OFF] platform compatible (slot 14)";translate_args(r,1);assert(!strcmp((char*)r[2],"[DESATIVADO] Compatível com a plataforma (posição 14)"));
 r[1]=(unsigned long)"SSSE3 support: %s\n";r[2]=(unsigned long)"YES";translate_args(r,1);assert(!strcmp((char*)r[1],"Suporte a SSSE3: %s\n"));assert(!strcmp((char*)r[2],"Sim"));
 r[1]=(unsigned long)"Label";r[2]=(unsigned long)"Path";r[3]=987;translate_args(r,3);assert(!strcmp((char*)r[2],"Caminho"));assert(r[3]==987);
 r[1]=(unsigned long)"%.3f ms/frame (%.1f FPS)";r[2]=321;translate_args(r,1);assert(r[2]==321);
 r[1]=(unsigned long)"VV Patching";translate_args(r,5);r[1]=1;r[2]=44;r[3]=99;translate_args(r,4);assert(!strcmp((char*)r[1],"Aplicar rt0 agora"));assert(r[2]==44&&r[3]==99);
 r[1]=(unsigned long)"[OFF] hardware blocked false (slot 5)";translate_args(r,4);assert(!strcmp((char*)r[1],"[DESATIVADO] Hardware bloqueado: falso (posição 5)"));
 r[1]=(unsigned long)"%s";r[2]=(unsigned long)"RayTracingHardware candidate[1] addr=0xabcd adjust=+2 top=0";translate_args(r,1);assert(!strcmp((char*)r[2],"Recursos de traçado de raios candidato[1] endereço=0xabcd ajuste=+2 topo=0"));
 puts("Translation argument checks passed");}
