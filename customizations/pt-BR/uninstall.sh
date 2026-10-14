#!/usr/bin/env bash
# Remove o que o install.sh instalou e oferece restaurar o backup mais recente.
set -euo pipefail
STATE="${XDG_STATE_HOME:-$HOME/.local/state}/mcpelauncher-pt-br"
LIST="$STATE/installed.txt"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
restore=0
case "${1:-}" in
  --restaurar) restore=1 ;;
  -h|--help) echo "Uso: $0 [--restaurar]  (--restaurar devolve os arquivos do backup mais antigo, ou seja, os originais)"; exit 0 ;;
  '') ;;
  *) echo "Opção desconhecida: $1" >&2; exit 2 ;;
esac
[[ -f "$LIST" ]] || { echo 'Nada instalado pelo install.sh foi encontrado.'; exit 0; }
while IFS= read -r f; do
  [[ -n "$f" && "$f" == "$HOME"/* ]] || continue
  if [[ -e "$f" ]]; then rm -f -- "$f"; echo "  - $f"; fi
done < "$LIST"
if (( restore )) && [[ -d "$STATE/backups" ]]; then
  # O backup mais antigo de cada arquivo é o original anterior à primeira instalação.
  for b in "$STATE"/backups/*/; do
    while IFS= read -r -d '' f; do
      dst="${f#"${b%/}"}"
      if [[ ! -e "$dst" ]]; then install -D -m "$(stat -c %a "$f")" -- "$f" "$dst"; echo "  ↺ $dst"; fi
    done < <(find "$b" -type f -print0)
  done
fi
rm -f -- "$LIST"
find "$HOME/.var/app/io.mrarm.mcpelauncher/data/minecraft-game-menu-localization" -type d -empty -delete 2>/dev/null || true
if command -v update-desktop-database >/dev/null; then update-desktop-database -q "$DATA_HOME/applications" || true; fi
echo "Removido. Backups mantidos em $STATE/backups."
