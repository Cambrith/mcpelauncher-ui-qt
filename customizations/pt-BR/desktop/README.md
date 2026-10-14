# Modelos `.desktop`

Modelos genéricos, sem caminhos pessoais. O `install.sh` substitui:

- `@BINDIR@` pelo diretório dos inicializadores (padrão `~/.local/bin`);
- `@ICON_LAUNCHER@` / `@ICON_GAME@` pelos nomes dos ícones (`minecraft-launcher-creeper`,
  `minecraft-bedrock-block`) ou pelo ícone original `io.mrarm.mcpelauncher` com `--sem-icones`.

`io.mrarm.mcpelauncher.desktop` em `~/.local/share/applications` tem prioridade sobre o atalho
exportado pelo Flatpak e abre o launcher pelo inicializador traduzido.
`minecraft-bedrock-game.desktop` abre direto o perfil `Default`.
