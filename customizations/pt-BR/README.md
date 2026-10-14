# Personalizações pt-BR e KDE Plasma

Tradução completa para português do Brasil do Minecraft Bedrock Launcher no Linux
(interface do launcher **e** menus nativos do jogo), ícones, atalhos e ajustes de jogabilidade.

**Não afiliado à Mojang/Microsoft; Minecraft é marca da Mojang/Microsoft.**

## Requisitos

- Linux x86_64 com Flatpak e o launcher `io.mrarm.mcpelauncher` (Flathub).
- `python3`, `gcc` e `binutils` (`objdump`, `ld`, `objcopy`, `nm`) para gerar os menus traduzidos.
- **Você precisa ter o Minecraft Bedrock** (comprado na Google Play). Este repositório não contém nem baixa o jogo.

### Versões suportadas

| Componente | Versão | SHA-256 do original |
|---|---|---|
| Flatpak `io.mrarm.mcpelauncher` | v1.8.4 (Flathub, commit `ce7913847af3…`, 17/09/2026) | — |
| `files/bin/mcpelauncher-client` (menus do jogo) | cliente `78904982c13d` | `448af80b3f785c50336e93967b58dbf55c05c6958518aa20dbf09724c5a8dc5a` |
| `files/bin/mcpelauncher-ui-qt` (patch histórico da interface) | v1.8.4 build 117 | `f81e6c22ecf9143ded07b81645658e7f79c0de5e6f1818ea78cf2c1b2a2a32c8` |

Se o Flatpak for atualizado e o hash mudar, o instalador e o inicializador detectam isso e
**usam o cliente original: o jogo funciona normalmente, mas com os menus em inglês**.
O hash da cópia *gerada* varia conforme a versão do `gcc`/`ld`; o `manifest.json` gerado na sua
máquina registra o valor correto e é ele que o inicializador confere.

## Instalar

```bash
./install.sh --simular   # mostra tudo o que seria feito, sem alterar nada
./install.sh
```

Opções: `--sem-icones` (mantém o ícone original), `--sem-menus-jogo`, `--com-ajustes`
(aplica `gameplay/mcpelauncher-client-settings.exemplo.txt`; seu arquivo atual vai para o backup).

O instalador:

1. confere se o Flatpak `io.mrarm.mcpelauncher` está instalado (senão, mostra `flatpak install flathub io.mrarm.mcpelauncher`);
2. instala `minecraft-launcher-localized` em `~/.local/bin`;
3. instala ícones em `~/.local/share/icons/hicolor` e atalhos em `~/.local/share/applications`;
4. roda `game-client/build.py` sobre o `mcpelauncher-client` **do seu Flatpak** (só leitura) e grava a cópia traduzida e o `manifest.json` em `~/.var/app/io.mrarm.mcpelauncher/data/minecraft-game-menu-localization/`;
5. faz backup de qualquer arquivo diferente antes de substituí-lo, em `~/.local/state/mcpelauncher-pt-br/backups/`.

Pode ser executado várias vezes (arquivos iguais são ignorados). Nada fora do seu `HOME` é alterado
e o Flatpak original não é modificado.

## Desinstalar

```bash
./uninstall.sh              # remove o que foi instalado
./uninstall.sh --restaurar  # remove e devolve os arquivos originais guardados no backup
```

## Componentes

- `../../qml/`, `../../mcpelauncher_pt_BR.ts`, `../../qml.qrc`: tradução da interface integrada ao fork Qt6 (compilar com `Qt6LinguistTools`, conforme o projeto original). `qml/NewsTranslation.js` traduz notícias e pode enviar títulos/resumos públicos à API MyMemory.
- `game-client/`: fontes C/Assembly e `build.py` do patch dos menus nativos (`build.py --help`). `manifest-game-client.json` é o registro de um build de referência.
- `scripts/minecraft-launcher-localized`: abre o Flatpak usando as cópias traduzidas somente se os hashes conferirem; senão usa o original. `scripts/minecraft-bedrock-direct`: alternativa simples, sem tradução.
- `desktop/`: modelos `.desktop` genéricos (veja `desktop/README.md`).
- `icons/`: ícones personalizados; leia `icons/AVISO-MARCAS.md`.
- `gameplay/`: exemplo comentado das configurações do cliente (FPS, VSync, HUD, correções de teclado).
- `ui-build/`: registros do patch histórico da interface (`historical-build_candidate.py`, `manifest-v1.8.4.json`), `translation-additions.json` e o catálogo completo `mcpelauncher-with-qt_pt_BR.ts` (inclui as mensagens do próprio Qt). O script histórico **não** é usado pelo instalador: depende de arquivos temporários não incluídos.

## Por que não há binários

O mcpelauncher é GPL-3.0. Um executável modificado é obra derivada e só pode ser redistribuído
junto da fonte correspondente completa. Para evitar isso e para não depender de um binário
de terceiros, este repositório traz **só as fontes, os patches e os scripts**; o binário traduzido
é gerado localmente a partir da cópia que você já instalou. Também não são incluídos APKs,
arquivos ou dados do jogo, mundos, contas ou tokens.

## Limitações

- O patch do cliente é específico de versão e de x86_64; atualizações do Flatpak exigem revisão.
- Os menus traduzidos só aparecem ao abrir pelo atalho/inicializador `minecraft-launcher-localized`.
- Testado em Debian 13 com Flatpak de usuário; o jogo em si não foi executado nos testes automáticos.

## Licença

Código sob GPL-3.0, como o upstream [minecraft-linux/mcpelauncher-ui-qt](https://github.com/minecraft-linux/mcpelauncher-ui-qt).
Os ícones não fazem parte da licença GPL (veja o aviso de marcas).
