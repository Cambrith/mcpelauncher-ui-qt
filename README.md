# Minecraft Bedrock Launcher — PT-BR e personalizações para Linux

Este repositório é um **fork** de [minecraft-linux/mcpelauncher-ui-qt](https://github.com/minecraft-linux/mcpelauncher-ui-qt), mantido por Cambrith para documentar e desenvolver uma tradução ampliada da interface do launcher, a tradução dos menus nativos do cliente Linux e sua integração com o KDE Plasma.

> **Status:** código-fonte documentado, sem garantia de compilação em novas versões. Os patches binários históricos são específicos de versão; executáveis modificados, APKs, mundos e credenciais não são distribuídos.

## Personalizações

- Catálogo `mcpelauncher_pt_BR.ts` com **405 mensagens** traduzidas, além de modificações de interface QML.
- Notícias em português brasileiro por catálogo local e consulta opcional à API pública MyMemory para títulos e resumos não traduzidos.
- Traduções dos menus nativos do Minecraft Bedrock Launcher e opções de vídeo/HUD via fontes do patch para cliente Linux x86_64.
- Scripts para execução do launcher localizado e do jogo diretamente, atalhos KDE Plasma e validação por hash SHA-256 para fallback seguro.

**[Leia a documentação das personalizações, limitações e notas de segurança](customizations/pt-BR/README.md).**

## Projeto original

O upstream é licenciado sob [GNU GPL v3](LICENSE). Este fork mantém a autoria, as contribuições históricas e a licença original. Não é um produto oficial da Mojang ou Microsoft.

---

### Nota mantida do projeto upstream

_We evaluate to use weblate for translation <https://hosted.weblate.org/projects/minecraft-linux/mcpelauncher-ui-qt/>_

- `cmake -DUPDATE_TRANSLATIONS=ON` updates qm files with source code content
