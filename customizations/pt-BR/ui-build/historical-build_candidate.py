from pathlib import Path
import json, hashlib, ctypes, ctypes.util, shutil, struct
base=Path.home()/'.var/app/io.mrarm.mcpelauncher/data/minecraft-ui-localization'
source=Path('/var/lib/flatpak/app/io.mrarm.mcpelauncher/current/active/files/bin/mcpelauncher-ui-qt')
stock=source.read_bytes();binary=bytearray(stock)
assert hashlib.sha256(stock).hexdigest()=='f81e6c22ecf9143ded07b81645658e7f79c0de5e6f1818ea78cf2c1b2a2a32c8'
shutil.copytree('/tmp/minecraft-complete-pt/qml',base/'qml',dirs_exist_ok=True)
i18n=base.parent/'i18n';i18n.mkdir(exist_ok=True)
shutil.copy2('/tmp/minecraft-complete-pt/mcpelauncher_pt_BR.qm',i18n/'mcpelauncher_pt_BR.qm')
zstd=ctypes.CDLL(ctypes.util.find_library('zstd'))
zstd.ZSTD_compressBound.argtypes=[ctypes.c_size_t];zstd.ZSTD_compressBound.restype=ctypes.c_size_t
zstd.ZSTD_compress.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_int];zstd.ZSTD_compress.restype=ctypes.c_size_t
zstd.ZSTD_isError.argtypes=[ctypes.c_size_t];zstd.ZSTD_isError.restype=ctypes.c_uint
patches=[]
for e in json.loads(Path('/tmp/minecraft-qml-resource-index.json').read_text()):
 if e['file'] not in ['qml/main.qml','qml/RequestGoogleCredentials.qml']:continue
 name='MainWindow' if e['file']=='qml/main.qml' else 'RequestGoogleCredentials'
 payload=('import QtQuick\nimport "file:/var/data/minecraft-ui-localization/qml" as Local\nLocal.'+name+' {}\n').encode()
 if e.get('compression')=='zstd':
  out=ctypes.create_string_buffer(zstd.ZSTD_compressBound(len(payload)))
  n=zstd.ZSTD_compress(out,len(out),payload,len(payload),19)
  assert not zstd.ZSTD_isError(n)
  payload=out.raw[:n]
 offset=e['offset'];allocation=e['length'];assert len(payload)<=allocation
 assert struct.unpack('>I',stock[offset-4:offset])[0]==allocation
 binary[offset-4:offset]=struct.pack('>I',len(payload))
 binary[offset:offset+allocation]=payload+bytes(allocation-len(payload))
 patches.append({'offset':offset-4,'length':allocation+4,'file':e['file']})
old=b':/translations';new=b'/var/data/i18n';assert len(old)==len(new) and stock.count(old)==1
offset=stock.index(old);binary[offset:offset+len(old)]=new;patches.append({'offset':offset,'length':len(old),'file':'translation search directory'})
for i,(a,b) in enumerate(zip(stock,binary)):
 if a!=b:assert any(e['offset']<=i<e['offset']+e['length'] for e in patches)
trial=base/'trial/bin/mcpelauncher-ui-qt';trial.parent.mkdir(parents=True,exist_ok=True);temp=trial.with_suffix('.tmp');temp.write_bytes(binary);temp.chmod(0o755);temp.replace(trial)
external={str(p.relative_to(base.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((base/'qml').rglob('*')) if p.is_file()}
external['i18n/mcpelauncher_pt_BR.qm']=hashlib.sha256((i18n/'mcpelauncher_pt_BR.qm').read_bytes()).hexdigest()
manifest={'source_sha256':hashlib.sha256(stock).hexdigest(),'patched_sha256':hashlib.sha256(binary).hexdigest(),'version':'v1.8.4 build 117','patches':patches,'external_files':external,'translation_messages':405,'mod_descriptions':12,'news_translation':'public titles and summaries only; MyMemory public API; local SQLite cache'}
Path('/tmp/minecraft-complete-pt/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Candidate ready; original untouched; changes limited to',len(patches),'resource ranges;',len(external),'external files.')
