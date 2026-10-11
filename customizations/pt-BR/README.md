# Personalizações PT-BR e KDE Plasma — Cambrith

Este diretório documenta **as alterações locais observadas em outubro de 2026** na instalação Flatpak `io.mrarm.mcpelauncher`, versão v1.8.4 (build 117), com cliente 1.26.52.3.

## Componentes

- `../../qml/` e `../../mcpelauncher_pt_BR.ts`: personalização integrada ao fork Qt6. Apenas os componentes diferentes da branch `qt6` do upstream foram sobrepostos. O arquivo QML do usuário `MainWindow.qml` foi colocado em `qml/main.qml` para corresponder à entrada do recurso Qt. `qml/NewsTranslation.js` foi adicionado a `qml.qrc`.
- `ui-build/`: script histórico que modifica a cópia *local* do binário de interface do Flatpak e seus metadados de integridade. **Não é instalador universal**: usa caminhos temporários `/tmp/...` ausentes neste repositório e hashes fixos. Não execute automaticamente.
- `game-client/`: código-fonte C, Assembly e Python para tradução de textos renderizados pelos menus nativos do cliente Linux. Altera uma cópia de binário, validando SHA-256; **é específico de versão e arquitetura x86_64**. O arquivo `manifest-game-client.json` descreve um build executado localmente; não distribui o executável modificado.
- `scripts/`: inicializador Python que seleciona cópias locais com base em hashes e tem fallback ao Flatpak original. `minecraft-bedrock-direct-original` é uma implementação anterior, preservada como registro, que não aplica a tradução nativa.
- `desktop/originais/`: arquivos `.desktop` de uma instalação pessoal, com caminhos `/home/cambrith`. **São exemplos**, não devem ser instalados em outras contas sem substituição desses caminhos.

## Reproduzir a interface a partir do código-fonte

1. Instale as dependências de compilação do projeto original conforme sua documentação. Este fork preserva a estrutura do upstream e foi preparado a partir da branch `qt6`.
2. Compile o launcher pela configuração padrão do projeto, tendo disponíveis os recursos `Qt6LinguistTools` para que `mcpelauncher_pt_BR.ts` seja compilado em `.qm`.
3. Selecione o idioma `pt_BR` nas opções de idioma do sistema/launcher. O script de tradução dinâmica de notícias usa **MyMemory** e pode enviar somente títulos e resumos públicos dos artigos para a API do serviço. A tradução de notícias dependerá de rede, cota e terceiros.
4. Para testar patches do cliente, trabalhe **somente com cópias** dos executáveis e confirme os hashes em `game-client/manifest-game-client.json`. Eles não são aplicados pela compilação Qt padrão.

## Limitações e segurança

- **Não há garantia de compilação ou funcionamento em novas versões**: o código ainda não foi recompilado ou testado neste fork.
- Não inclua APKs, mundos, credenciais, tokens, binários proprietários, caches, nem imagens do jogo obtidas de fontes sem direitos de redistribuição.
- O arquivo legado `ui-build/historical-build_candidate.py` requer entradas que não foram fornecidas: `qml` e `.qm` sob `/tmp/minecraft-complete-pt/`, além de `/tmp/minecraft-qml-resource-index.json`.
- O catálogo agregado de traduções gerais do Qt (`mcpelauncher-with-qt_pt_BR.ts`, 614 KB) foi **omitido**, pois resulta de conteúdo distribuído separadamente com Qt. A tradução específica do launcher foi preservada em `mcpelauncher_pt_BR.ts`.
- Alguns scripts são históricos e possuem caminhos locais; revise antes de instalar em outro computador.

## Licença e atribuição

O upstream [minecraft-linux/mcpelauncher-ui-qt](https://github.com/minecraft-linux/mcpelauncher-ui-qt) é GPL-3.0. O código adaptado e as contribuições ao fork são publicadas sob os mesmos termos, mantendo licença e histórico do fork. Minecraft é propriedade de seus respectivos titulares; este fork não distribui o jogo.
