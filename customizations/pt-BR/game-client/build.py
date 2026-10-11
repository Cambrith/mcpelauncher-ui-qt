from pathlib import Path
import json,re,struct,subprocess,hashlib,os
W=Path(__file__).parent
source=Path('/var/lib/flatpak/app/io.mrarm.mcpelauncher/current/active/files/bin/mcpelauncher-client')
assert hashlib.sha256(source.read_bytes()).hexdigest() == '448af80b3f785c50336e93967b58dbf55c05c6958518aa20dbf09724c5a8dc5a', 'Unsupported client version'
translations={
'File':'Arquivo','Mods':'Modificações','View':'Exibir','Video':'Vídeo','Help':'Ajuda','Hide Menubar':'Ocultar barra de menus','Use Alt to Focus Menubar':'Usar Alt para selecionar a barra de menus','Close':'Fechar',
'Enable Keyboard AutoFocus Patches for 1.20.60+':'Ativar correções de foco automático do teclado para 1.20.60+',
'Enable Keyboard AutoFocus Paste Patches for 1.20.60+':'Ativar correções para colar com foco automático para 1.20.60+',
'Enable Sprint strafe patch for Intel CPUs (requires restart)':'Ativar correção de corrida lateral em CPUs Intel (exige reiniciar)',
'Show FPS-Hud':'Exibir contador de FPS','None':'Não exibir','Always':'Sempre','Ingame':'Durante o jogo','Show Keystroke-Mouse-Hud':'Exibir teclas e cliques do mouse','UI Scale':'Escala da interface','Move huds':'Mover indicadores',
'Use VSync':'Usar sincronização vertical (VSync)','Toggle Fullscreen':'Alternar tela cheia','Default':'Padrão','About':'Sobre','Hide Menubar until exit?':'Ocultar barra de menus até sair?',
'After doing this you cannot access the functionality provided by the menubar until you manually change/delete the settings file':'Depois disso, as funções da barra de menus ficarão indisponíveis até você alterar ou excluir manualmente o arquivo de configurações.',
'After doing this you cannot access the functionality provided by the menubar until you restart Minecraft':'Depois disso, as funções da barra de menus ficarão indisponíveis até você reiniciar o Minecraft.',
'Remember my Decision Forever (a really long time)':'Lembrar esta decisão permanentemente','OK':'Confirmar','Cancel':'Cancelar','OS: %s\n':'Sistema operacional: %s\n','Arch: %s\n':'Arquitetura: %s\n','CPU: %s %s\n':'Processador: %s %s\n','SSSE3 support: %s\n':'Suporte a SSSE3: %s\n','YES':'Sim','NO':'Não','Unknown':'Desconhecido',
'GL Vendor: %s\n':'Fabricante OpenGL: %s\n','GL Renderer: %s\n':'Renderizador OpenGL: %s\n','GL Version: %s\n':'Versão do OpenGL: %s\n','mcpelauncher-client %s / manifest %s\n':'mcpelauncher-client %s / compilação %s\n',
'filepicker':'Selecionar arquivo','Path':'Caminho','Open':'Abrir','xxxx ms/frame (xxxx.x FPS)':'xxxx ms/quadro (xxxx.x FPS)','xxxx ms/frame (xxxx FPS)':'xxxx ms/quadro (xxxx FPS)','Show Demo':'Exibir demonstração','%.3f ms/frame (%.1f FPS)':'%.3f ms/quadro (%.1f FPS)','LMB':'BEM','RMB':'BDM',
'VV Patching':'Ajustes VV','Apply rt0 now':'Aplicar rt0 agora','Apply rt0 at startup':'Aplicar rt0 ao iniciar','Open Window':'Abrir painel','RayTracingOptions':'Opções de traçado de raios','RayTracingHardware':'Recursos de traçado de raios',
'Window refreshes immediately after toggles.':'O painel é atualizado imediatamente após mudar uma opção.',
'Whole vtable group':'Todo o grupo de tabelas virtuais','force disable vibrant visuals':'Forçar desativação dos visuais vibrantes','vibrant visuals allowed':'Permitir visuais vibrantes','slot21 force hook':'Interceptação forçada da posição 21','deferred performance':'Desempenho com renderização diferida','can switch graphics mode':'Permitir alternar o modo gráfico','slot10 deep hook':'Interceptação profunda da posição 10','platform compatible':'Compatível com a plataforma','hardware enabled':'Hardware ativado','graphics mode enum':'Valor do modo gráfico','slot21 deep hook':'Interceptação profunda da posição 21','slot22 state patch':'Correção de estado da posição 22',
'hardware blocked false':'Hardware bloqueado: falso','Enabled':'Ativado','Disabled':'Desativado','enabled':'ativado','disabled':'desativado','true':'verdadeiro','false':'falso',
}
# Ordered replacements apply only to visible strings supplied to GUI widgets.
replacements={'[ON] ':'[ATIVADO] ','[OFF] ':'[DESATIVADO] ','rt0 startup is ':'rt0 ao iniciar está ','RayTracingOptions':'Opções de traçado de raios','RayTracingHardwareOptions':'Recursos de traçado de raios','RayTracingHardware':'Recursos de traçado de raios','hardware blocked false':'Hardware bloqueado: falso',' candidate[':' candidato[',' PRIMARY':' PRINCIPAL',' SECONDARY':' SECUNDÁRIO',' addr=':' endereço=',' adjust=+':' ajuste=+',' top=':' topo=',' (slot ':' (posição ','slot':'posição ','Whole vtable group':'Todo o grupo de tabelas virtuais','Apply rt0 at startup':'Aplicar rt0 ao iniciar','platform compatible':'Compatível com a plataforma','deferred performance':'Desempenho com renderização diferida','vibrant visuals allowed':'Permitir visuais vibrantes','can switch graphics mode':'Permitir alternar o modo gráfico','force disable vibrant visuals':'Forçar desativação dos visuais vibrantes','hardware enabled':'Hardware ativado','graphics mode enum':'Valor do modo gráfico','deep hook':'interceptação profunda','force hook':'interceptação forçada','state patch':'correção de estado','enabled':'ativado','disabled':'desativado'}
(W/'translations.json').write_text(json.dumps(translations,ensure_ascii=False,indent=2)+'\n')
def table(d):return ''.join(json.dumps(k+'\0'+v+'\0',ensure_ascii=False) for k,v in d.items())+'"\\0"'
c='''typedef unsigned long U;
static const char exact[] = TABLE;
static const char parts[] = PARTS;
static char buffers[64][2048]; static unsigned cursor; static unsigned vv_window, vv_button;
static unsigned length(const char*s){unsigned n=0;while(s[n])n++;return n;}
static int same(const char*a,const char*b){while(*a&&*a==*b){a++;b++;}return *a==*b;}
static int starts(const char*a,const char*b){while(*b){if(*a++!=*b++)return 0;}return 1;}
static const char* tr(const char*s){if(!s)return s;const char*p=exact;while(*p){const char*t=p+length(p)+1;if(same(s,p))return t;p=t+length(t)+1;}
 char*out=buffers[(cursor++)&63];unsigned n=0,changed=0;const char*orig=s;
 while(*s&&n<2047){p=parts;int found=0;while(*p){const char*t=p+length(p)+1;if(starts(s,p)){unsigned l=length(t);if(n+l>=2048)return orig;for(unsigned i=0;i<l;i++)out[n++]=t[i];s+=length(p);changed=found=1;break;}p=t+length(t)+1;}if(!found)out[n++]=*s++;}if(*s)return orig;out[n]=0;return changed?out:orig;}
__attribute__((visibility("hidden"))) void translate_args(U*r,int mode){const char*fmt=(const char*)r[1];if(mode==5){vv_window=fmt&&same(fmt,"VV Patching");vv_button=0;}if(mode==4&&vv_window&&vv_button++==0){r[1]=(U)"Aplicar rt0 agora";return;}r[1]=(U)tr(fmt);if(mode==2){if((const char*)r[1]!=fmt)r[2]=0;}if(mode==3)r[2]=(U)tr((const char*)r[2]);
 if(mode==1&&fmt){unsigned arg=2;for(const char*p=fmt;*p&&arg<7;p++){if(*p!='%')continue;p++;if(*p=='%')continue;while(*p&&(*p<'A'||*p>'z'||*p=='h'||*p=='l'||*p=='L'||*p=='z'||*p=='t'||*p=='j')){if(*p=='*')arg++;p++;}if(!*p)break;if(*p=='s'&&arg<7)r[arg]=(U)tr((const char*)r[arg]);if(*p!='f'&&*p!='F'&&*p!='e'&&*p!='E'&&*p!='g'&&*p!='G'&&*p!='a'&&*p!='A')arg++;}}
}
'''.replace('TABLE',table(translations)).replace('PARTS',table(replacements))
# JSON escapes null as \\u0000, which C does not permit. Use octal escape.
c=c.replace('\\u0000','\\000')
(W/'translate.c').write_text(c)
# exact native renderer and its recursive module menu function; no game or ImGui internals.
ranges=[(0x360530,0x36390f),(0x363a70,0x363b5c)]
functions={0x24f320:0,0x2eef10:0,0x2d63d0:0,0x2ef580:0,0x2410b0:0,0x2d1d80:1,0x2d21b0:1,0x2d3560:0,0x2d49e0:0,0x2e1380:0,0x230e80:2,0x230910:2,0x252f60:0,0x253aa0:0,0x2e17b0:3,0x2dbbf0:0,0x2dd160:0}
# discover SliderFloat callee precisely at known call site from source switch.
dis=subprocess.check_output(['objdump','-d','-M','intel',str(source)],text=True)
m=re.search(r'^\s*3634bc:.*call\s+([0-9a-f]+)',dis,re.M);assert m;functions[int(m[1],16)]=0
sites=[]
for m in re.finditer(r'^\s*([0-9a-f]+):\s+e8 ((?:[0-9a-f]{2} ){3}[0-9a-f]{2})\s+call\s+([0-9a-f]+)',dis,re.M):
 address,target=int(m[1],16),int(m[3],16)
 if any(a<=address<b for a,b in ranges) and target in functions:sites.append((address,target))
assert len(sites)>45,len(sites)
asm='.text\n'
special={0x3633bc:(0x2410b0,5),0x36345e:(0x2d3560,4)}
for special_id,(target,mode) in special.items(): functions[special_id]=mode
for target,mode in functions.items():
 asm+=f'.global wrap_{target:x}\nwrap_{target:x}:\n sub $200,%rsp\n'
 for i,reg in enumerate(['rax','rdi','rsi','rdx','rcx','r8','r9']):asm+=f' mov %{reg},{i*8}(%rsp)\n'
 for i in range(8):asm+=f' movdqu %xmm{i},{64+i*16}(%rsp)\n'
 asm+=f' mov %rsp,%rdi\n mov ${mode},%esi\n call translate_args\n'
 for i in range(8):asm+=f' movdqu {64+i*16}(%rsp),%xmm{i}\n'
 for i,reg in enumerate(['rax','rdi','rsi','rdx','rcx','r8','r9']):asm+=f' mov {i*8}(%rsp),%{reg}\n'
 asm+=f' add $200,%rsp\n jmp original_{special.get(target,(target,mode))[0]:x}\n'
asm+='.section .note.GNU-stack,"",@progbits\n'
(W/'wrappers.S').write_text(asm)
assert hashlib.sha256(source.read_bytes()).hexdigest() == '448af80b3f785c50336e93967b58dbf55c05c6958518aa20dbf09724c5a8dc5a', 'Unsupported client version'
b=bytearray(source.read_bytes());phoff=struct.unpack_from('<Q',b,32)[0];n=struct.unpack_from('<H',b,56)[0];ph=[list(struct.unpack_from('<IIQQQQQQ',b,phoff+56*i)) for i in range(n)]
align=lambda x:(x+4095)&~4095
base=align(max(p[3]+p[6] for p in ph if p[0]==1));offset=align(len(b));headsize=56*(n+2);codebase=base+align(headsize)
link='SECTIONS { . = '+hex(codebase)+'; .text : { *(.text*) } .rodata : { *(.rodata*) } . = ALIGN(4096); .bss : { *(.bss*) *(COMMON) } /DISCARD/ : { *(.eh_frame*) *(.comment*) *(.note*) } }\n'
for target in functions:
 if target not in special:link+=f'original_{target:x} = 0x{target:x};\n'
(W/'helper.ld').write_text(link)
def run(*args):subprocess.run(args,cwd=W,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
run('gcc','-c','-Os','-ffreestanding','-fno-builtin','-fPIC','-fvisibility=hidden','-fno-stack-protector','-fno-asynchronous-unwind-tables','-fno-unwind-tables','-o','translate.o','translate.c')
run('gcc','-c','-o','wrappers.o','wrappers.S')
run('ld','-T','helper.ld','-o','helper.elf','wrappers.o','translate.o')
run('objcopy','-O','binary','helper.elf','helper.bin')
elf=(W/'helper.elf').read_bytes();shoff=struct.unpack_from('<Q',elf,40)[0];sn=struct.unpack_from('<H',elf,60)[0]
bss=[struct.unpack_from('<IIQQQQIIQQ',elf,shoff+64*i) for i in range(sn)];bss=[s for s in bss if s[1]==8][0];bssaddr,bsslen=bss[3],bss[5]
symbols={s.split()[2]:int(s.split()[0],16) for s in subprocess.check_output(['nm','--defined-only',str(W/'helper.elf')],text=True).splitlines() if len(s.split())==3}
helper=(W/'helper.bin').read_bytes();rxsize=align(headsize)+len(helper)
for p in ph:
 if p[0]==6:p[2]=offset;p[3]=p[4]=base;p[5]=p[6]=headsize
ph += [[1,5,offset,base,base,rxsize,rxsize,4096],[1,6,align(offset+rxsize),bssaddr,bssaddr,0,bsslen,4096]]
b.extend(bytes(offset-len(b)));b.extend(b''.join(struct.pack('<IIQQQQQQ',*p) for p in ph));b.extend(bytes(offset+align(headsize)-len(b)));b.extend(helper)
# Keep the zero-file-size BSS segment offset within the real file.
b.extend(bytes(align(len(b))-len(b)))
struct.pack_into('<Q',b,32,offset);struct.pack_into('<H',b,56,len(ph))
for address,target in sites:
 assert b[address]==0xe8
 assert address+5+struct.unpack_from('<i',b,address+1)[0]==target
 struct.pack_into('<i',b,address+1,symbols[f'wrap_{address if address in special else target:x}']-address-5)
(W/'mcpelauncher-client').write_bytes(b);(W/'mcpelauncher-client').chmod(0o755)
manifest={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'patched_sha256':hashlib.sha256(b).hexdigest(),'source_client_commit':'78904982c13d7bcec7af4b572b18cac83d930d31','translations':len(translations),'ui_call_sites':[{'address':hex(a),'original':hex(t),'wrapper':hex(symbols[f'wrap_{a if a in special else t:x}'])} for a,t in sites],'protected_ranges':[[hex(a),hex(z)] for a,z in ranges]}
(W/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Built',len(sites),'UI call redirects;',len(translations),'exact translations; helper',len(helper),'bytes')
