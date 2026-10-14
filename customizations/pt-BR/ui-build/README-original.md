# Tradução local do Minecraft Bedrock Launcher — 8 de outubro de 2026

Aplicada à versão v1.8.4, compilação 117. O Flatpak original permanece intacto.

- 405 mensagens do aplicativo, todas concluídas; marcadores %1, %2 etc. preservados.
- 44 componentes QML auditados, com alterações apenas de apresentação/tradução.
- Catálogos oficiais qtbase_pt_BR e qtdeclarative_pt_BR do runtime instalado incluídos no catálogo: 3441 mensagens totais.
- Descrições dos 12 mods atuais traduzidas localmente. Nomes, versões e arquivos dos mods preservados.
- Títulos e resumos atuais de notícias têm tradução local revisada. Textos novos são enviados exclusivamente para a API pública MyMemory, en → pt-BR. Não há chave, conta de tradução ou serviço pago configurado.
- Cache SQLite: ~/.var/app/io.mrarm.mcpelauncher/data/Minecraft Linux Launcher/Minecraft Linux Launcher UI/QML/OfflineStorage/Databases/6ffa3983a7f24a4734405f2701f9021f.sqlite
- Somente consultas GET /get com os títulos/resumos públicos. Perfis, nomes de usuário, credenciais, arquivos do jogo, erros e registros não são enviados.
- Requisições serializadas, intervalo de 750 ms, prazo de 15 s, segmentação de trechos acima de 500 bytes. Falhas de cota acionam espera de 5 minutos nesta sessão; traduções falhas não entram no cache. Falhas exibem aviso em português e o texto original para preservar o conteúdo.
- Não há promessa de disponibilidade ilimitada ou qualidade perfeita da tradução automática. O Google recusou as solicitações feitas pelo Flatpak; não há tentativa de contornar esse bloqueio nem fallback silencioso entre serviços.
- A licença GNU GPL original, identificadores técnicos, nomes próprios e o conteúdo literal dos registros não foram alterados. Textos embutidos nas imagens e páginas externas abertas pelos links ficam fora do catálogo da interface. Novas descrições de mods precisam de atualização do catálogo local.

## Arquivos ativos

`bin/mcpelauncher-ui-qt`: cópia local do executável com apenas três intervalos de recursos alterados: raiz QML, raiz QML de solicitação de credenciais e caminho do catálogo de tradução. Código executável preservado.
`qml/`: cópias dos componentes com traduções, `MainWindow.qml` e `NewsTranslation.js`.
`../i18n/mcpelauncher_pt_BR.qm`: catálogo efetivamente carregado.
`resources/mcpelauncher_pt_BR.ts`: traduções do aplicativo editáveis.
`resources/mcpelauncher-with-qt_pt_BR.ts`: catálogo unido às traduções oficiais Qt.
`manifest.json`: hashes da origem, executável local e todos os arquivos externos ativos.
`~/.local/bin/minecraft-launcher-localized`: verifica todos os hashes e executa a personalização. Se a versão do Flatpak mudar ou um recurso não corresponder, abre a interface original com aviso.
Os recursos antigos compactados em `resources/` são registros da personalização anterior e não são usados nesta versão.

## Reversão

Feche o lançador e execute o script abaixo para voltar à tradução existente antes desta ampliação. A versão retirada é preservada junto ao backup. O cache de textos públicos pode permanecer; ele não contém dados de conta. Não se restaura configuração do jogo nem arquivos de perfil.

~/.local/state/minecraft-bedrock-kde/complete-pt-br-20261008/reverter-traducao.py

Backup: ~/.local/state/minecraft-bedrock-kde/backups/complete-pt-br-20261008-090723
