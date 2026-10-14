#!/usr/bin/env bash
# Instala a personalização pt-BR do Minecraft Bedrock Launcher (Flatpak io.mrarm.mcpelauncher).
# Seguro para rodar várias vezes: arquivos idênticos são ignorados e qualquer arquivo
# diferente é copiado para um backup antes de ser substituído. Nada fora do seu HOME é alterado.
set -euo pipefail

APP_ID=io.mrarm.mcpelauncher
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BINDIR="${BINDIR:-$HOME/.local/bin}"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
STATE="${XDG_STATE_HOME:-$HOME/.local/state}/mcpelauncher-pt-br"
APP_DATA="$HOME/.var/app/$APP_ID/data"
GAME_DIR="$APP_DATA/minecraft-game-menu-localization"
SETTINGS="$APP_DATA/mcpelauncher/mcpelauncher-client-settings.txt"
BACKUP="$STATE/backups/$(date +%Y%m%d-%H%M%S)"
LIST="$STATE/installed.txt"

icons=1 game=1 settings=0 dry=0
usage() {
  cat <<USO
Uso: $0 [opções]
  --sem-icones     não instala os ícones personalizados (usa o ícone original)
  --sem-menus-jogo não gera a tradução dos menus nativos do jogo
  --com-ajustes    copia gameplay/mcpelauncher-client-settings.exemplo.txt para as
                   configurações do cliente (o arquivo atual vai para o backup)
  --simular        mostra o que seria feito, sem alterar nada
  -h, --help       esta ajuda
USO
}
for arg in "$@"; do
  case "$arg" in
    --sem-icones) icons=0 ;;
    --sem-menus-jogo) game=0 ;;
    --com-ajustes) settings=1 ;;
    --simular) dry=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opção desconhecida: $arg" >&2; usage >&2; exit 2 ;;
  esac
done

say() { printf '%s\n' "$*"; }
run() { if (( dry )); then say "[simulação] $*"; else "$@"; fi; }

# Copia $1 (arquivo) para $2 com modo $3; faz backup de $2 se existir e for diferente.
put() {
  local src="$1" dst="$2" mode="$3"
  if [[ -f "$dst" ]] && cmp -s "$src" "$dst"; then
    say "  = $dst"
  else
    if [[ -e "$dst" ]]; then
      say "  ! $dst (backup em $BACKUP)"
      run mkdir -p "$BACKUP$(dirname -- "$dst")"
      run cp -a -- "$dst" "$BACKUP$dst"
    else
      say "  + $dst"
    fi
    run install -D -m "$mode" -- "$src" "$dst"
  fi
  if (( ! dry )); then
    mkdir -p "$STATE"; touch "$LIST"
    grep -qxF -- "$dst" "$LIST" || printf '%s\n' "$dst" >> "$LIST"
  fi
}

say '== Verificando o Flatpak'
command -v flatpak >/dev/null || { say 'Flatpak não encontrado. Instale-o pelo gerenciador de pacotes da sua distribuição.' >&2; exit 1; }
if ! flatpak info "$APP_ID" >/dev/null 2>&1; then
  say "O launcher ($APP_ID) não está instalado. Instale com:" >&2
  say "  flatpak install flathub $APP_ID" >&2
  say 'Abra-o uma vez, faça login e baixe o jogo; depois rode este script de novo.' >&2
  exit 1
fi
LOCATION="$(flatpak info --show-location "$APP_ID")"
say "  $APP_ID: $(flatpak info "$APP_ID" | awk -F': *' '/(Version|Versão):/{print $2; exit}') em $LOCATION"

TMP="$(mktemp -d)"; trap 'rm -rf -- "$TMP"' EXIT

say '== Inicializadores'
put "$HERE/scripts/minecraft-launcher-localized" "$BINDIR/minecraft-launcher-localized" 0755

if (( icons )); then
  say '== Ícones (veja icons/AVISO-MARCAS.md)'
  while IFS= read -r -d '' png; do
    put "$png" "$DATA_HOME/icons/${png#"$HERE/icons/"}" 0644
  done < <(find "$HERE/icons/hicolor" -name '*.png' -print0 | sort -z)
  icon_launcher=minecraft-launcher-creeper icon_game=minecraft-bedrock-block
else
  icon_launcher=$APP_ID icon_game=$APP_ID
fi

say '== Atalhos do menu'
for desktop in "$HERE"/desktop/*.desktop; do
  sed -e "s|@BINDIR@|$BINDIR|g" -e "s|@ICON_LAUNCHER@|$icon_launcher|g" -e "s|@ICON_GAME@|$icon_game|g" \
    "$desktop" > "$TMP/$(basename -- "$desktop")"
  put "$TMP/$(basename -- "$desktop")" "$DATA_HOME/applications/$(basename -- "$desktop")" 0644
done

if (( game )); then
  say '== Tradução dos menus do jogo'
  rc=0
  python3 "$HERE/game-client/build.py" --source "$LOCATION/files/bin/mcpelauncher-client" --check-only || rc=$?
  if (( rc == 3 )); then
    say '  Esta versão do cliente não é suportada: os menus do jogo ficarão em inglês.'
    say '  (O restante da instalação continua funcionando.)'
  elif (( rc != 0 )); then
    say '  Não foi possível verificar o cliente; pulando a tradução dos menus.' >&2
  elif (( dry )); then
    say "[simulação] build.py geraria $GAME_DIR/bin/mcpelauncher-client"
  elif python3 "$HERE/game-client/build.py" --source "$LOCATION/files/bin/mcpelauncher-client" --outdir "$TMP/game"; then
    patched="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["patched_sha256"])' "$TMP/game/manifest.json")"
    [[ "$(sha256sum "$TMP/game/mcpelauncher-client" | cut -d' ' -f1)" == "$patched" ]] || { say 'Hash da cópia gerada não confere; abortando.' >&2; exit 1; }
    put "$TMP/game/mcpelauncher-client" "$GAME_DIR/bin/mcpelauncher-client" 0755
    put "$TMP/game/manifest.json" "$GAME_DIR/manifest.json" 0644
  else
    say '  Falha ao gerar a cópia traduzida (gcc/binutils instalados?). Os menus ficarão em inglês.' >&2
  fi
fi

if (( settings )); then
  say '== Ajustes de jogabilidade'
  grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$HERE/gameplay/mcpelauncher-client-settings.exemplo.txt" > "$TMP/settings.txt"
  put "$TMP/settings.txt" "$SETTINGS" 0644
fi

if (( ! dry )); then
  if command -v update-desktop-database >/dev/null; then update-desktop-database -q "$DATA_HOME/applications" || true; fi
  if command -v gtk-update-icon-cache >/dev/null; then gtk-update-icon-cache -q -t "$DATA_HOME/icons/hicolor" 2>/dev/null || true; fi
fi
[[ ":$PATH:" == *":$BINDIR:"* ]] || say "Aviso: $BINDIR não está no PATH (os atalhos usam o caminho completo, então funcionam mesmo assim)."
say "Pronto. Para desfazer: $HERE/uninstall.sh"
