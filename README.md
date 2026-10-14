# Minecraft Bedrock Launcher — PT-BR e personalizações para Linux

Este repositório é um **fork** de [minecraft-linux/mcpelauncher-ui-qt](https://github.com/minecraft-linux/mcpelauncher-ui-qt), mantido por Cambrith para documentar e desenvolver uma tradução ampliada da interface do launcher, a tradução dos menus nativos do cliente Linux e sua integração com o KDE Plasma.

> **Status:** instalador testado com o Flatpak v1.8.4 do Flathub. Os patches binários são específicos de versão; executáveis modificados, APKs, mundos e credenciais não são distribuídos.

## O que tem aqui

- **Interface do launcher em pt-BR**: catálogo `mcpelauncher_pt_BR.ts` (**405 mensagens**) e ajustes nos arquivos QML. Notícias traduzidas por catálogo local e, opcionalmente, pela API pública MyMemory.
- **Menus do jogo em pt-BR** (barra de menus, vídeo, HUD do cliente Linux): fontes do patch e `build.py`, que gera a cópia traduzida **a partir do binário do seu próprio Flatpak**.
- **Ícones personalizados** (Creeper quadrado e bloco de grama) e atalhos para o KDE Plasma e outros ambientes.
- **Ajustes de jogabilidade**: exemplo comentado das configurações do cliente.
- `install.sh` / `uninstall.sh`: instalação segura, com backup, no seu `HOME`.

## Instalação rápida

Requisitos: Linux x86_64, Flatpak, `python3`, `gcc` e `binutils`, **e uma cópia legítima do Minecraft Bedrock** (o launcher baixa o jogo da sua conta Google Play; nada do jogo vem deste repositório).

```bash
flatpak install flathub io.mrarm.mcpelauncher     # se ainda não tiver
git clone -b pt-br-cambrith https://github.com/Cambrith/mcpelauncher-ui-qt.git
cd mcpelauncher-ui-qt/customizations/pt-BR
./install.sh --simular   # mostra o que será feito
./install.sh             # opções: --sem-icones, --sem-menus-jogo, --com-ajustes
```

Para desfazer: `./uninstall.sh` (ou `./uninstall.sh --restaurar` para devolver os arquivos anteriores do backup).

> **Versão suportada:** a tradução dos menus do jogo só funciona com o Flatpak `io.mrarm.mcpelauncher` **v1.8.4** (commit Flathub `ce79138…`, de 17/09/2026), cujo `mcpelauncher-client` tem SHA-256 `448af80b…5a8dc5a`. Em outra versão, o instalador avisa e **o jogo continua funcionando com os menus originais em inglês**. A tradução da interface do launcher via patch binário **não** é aplicada pelo instalador; para ela, compile este fork (veja a documentação).

**[Documentação completa, limitações e segurança](customizations/pt-BR/README.md).**

## Por que não há binários

O launcher é GPL-3.0. Distribuir um executável modificado exigiria publicar junto a fonte correspondente exata; por isso o repositório traz **só as fontes e scripts**, e o binário traduzido é gerado na sua máquina. Também não há APKs, arquivos do jogo, mundos nem credenciais.

## Marcas

**Não afiliado à Mojang/Microsoft; Minecraft é marca da Mojang/Microsoft.** Os ícones fazem referência a elementos visuais do jogo; veja [`icons/AVISO-MARCAS.md`](customizations/pt-BR/icons/AVISO-MARCAS.md).

## Projeto original

O upstream é licenciado sob [GNU GPL v3](LICENSE). Este fork mantém a autoria, as contribuições históricas e a licença original. Não é um produto oficial da Mojang ou Microsoft.

---

### Nota mantida do projeto upstream

_We evaluate to use weblate for translation <https://hosted.weblate.org/projects/minecraft-linux/mcpelauncher-ui-qt/>_

- `cmake -DUPDATE_TRANSLATIONS=ON` updates qm files with source code content
