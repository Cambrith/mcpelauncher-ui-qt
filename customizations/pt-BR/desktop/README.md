# Modelos `.desktop`

Modelos genéricos, sem caminhos pessoais. O `install.sh` substitui:

- `@BINDIR@` pelo diretório dos inicializadores (padrão `~/.local/bin`);
- `@ICON_LAUNCHER@` / `@ICON_GAME@` pelos nomes dos ícones (`minecraft-launcher-creeper`,
  `minecraft-bedrock-block`) ou pelo ícone original `io.mrarm.mcpelauncher` com `--sem-icones`.

`io.mrarm.mcpelauncher.desktop` em `~/.local/share/applications` tem prioridade sobre o atalho
exportado pelo Flatpak e abre o launcher pelo inicializador traduzido.
`minecraft-bedrock-game.desktop` abre direto o perfil `Default`.

`io.mrarm.mcpelauncher-ui-qt.desktop` é oculto (`NoDisplay=true`): existe só para que a janela do
launcher, cujo `app_id` é `io.mrarm.mcpelauncher-ui-qt`, seja associada ao ícone correto na barra
de tarefas e no alternador de janelas. Sem ele o ambiente mostra um ícone genérico.

## Ícone da janela do jogo (KDE Plasma)

Dentro do Flatpak a janela do jogo se identifica como `io.mrarm.mcpelauncher` (o mesmo ID do
launcher), então herdaria o ícone do launcher. No KDE, uma regra de janela corrige isso
(Configurações do Sistema → Regras de janela, ou em `~/.config/kwinrulesrc`):
classe `io.mrarm.mcpelauncher` (exata) + título `Minecraft` (exato) →
forçar *Nome do arquivo desktop* `minecraft-bedrock-game` e ícone `minecraft-bedrock-block`.
