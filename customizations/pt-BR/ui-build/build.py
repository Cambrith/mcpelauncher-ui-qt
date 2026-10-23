#!/usr/bin/env python3
"""Gera a personalização pt-BR da interface do lançador (mcpelauncher-ui-qt).

Compila as traduções com lrelease6/lrelease, copia os componentes QML traduzidos
e gera a cópia com redirecionamento de recursos e manifest.json correspondente.
"""
from pathlib import Path
import argparse, ctypes, ctypes.util, hashlib, json, shutil, struct, subprocess, sys

SUPPORTED_SHA256 = 'f81e6c22ecf9143ded07b81645658e7f79c0de5e6f1818ea78cf2c1b2a2a32c8'
APP_ID = 'io.mrarm.mcpelauncher'

def default_source():
    try:
        loc = subprocess.check_output(['flatpak', 'info', '--show-location', APP_ID],
                                      text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.SubprocessError):
        return None
    return Path(loc) / 'files/bin/mcpelauncher-ui-qt'

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--source', type=Path, default=None, help='mcpelauncher-ui-qt original')
    ap.add_argument('--check-only', action='store_true', help='apenas verifica se a versão é suportada')
    opts = ap.parse_args()

    source = opts.source or default_source()
    if source is None or not source.is_file():
        sys.exit(f'Erro: mcpelauncher-ui-qt não encontrado no Flatpak {APP_ID}.')

    stock = source.read_bytes()
    stock_sha = hashlib.sha256(stock).hexdigest()
    if stock_sha != SUPPORTED_SHA256:
        print(f'Versão não suportada da interface (sha256 {stock_sha}).\n'
              f'Esperado: {SUPPORTED_SHA256}', file=sys.stderr)
        sys.exit(3)

    if opts.check_only:
        print('Versão da interface suportada.')
        sys.exit(0)

    lrelease = shutil.which('lrelease6') or shutil.which('lrelease')
    if not lrelease:
        sys.exit('Erro: lrelease6 ou lrelease não encontrado.')

    repo_dir = Path(__file__).resolve().parents[2]  # customizations/pt-BR -> customizations -> repo
    if not (repo_dir / 'qml').exists():
        repo_dir = Path(__file__).resolve().parents[3]
    data_dir = Path.home() / '.var/app' / APP_ID / 'data'
    ui_base = data_dir / 'minecraft-ui-localization'
    i18n_dir = data_dir / 'i18n'

    ui_base.mkdir(parents=True, exist_ok=True)
    (ui_base / 'bin').mkdir(parents=True, exist_ok=True)
    (ui_base / 'qml').mkdir(parents=True, exist_ok=True)
    i18n_dir.mkdir(parents=True, exist_ok=True)

    # 1. Compilar catálogo de traduções
    ts_file = Path(__file__).resolve().parent / 'mcpelauncher-with-qt_pt_BR.ts'
    qm_file = i18n_dir / 'mcpelauncher_pt_BR.qm'
    subprocess.run([lrelease, str(ts_file), '-qm', str(qm_file)], check=True)

    # 2. Copiar componentes QML
    shutil.copytree(repo_dir / 'qml', ui_base / 'qml', dirs_exist_ok=True)
    shutil.copy2(repo_dir / 'qml/main.qml', ui_base / 'qml/MainWindow.qml')

    # 3. Patch no executável
    binary = bytearray(stock)
    zstd = ctypes.CDLL(ctypes.util.find_library('zstd'))
    zstd.ZSTD_compressBound.argtypes = [ctypes.c_size_t]
    zstd.ZSTD_compressBound.restype = ctypes.c_size_t
    zstd.ZSTD_compress.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
    zstd.ZSTD_compress.restype = ctypes.c_size_t
    zstd.ZSTD_isError.argtypes = [ctypes.c_size_t]
    zstd.ZSTD_isError.restype = ctypes.c_uint

    patches = []

    # Patch RequestGoogleCredentials
    payload1 = b'import QtQuick\nimport "file:/var/data/minecraft-ui-localization/qml" as Local\nLocal.RequestGoogleCredentials {}\n'
    off1 = 2658328 + 4
    alloc1 = 2557 - 4
    assert struct.unpack('>I', stock[off1-4:off1])[0] == alloc1
    binary[off1-4:off1] = struct.pack('>I', len(payload1))
    binary[off1:off1+alloc1] = payload1 + bytes(alloc1 - len(payload1))
    patches.append({'offset': off1 - 4, 'length': alloc1 + 4, 'file': 'qml/RequestGoogleCredentials.qml'})

    # Patch main.qml
    payload2 = b'import QtQuick\nimport "file:/var/data/minecraft-ui-localization/qml" as Local\nLocal.MainWindow {}\n'
    off2 = 2677439 + 4
    alloc2 = 2607 - 4
    assert struct.unpack('>I', stock[off2-4:off2])[0] == alloc2
    out = ctypes.create_string_buffer(zstd.ZSTD_compressBound(len(payload2)))
    n = zstd.ZSTD_compress(out, len(out), payload2, len(payload2), 13)
    assert not zstd.ZSTD_isError(n)
    comp2 = out.raw[:n]
    binary[off2-4:off2] = struct.pack('>I', len(comp2))
    binary[off2:off2+alloc2] = comp2 + bytes(alloc2 - len(comp2))
    patches.append({'offset': off2 - 4, 'length': alloc2 + 4, 'file': 'qml/main.qml'})

    # Patch :/translations
    old = b':/translations'
    new = b'/var/data/i18n'
    assert stock.count(old) == 1
    off3 = stock.index(old)
    binary[off3:off3+len(old)] = new
    patches.append({'offset': off3, 'length': len(old), 'file': 'translation search directory'})

    # Gravar binário corrigido
    patched_bin = ui_base / 'bin/mcpelauncher-ui-qt'
    patched_bin.write_bytes(binary)
    patched_bin.chmod(0o755)

    # Coletar hashes dos arquivos externos
    external = {
        str(p.relative_to(data_dir)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((ui_base / 'qml').rglob('*')) if p.is_file()
    }
    external['i18n/mcpelauncher_pt_BR.qm'] = hashlib.sha256(qm_file.read_bytes()).hexdigest()

    manifest = {
        'source_sha256': stock_sha,
        'patched_sha256': hashlib.sha256(binary).hexdigest(),
        'version': 'v1.8.4 build 117',
        'patches': patches,
        'external_files': external,
        'translation_messages': 3441,
        'mod_descriptions': 12,
        'news_translation': 'public titles and summaries only; MyMemory public API; local SQLite cache'
    }

    (ui_base / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Tradução da interface configurada com sucesso!')

if __name__ == '__main__':
    main()
