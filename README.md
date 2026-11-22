# Sistema de Inventário Patrimonial — CFC

Sistema de gestão patrimonial da Gerência de Serviços Administrativos (Gersev) do Conselho Federal de
Contabilidade: inventário físico por evento (comissão, salas, leitura por plaqueta, fotos, sobras, painel e
relatório), Termos de Responsabilidade (por centro de custo e individuais) e Termos de Devolução, com
**Copiar para o SEI**, envio ao SEI por robô, download em `.docx` e atualização automática da base a partir
do SPW. Roda como programa local (Windows) ou na web (Docker). Os dados ficam num SQLite
(`dados/termos.db`) mantido pelo próprio sistema.

## Trabalho de Conclusão de Curso — MBA USP/Esalq

Este repositório é o produto técnico do Trabalho de Conclusão de Curso **"Automação de inventários no
setor público com Data Science e infraestrutura open source replicável"**, de Antônio Rodrigues de Sousa
Júnior, MBA em Data Science e Analytics da USP/Esalq (turma 2025–2026), sob orientação do Prof. PhD.
Gabriel Gomes de Oliveira.

### A pesquisa

Pesquisa-ação no CFC, autarquia federal em Brasília com 7.428 registros patrimoniais (3.519 bens ativos em
97 localizações). O inventário anual era manual: listagens impressas, anotação à mão, digitação depois. A
pergunta do TCC foi medir — em produtividade e acurácia — o efeito de uma arquitetura progressiva de
automação feita só com software livre: (1) conferência em campo por sistema web em celular, com
sincronização em lotes; (2) pipeline de dados em Python, indicadores, painéis e carga no sistema de gestão
patrimonial (este repositório); (3) RFID UHF como evolução futura. O método combinou um inventário-piloto
cronometrado (26 maio 2026, setor de TI, 266 bens), uma simulação de Monte Carlo com reamostragem
bootstrap dos lotes para projetar o esforço do acervo inteiro, e uma campanha censitária de validação
(18 ago. a 22 set. 2026, 15 dias de campo, quatro servidores).

### O que a pesquisa encontrou

- **Piloto:** 94 bens/hora, 37 s por bem (mediana), 94,4% de concordância entre local físico e cadastro.
  A simulação de Monte Carlo projetou 37,6 h para os 3.518 bens ativos (IC 95%: 30,6–46,6 h).
- **Campanha censitária:** 3.457 bens conferidos (97,4% do acervo ativo) em 28,2 h efetivas — 113 bens/hora
  na média, com **rendimentos fortemente decrescentes**: 185 bens/h nos pavimentos administrativos
  (etapa 1), 114 nos depósitos e áreas técnicas (etapa 2) e 35 na varredura residual dos bens que não
  estavam onde deveriam (etapa 3). Projeção para 100% do acervo: ≈ 31 h, dentro do intervalo do modelo.
- **Divergências de localização:** 569 (16,6%) contra o cadastro que valia durante a campanha. A
  concordância caiu dos 94,4% do piloto (setor de TI, bem acompanhado) para 83,4% no órgão inteiro.
- **O achado mais importante veio depois da coleta:** o órgão passou por uma reestruturação
  administrativa durante o inventário. Setores foram renomeados, fundidos e desmembrados, e o SPW só
  refletiu a nova estrutura ao final. 38 das 91 localizações lidas deixaram de existir com o nome usado
  em campo (1.970 leituras, 57% do total). Ao reconciliar as mesmas leituras com o cadastro atualizado —
  por uma tabela de correspondência derivada automaticamente de onde cada bem passou a figurar — as
  divergências caíram de 569 para 280 (8,1%). **Cerca de metade das "divergências" era o cadastro
  correndo atrás da reorganização, não bem fora do lugar.** Isso foi o que a experiência de campo
  provou: o problema central do inventário público não é achar o bem, é a instabilidade da estrutura
  administrativa e das localizações contra as quais ele é conferido — e só um registro estruturado
  (data, hora, responsável, local físico por leitura) permite reconciliar isso retroativamente sem voltar
  a campo.
- **Carga de validação neste sistema:** as 3.456 leituras com número de tombamento foram aceitas pela
  importação atômica (bem existente, sala do cadastro, integrante, data e conservação válidos); nenhuma
  foi rejeitada, e as 98 salas resultantes coincidiram com as localizações ativas do cadastro. Foi a
  validação de ponta a ponta da arquitetura: dados de quatro operadores, 15 dias e uma reestruturação
  chegaram íntegros ao sistema de gestão sem redigitação.
- **Outros achados:** 29 bens já baixados ou doados ainda estavam fisicamente no órgão (12 em
  depósitos); o cadastro tinha 2.051 baixados e 1.854 doados acumulados (52,6% dos registros); 352 bens
  (10% do acervo móvel) concentram 80% do valor.

### Dificuldades e limitações

- **Não há medição do processo manual.** O tempo do cenário anterior (125 a 188 h) foi estimado a partir
  da literatura (70–80% de redução com automação), não cronometrado. A comparação é indicativa.
- **A extrapolação otimista estava errada.** Ao final da primeira etapa, com 185 bens/h, o acervo inteiro
  parecia caber em 19 h; a campanha levou 28,2 h para 97,4%. Projetar o esforço total a partir dos setores
  fáceis subestimou em quase 40%. O modelo de Monte Carlo do piloto, mais conservador, acertou.
- **A campanha não tirou fotos** (o piloto tirou). Foi decisão operacional para manter o ritmo com equipe
  reduzida; a evidência de inventário ficou restrita a local, estado, responsável e hora.
- **Os 3.457 bens receberam estado "Bom".** A escala não discriminou nada; é limitação de procedimento e
  de parametrização, a corrigir nos próximos ciclos.
- **Produtividade medida por lote de sincronização, não por bem.** A regra de descartar pausas maiores
  que uma hora é uma convenção; dias com poucos lotes produzem números instáveis (10/09: 315 bens/h em
  0,2 h). Marcações de início e fim por bem seriam necessárias para rigor maior.
- **Nomes de pessoas e salas não bateram entre sistemas.** A conferência foi feita no sistema de
  primeira geração; ao migrar para este, os integrantes vinham com nomes diferentes dos usuários
  cadastrados e as salas com os nomes antigos. Foi preciso um de-para de 38 localizações, decidido por
  regra de maioria, com quatro casos ambíguos (setores desmembrados) e um sem correspondência clara.
- **Restaram 91 bens pendentes** (12 em localizações lógicas, como licenças de software amortizadas), e o
  desfecho das 280 divergências (movimentação legítima, erro de cadastro, bem não localizado) ainda não
  foi classificado.

- **Um único órgão.** É pesquisa-ação; a generalização exige cautela, ainda que a solução seja livre,
  conteinerizada e replicável.

## Uso

1. Abra `TermosCFC.exe`. A janela abre em `http://127.0.0.1:12345`.
   **Pesquisa** (lupa no cabeçalho, para quem tem acesso ao acervo): número do bem abre a ficha; texto procura em bens
   (descrição, complemento, localização, centro, pessoa), pessoas e centros de custo. Várias palavras: todas
   têm que bater (`computador GEX-LIC` = computadores do GEX-LIC; o "e" solto é ignorado). Texto simples
   busca "contém"; com `*` o padrão é literal (`GEX*` começa com GEX, `*ITEC` termina com ITEC). Nos
   resultados, centro ou pessoa têm *Ver bens* (lista filtrada) e *Termo*.
   **Processos SEI** (Cadastros → Processos SEI): um vigente por tipo de termo (centro de custo,
   individual, devolução). Sem processo vigente o termo não pode ser copiado nem baixado.
   **Termos emitidos**: cada cópia ou download registra data, processo e a lista de bens daquele
   momento (foto). Na tela do termo aparece o último registro e se entraram/saíram bens desde então
   (termo *desatualizado*). O número do documento SEI pode ser anotado depois, no registro.
   **Atualizar base** guarda o que mudou a cada importação (novos, removidos, movidos, situação) e a
   ficha do bem mostra o histórico dele.
   **Início** é enxuto: até seis atalhos (termo por centro de custo, termo individual, termo de devolução,
   termos emitidos, realizar inventário e Análise), os indicadores permitidos (ativos, valor sem imóveis,
   imóveis, sem centro nem pessoa, termos a emitir, última importação, andamento do inventário) e o card
   *Sobre o patrimônio*. Não tem mais gráficos nem busca no meio da tela — os gráficos ficam na Análise,
   e a busca, na lupa do cabeçalho. Cada usuário vê só os atalhos e indicadores cujas telas ele pode abrir.
   **Análise** filtra bens por qualquer combinação, com seis gráficos (onde está o valor, concentração,
   explorar a base com seletores Dimensão × Medida, entradas por ano, comprado × vale hoje e cobertura de
   termos — `painel.cards_analise`, os mesmos nas duas aparências), os cards de valor não
   informado × valor zero (contados à parte um do outro), *Abrir termo completo* do centro/pessoa quando
   couber — com o aviso *Os filtros desta análise não limitam o termo*, porque o documento sai inteiro —
   e *Exportar .xlsx* (`analise.xlsx`, com todos os bens do filtro, sem o limite de 1000 linhas da tabela
   na tela). A antiga tela **Recorte** passou a se chamar **Análise**; `/recorte` e `/recorte/xlsx`
   continuam funcionando e redirecionam para os novos endereços.
   **Menu** em árvore, recortado pelas funções de quem entrou: Início, Termos de Responsabilidade (grupo),
   Análise, Inventário (grupo), Cadastros (grupo), Textos, Atualizar base, Administração e Ajuda. Grupo sem
   nenhum item permitido não aparece; o grupo da tela aberta já vem expandido e só o item da tela fica
   marcado (o relatório de um evento encerrado não acende o relatório do evento aberto).
   **Ajuda** (`/ajuda`) é o guia do sistema: sumário e seções apenas das funções do usuário, incluindo
   perguntas frequentes. O ícone de interrogação ao lado do título das telas de trabalho abre o guia direto
   na seção correspondente; a própria Ajuda, o login, as telas de erro e os documentos não têm esse botão.
   **Administração › Inventários** (menu Administração, só admin): crie o evento (nome, portaria; nasce
   fechado, salvo marcar "Abrir agora"), abra/feche pela chave — só um aberto por vez; abrir um evento
   fecha o outro automaticamente ("Inventário X aberto; Y foi fechado.") —, finalize (permanente, congela
   os bens) e defina a comissão (qualquer usuário ativo; quem ainda não tem a função Inventário a recebe
   automaticamente ao entrar na comissão), além de excluir e ver o relatório de um evento finalizado.
   A comissão pode ser editada enquanto o evento estiver fechado.
   **Inventário** (menu próprio, tela de conferência): escolha o integrante e leia as plaquetas do evento
   aberto por sala com leitor de código de barras, câmera do celular ou digitação. Bem lido na sala
   cadastrada = localizado; em outra sala = divergente (o cadastro do SPW não muda); não lido = pendente;
   sem cadastro = sobra (com foto). Bem baixado lido fica registrado (continua baixado). Conservação,
   quem usa, observação e foto por bem. Relatório e `.xlsx` por evento. Um evento fechado mostra
   "Inventário fechado" e não aceita leituras até ser reaberto; finalizar é definitivo e congela tudo.
   Cada evento tem **Painel** (KPIs e gráficos por situação, integrante, conservação, andar e sala —
   o andar é o texto antes do primeiro `-` no nome da sala), relatório com filtros/ordenação e `.xlsx`
   com opção *Incluir fotos* (`=IMAGEM`; exige Microsoft 365 — em Excel antigo aparece `#NOME?`). Na sala, é possível marcar bens como localizados em lote
   (plaqueta ilegível) e desmarcar. Ao finalizar, os bens do evento são congelados
   (`inventario_bens_encerrados`): o relatório de um evento finalizado não muda quando a base do SPW
   é atualizada.
   Fotos vão para o bucket R2 configurado em `secrets/.env` (variáveis `R2_*`); sem ele, fotos ficam
   desativadas. Cada bem aceita várias fotos por evento (a sala mostra todas; relatório e `.xlsx` só a
   primeira, com "+N"); a chave no bucket é `<pasta>/<n>-<número do bem>.webp`, com a pasta sendo o nome
   do evento em minúsculas sem acento (ex.: `inventario2026/1-12334.webp`), por isso dois eventos não podem
   ter nomes que gerem a mesma pasta. O cadastro do bem (`/bem`) lista as fotos agrupadas por evento.
   A planilha de cadastros ganha abas `inv_*` para exportar/importar inventários inteiros
   (migração de outros sistemas). No menu, *Inventário* é um grupo com *Eventos* e, quando há
   evento aberto, o próprio evento, *Painel* e *Relatório*.
   **Usuários e funções** (site): entrar com login (ou e-mail, se cadastrado) e senha. O e-mail é opcional e
   único. Cada usuário soma quantas funções quiser — não são perfis excludentes: *Administrador* (tudo:
   usuários, administração de inventários — chave Abrir/Fechar, Finalizar, comissão, excluir —, exclusões
   e importação de cadastros), *Operador* (termos,
   cadastros, textos, atualizar base), *Consulta* (só vê o acervo; não emite termo), *Inventário* (lê bens,
   tira foto e registra sobra nos eventos em que está na comissão) e *Consulta de inventários* (acompanha
   telas, painel, relatório e `.xlsx` de qualquer evento, aberto, fechado ou finalizado, sem poder ler bens). As funções
   se somam: por exemplo, Inventário + Consulta de inventários enxerga todos os eventos, mas só grava leitura,
   foto e sobra no evento da própria comissão. A comissão de cada evento é escolhida pelo administrador em
   Administração › Inventários, entre qualquer usuário ativo; quem ainda não tem a função Inventário a
   recebe automaticamente ao entrar na comissão. A leitura grava o nome de quem está logado.
   A entrada depende do acesso: quem enxerga o acervo cai no **Início**; quem só tem função de inventário é
   levado direto a **Inventário** (`/inventario`), sem lupa de pesquisa, Análise nem termos — nem por URL
   digitada (403). Dentro do módulo as duas funções se separam: quem tem só *Inventário* também não alcança
   painel, relatório nem exportação (403), e enxerga apenas os eventos de cujas comissões participa; quem tem
   *Consulta de inventários* alcança painel, relatório e `.xlsx` de todos os eventos, mas nenhuma ação de
   conferência. Quem tem Inventário e ainda não está em nenhuma comissão vê *Nenhum inventário atribuído a
   você*, sem nome nem total de evento alheio.
   Usuário não é excluído, só inativado. *Nova senha* gera uma senha temporária mostrada uma vez, com troca
   obrigatória no primeiro acesso. Cinco senhas erradas seguidas bloqueiam o login por 15 minutos. O programa
   Windows não pede senha: entra como "Administrador local". Renomear um usuário mantém o nome atualizado na
   comissão do evento aberto (se ele estiver nela); leituras já feitas continuam com o nome antigo.
   Quem vem de uma instalação com os quatro perfis antigos recebe, na migração, exatamente a função do mesmo
   código (*admin*→Administrador, *operador*→Operador, *consulta*→Consulta, *inventariante*→Inventário);
   isso é restrito por identidade, não por nome — usuários homônimos na comissão de um evento não são
   religados automaticamente, e o administrador precisa selecionar as contas certas na tela Comissão de cada
   evento que ainda estiver aberto.
2. **Atualizar base**: envie o export do sistema de patrimônio (`.xlsx`). Só a tabela de bens muda.
   *Exportar bens (formato SPW)* devolve a mesma tabela em `.xlsx`, nas 9 colunas do export — backup reimportável.
3. **Cadastros**: quatro áreas com busca visível, filtros, ordenação e paginação de 10/20/50 registros.
   Em **Centros de custo**, encontre a sigla ou o responsável e use *Editar*; alterar a sigla mantém
   as localizações e referências dos termos. Em **Localizações**, filtre as que estão sem centro,
   vincule-as ou altere o centro de uma ou várias localizações com revisão de origem e destino.
   A seleção em lote vale para a página atual e é limpa ao mudar busca, filtros ou página.
   Em **Pessoas**, use *Editar* para corrigir o nome ou *Ver bens* para consultar um patrimônio antes
   de atribuí-lo. Bem atribuído a pessoa não entra no termo do setor. Em **Processos SEI**, cadastre
   processos e revise o impacto antes de substituir o vigente, encerrar ou excluir.
   Inclusão e edição têm formulários próprios; erros mantêm os dados preenchidos. Salvar e cancelar
   preservam o contexto da lista. Exclusões e remoções de vínculo exigem confirmação; centros com
   bens ativos sob sua guarda e processos com termos registrados mantêm seus bloqueios de exclusão.
4. **Termos**: escolha o centro/pessoa → página do termo → *Copiar para o SEI* ou *Baixar .docx*.
5. **Textos**: os dizeres dos termos (abertura, compromissos, parágrafos, quem recebe a devolução,
   cidade, sigla do órgão) são editáveis no menu Textos, com marcadores como `{nome}` e `{ccustos}`;
   "Restaurar padrão" volta ao texto original.
6. **Planilha de cadastros**: Cadastros → *Exportar cadastros* gera `cadastros.xlsx` (4 abas; quando já
   existe inventário, mais 7 abas `inv_*`). Edite no Excel e importe em *Atualizar base → Importar
   cadastros* — substitui as 4 tabelas inteiras; as abas `inv_*` só são aceitas todas juntas (e então
   substituem o inventário inteiro) ou nenhuma (inventário preservado). A 6ª aba, `inv_bens_encerrados`,
   é o retrato dos bens de cada evento encerrado (gravado no encerramento); é opcional na importação —
   ausente, a tabela é mantida. A 7ª aba, `inv_fotos`, tem as fotos dos bens (evento, número, nfoto, url);
   também é opcional — ausente, uma coluna `foto_url` em `inv_leituras` (planilhas anteriores) vira a
   foto 1 de cada bem. Atenção: diferente de `inv_bens_encerrados`, quando as abas `inv_*` são importadas
   sem `inv_fotos` e sem a coluna `foto_url`, a tabela de fotos fica vazia (as imagens continuam no bucket,
   mas sem referência). A coluna `fotos_seq` de `inv_leituras` é o contador interno das fotos (maior número
   já usado por bem); é opcional na importação. Desmarcar um bem apaga a leitura e esse contador; se o bem
   for lido e fotografado de novo, a numeração recomeça em 1.

Backup = copiar a pasta `dados/`. `dados/segredo.txt` — chave que assina a sessão do navegador, criada
na primeira execução; na web pode vir da variável `TERMOS_SEGREDO`. Na VPS o container cria esse arquivo como root; para rodar o sistema fora do Docker na mesma pasta, defina `TERMOS_SEGREDO` no ambiente ou ajuste o dono do arquivo.

## Desenvolvimento

    python -m venv .venv && .venv/bin/pip install -r requirements.txt
    .venv/bin/pytest
    .venv/bin/python app.py        # http://127.0.0.1:12345 (debug)
    .venv/bin/python main.py       # como o programa: janela (ou navegador, se não houver WebView)

A porta pode ser trocada com a variável `TERMOS_PORTA` (padrão 12345), útil para testar sem conflitar
com outra instância já rodando.

Migração inicial a partir das planilhas antigas: `python importar_planilhas.py acervo.xlsx geral.xlsx`.
Migração de um inventário em andamento vindo de outro sistema: `dados/migrar_evento_2026.py` (uso na docstring;
renomeia integrantes, traduz salas pelo `dados/depara_localizacoes_2026.csv`, preserva leituras já feitas aqui — ou as
descarta com `--descartar-feitas-aqui`, caso de testes — e, com `--gravar`, carrega pela mesma validação tudo-ou-nada da tela).

## Gerar o executável (Windows)

    python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
    scripts\build.bat             # a partir da raiz do projeto

Sai em `dist\TermosCFC\`. Distribua a pasta inteira (zip). Requer o WebView2 Runtime (já vem no
Windows 10/11 atualizados); sem ele o programa abre no navegador padrão.

Copie o `dados\termos.db` já migrado (por exemplo, da máquina onde rodou o `importar_planilhas.py`)
para `dist\TermosCFC\dados\` antes de distribuir; sem isso o programa abre com a base vazia.

### Observações

Os parágrafos do termo por centro de custo não carregam mais 4 espaços em branco no início (era um
resíduo de indentação do código antigo) — confira o `.docx` gerado.

## Servir na web (Docker)

O mesmo código roda em `https://patrimonio.sistemascfc.org`, num container nesta máquina, atrás do nginx do host
(container em `127.0.0.1:12012`, Certbot). O login é do próprio sistema (`TERMOS_LOGIN=1` no `compose.yml`).

    docker compose up -d --build   # (re)constrói e sobe; dados em ./dados (termos.db, timbrado.docx)
    docker compose logs -f         # acompanhar
    docker compose exec web python usuarios.py criar-admin antonio "Antônio Sousa" antonio@cfc.org.br   # primeiro administrador (ou redefinir a senha de um admin)

### Design das telas: DSGov ou Tabler

A variável `TERMOS_DESIGN` escolhe a aparência; rotas, banco, permissões e robôs são os mesmos nos dois.

- sem a variável (ou `TERMOS_DESIGN=dsgov`): telas de `templates/` (DSGov, padrão);
- `TERMOS_DESIGN=tabler`: o sistema procura cada tela primeiro em `templates/tabler/` (Tabler.io 1.5.1, arquivos em
  `static/tabler/`, sem CDN) e só cai em `templates/` se ela não existir lá.

Para trocar o design de um site: pôr ou tirar `TERMOS_DESIGN: tabler` em `environment` do compose e rodar
`docker compose up -d` (reinicia o container; não precisa trocar de branch nem mexer em código). A prévia em
`https://patrimonio.analisedados.online` roda o Tabler pelo `compose.previa.yml` (worktree `/home/ToNiauM/ativos/docker/termos-tabler`,
container `termos-tabler` em `127.0.0.1:12014`, só o site, sem robô, com uma cópia do banco em `dados-previa/`).
Os testes da camada Tabler estão em `tests/test_tabler*.py`; a suíte antiga verifica o markup do DSGov.

A casca DSGov segue o padrão da **família de sistemas do CFC** (padrão DSGov, `references/layout.md` § Família CFC;
referência viva: o PCA): `templates/base.html` inclui, na ordem do padrão DSGov, os partials Jinja de `templates/dsgov/`
(`_skiplink`, `_header`, `_menu`, `_breadcrumb`, `_mensagens`, `_footer`), que reproduzem o HTML dos partials Django do
padrão DSGov. Cabeçalho em uma linha (☰ + "Sistema de Patrimônio"/unidade, pesquisa cinza no meio, botão-pílula do usuário
com Meus acessos, Trocar senha e Sair por POST com CSRF); logo do CFC (`static/img/logo-cfc.png`, o do padrão DSGov) no alto
do menu; pastas do menu só abrem e fecham (`href="javascript:void(0)"`, o sistema não tem CSP); página corrente
`active` + `aria-current`; rodapé com parágrafo institucional e links. `static/dsgov/css/dsgov.css` é cópia
byte-idêntica do padrão DSGov (ao atualizar o padrão DSGov, copie de novo; `tests/test_casca_dsgov.py` compara quando o padrão DSGov está
instalada) e as regras próprias ficam em `static/css/patrimonio.css`. O `static/dsgov/js/dsgov.js` continua uma
versão própria (blocos do projeto marcados no cabeçalho do arquivo). Duas regras de markup que o core 3.7.0 impõe,
guardadas por teste: mensagem `.br-message` (e botão `.br-button`) escondida usa a classe `d-none`, nunca o atributo
`hidden` (o `display` do componente vence o `hidden`); todo `.br-table` leva `<div class="table-header"></div>`, mesmo
vazio (sem ele o `BRTable` tira a tabela da página). `static/logo.png` continua sendo o logo da casca Tabler.

Paridade com o Tabler (as quatro ondas feitas em 23/10/2026):
a busca do `br-table` (macro `cabecalho_tabela`) filtra as linhas sem acento e sem maiúsculas e o rodapé conta
"N registro(s)" / "N de M registro(s)" — `prepararBusca` em `static/js/tabelas.js`, só na aparência DSGov (no Tabler
quem filtra é o `astra.js`). Acabamentos: pré-título acima do `h1` (macro `pre_titulo`), barra `<progress
class="dsgov-barra">` no inventário corrente, salas do evento em blocos no celular (`#dados-salas`), Salvar fixo em
Textos (`#salvar-textos`), sumário "Nesta página" fixo na Ajuda (`#sumario-ajuda`), campo de pesquisa no corpo da
Pesquisa, ícones na Importação e em Atualizar base, botões no `card-footer` dos formulários de cadastro, comissão e
exclusão de inventário e e-mail enviado como `br-tag` em Termos emitidos. As regras de CSS novas usam id e atributo
(nenhuma classe fora do DS, para o verificador do padrão DSGov). A trilha curta do Tabler no celular não foi copiada: o
`br-breadcrumb` do core já troca para o tipo especial abaixo de 575px. O painel "Personalizar aparência" e o modo
escuro ficam só no Tabler (decisão do usuário). `tests/test_paridade_dsgov.py` guarda o markup e os ganchos.

(Análise, 23/10/2026): a tela Análise do DSGov usa os seis cards de `painel.cards_analise`, como o Tabler; o
conjunto antigo (`painel.cards_graficos`, um card por dimensão) saiu do código. A macro `grafico` (`_macros.html`)
aceita `destaque` (frase em negrito acima do gráfico), `seletores` (um `br-select` da macro `select` por seletor,
envolvido em `data-grafico-seletor`) e `variantes` (um `<script type="application/json">` e uma tabela "Ver dados" por
combinação, id `g-explorar--ccusto--valor`). `static/js/analise.js`, carregado só na Análise depois do
`echarts-dsgov.js` (cópia congelada do padrão DSGov, não editada), monta esses gráficos no tema `dsgov`: tooltip
`"moeda"`/`"percentual"`, eixos abreviados (12 mil, 1,5 mi), total no furo da rosca que acompanha a legenda,
paleta categórica oficial no lugar da do Tabler (`graficos.CORES_CATEGORICA` é o espelho), legenda paginada sem
sobrepor o desenho e troca de variante sem recarregar (refaz o gráfico na largura atual). Ele marca os gráficos com
`data-dsgov-grafico`, então o `montar()` do padrão DSGov não os monta de novo. O verificador do padrão DSGov acusa a `<script>` do
`analise.js` (regra CDN: o verificador não reconhece `url_for` do Flask e acusa toda `<script>`/`<link>` do
projeto, inclusive as da lista fixa; o `analise.js` está fora da lista, como `tabelas.js` e `menu-estado.js`).

(sala do inventário, 23/10/2026): `templates/inventario_sala.html` tem o desenho do Tabler com componentes do
padrão DSGov — três seções num `br-tab` com contador (`data-counter`; "verificar" em Divergentes, bolinha `br-tag status` no
celular), faixa de leitura presa no topo (`#faixa-leitura`, `position: sticky` abaixo do cabeçalho fixo, que o
`sala.js` mede em `--sala-topo`), busca com "N de M", caixa "Todos", Lista (`br-list`) ou Quadros (`br-card` com
`br-avatar`: primeira foto ou ícone da categoria) lembrada em `localStorage` (`inventario.sala.visao`, com
try/catch), selos `br-tag`, menu ⋮ (`br-list role="menu"` + `data-toggle="dropdown"`, instanciado pelo `sala.js`
com o `Dropdown` do core sem trocar o ícone; `data-dsgov-init` faz o `dsgov.js` pular), ficha do bem em
`br-scrim-util` + `br-modal dsgov-modal-largo` (contexto `fichas`, o mesmo do Tabler), barra do lote presa embaixo só
com bens marcados (`#barra-lote`) e divergentes nas seções, sem a tabela "Trazidos". O comportamento mora em
`static/js/sala.js` (lógica do JS inline do Tabler, carregado só na sala; mais um erro CDN no verificador, como o
`analise.js`): mostrar/esconder sempre por `d-none`, cada bem com duas cópias (`data-copia="lista"|"grade"`), fotos
de bem por um só `<input type="file" id="foto-bem">` cujos rótulos são o "Nova foto" do menu e o "Adicionar foto" da
ficha. Rotas e POSTs não mudaram (a ficha exclui foto pelo pedido JSON de `foto_excluir`). O formulário de sobra
leva o `<p class="text-base">` do HTML canônico do `br-upload`: sem ele o `BRUpload` do core compara o irmão
seguinte (null) com `document.querySelector(".text-base")` (null) e faz `null.style` ao anexar a foto.
`tests/test_sala_dsgov.py` guarda a tela.

O `dsgov.js` do repositório **não** é a cópia do padrão DSGov e não deve ser sobrescrito por ela: (1) tem o bloco próprio que
devolve o id do servidor aos `.br-card` depois do `BRCard` do core (âncoras da Ajuda; `tests/test_ajuda.py` guarda);
(2) a versão atual do padrão DSGov acrescenta ordenação por clique no `<th>`, coluna de ações fixa, modal com rolagem,
composer de chat e painel recolhível — a ordenação duplicaria a de `tabelas.js` (dois ícones e dois cliques por
cabeçalho). O resto do arquivo é igual à versão do padrão DSGov que o originou.

Publicação da Fase 4 (uma vez): subir o container; criar o administrador pelo comando acima; entrar e criar os
usuários da comissão do evento aberto com **exatamente** os nomes já gravados nas leituras (Inventário → evento →
*Comissão* mostra quem já tem leituras); remover `auth_basic` e `auth_basic_user_file` do vhost
`/etc/nginx/conf.d/patrimonio.sistemascfc.org.conf` e recarregar (`nginx -t && systemctl reload nginx`).
Enquanto o `auth_basic` ficar, o site pede as duas senhas, sem prejuízo.

`Dockerfile` (alvos `web` e `robo`), `compose.yml` e `.dockerignore` são só do site; o programa de desktop não os
usa. O vhost fica em `/etc/nginx/conf.d/patrimonio.sistemascfc.org.conf`. Backup continua sendo copiar a pasta
`dados/`.

### Emissão no SEI

O botão **Emitir Termo no SEI** (página do termo) e **Atualizar com SPW** (Atualizar base) enfileiram pedidos em
`robo_pedidos`; quem atende é `atender_pedidos.py`, rodando **dentro do container `robo`** (`compose.yml`,
alvo `robo` do `Dockerfile`), que tem Playwright e xlrd por cima da imagem do site:

    docker compose up -d --build   # constrói as duas imagens (web e robo) e sobe os dois containers
    docker compose logs -f robo    # acompanhar o trabalhador (pedidos atendidos, erros)

O container `robo` é permanente (`restart: unless-stopped`), sem porta exposta; monta `./dados` (banco, logs,
capturas de erro) e `./secrets` (somente leitura). Sem ele de pé, o site continua funcionando: o pedido fica
"aguardando a vez" e a tela avisa depois de 2 minutos.

Segredos em `secrets/sei.env` (`SEI_LOGIN_URL`, `SEI_ORGAO`; chmod 600); usuário, senha e unidade são os cadastrados
por quem emitiu em *Meus acessos* (ver "Acessos por usuário (SEI e SPW)" abaixo). No SEI, crie à mão
um bloco de assinatura por unidade, com o nome exato `Termos {UNIDADE}` (ex.: `Termos GECONT`); o sistema só inclui o
documento — disponibilizar o bloco continua sendo feito por vocês. Em Cadastros, informe a "Unidade no SEI" das pessoas
que recebem termo individual (e a exceção no centro de custo cuja sigla difere da unidade do SEI). Em Textos, o nome do
tipo de documento por tipo de termo.

Diagnóstico: `dados/robo_pedidos.log` (exceções), `dados/sei/erro.png` (tela do SEI no erro), tabela `robo_pedidos`.

### Acessos por usuário (SEI e SPW)

As senhas de cada operador ficam cifradas (Fernet, `cofre.py`) no banco, nunca em texto puro. Uma vez, gere a
chave e guarde-a:

    .venv/bin/python -c "import cofre; print(cofre.gerar_chave())"   # cole o resultado em secrets/chaves.env
    # secrets/chaves.env:
    # CHAVE_SENHAS=...
    chmod 600 secrets/chaves.env

As duas imagens (`web` e `robo`) montam `./secrets` (somente leitura). **`scripts/backup.sh` não copia `chaves.env`** —
ele só leva `termos.db` para o bucket R2; guarde a chave à parte, à mão, em outro lugar (por exemplo, no
gerenciador de senhas do administrador). Sem ela as senhas cifradas em `termos.db` são inúteis; quem restaura um
backup sem a chave junto precisa pedir que cada operador cadastre o acesso de novo. Com isso, `secrets/sei.env`
fica só com `SEI_LOGIN_URL` e `SEI_ORGAO`.

Cada operador cadastra o próprio acesso em **Meus acessos** (no botão do usuário, no cabeçalho, `/meus-acessos`): ao SEI (usuário,
senha e sigla da unidade — é nessa unidade e em nome dessa pessoa que os termos nascem no SEI, e é lá que o bloco
`Termos {SIGLA}` precisa existir) e ao SPW (usuário e senha — usado por *Atualizar com SPW* pelo site). Sem acesso
cadastrado, o site recusa antes de enfileirar ("Cadastre seu acesso ao SEI em Meus acessos para emitir."/"...ao SPW
... para atualizar."). Ao trocar a senha no SEI ou no SPW, atualize na mesma tela (deixar a senha em branco mantém
a atual). O administrador, na lista de usuários, só vê se há acesso cadastrado (coluna "Acessos") e pode apagá-lo
(*Apagar acessos*) — nunca vê a senha.

O cron diário (`scripts/atualizar_base.sh`) continua usando `secrets/spw.env` completo, sem depender de acesso de
ninguém (ver "Robô do SPW" abaixo).

### Robô do SPW

`importar_spw.py` entra no SPW, exporta a relação de bens (Excel/Detalhado), compara com a última execução e,
se mudou, importa como o upload de Atualizar base faria. Roda dentro do container `robo` (acima), uma vez por dia
útil (seg-sex) num horário sorteado entre 7h e 7h30, e registra cada execução em `robo_execucoes`: o card
"última importação" do Início mostra `robô ok`/`robô falhou` e Atualizar base lista as últimas execuções.
Segredos em `secrets/spw.env` (`SPW_USUARIO`, `SPW_SENHA`,
`SPW_LOGIN_URL`, `SPW_CONSULTA_URL`, chmod 600). Pelo site, *Atualizar com SPW* usa a credencial de quem clicou
(ver "Acessos por usuário" acima); o cron continua com `spw.env`.

`scripts/atualizar_base.sh` não roda mais o robô diretamente: ele entra no container já de pé com `docker compose exec`
(e sai com um aviso claro se o `robo` não estiver rodando):

    scripts/atualizar_base.sh            # docker compose exec -T robo python importar_spw.py; sai 0/1
    scripts/atualizar_base.sh --teste    # mesma coisa numa cópia em dados/robo-teste, sem tocar na base real

Crontab (`crontab -e`, usuário dono de `dados/termos.db`); o script já grava em `dados/robo_spw.log` (o container
`robo` precisa estar de pé — `docker compose up -d` — para o cron funcionar):

    0 7 * * 1-5 sleep $(shuf -i 0-1800 -n 1); /home/ToNiauM/ativos/docker/sistema-inventario/scripts/atualizar_base.sh >/dev/null 2>>/home/ToNiauM/ativos/docker/sistema-inventario/dados/robo_spw.log

**reCAPTCHA no login (desde 07/10/2026).** O login do SPW passou a ter o "Não sou um robô" do Google. O robô entra
com o SeleniumBase em CDP puro (`sb_cdp`: Google Chrome sem chromedriver, numa tela virtual Xvfb), que preenche
usuário e senha e marca a caixa; só depois o Playwright se conecta ao mesmo Chrome (`connect_over_cdp`) para a
consulta e o download. Quem decide se a caixa basta é o Google: quando ele abre o desafio de imagens, o robô para
**antes** de clicar em Entrar (não gasta tentativa de login) e o Início mostra "o reCAPTCHA do login do SPW não
liberou"; aí vale Atualizar base com o export baixado à mão (abrir o `.xls`, apagar as linhas acima de "Número Bem"
e salvar como `.xlsx`, que é o que o upload aceita). Para o Google desconfiar menos, o perfil do Chrome
fica guardado entre execuções em `dados/spw/chrome-perfil/` e o cron roda uma vez por dia, em minuto sorteado (era
de 2 em 2 horas). A saída garantida é a TI do CFC liberar o robô do reCAPTCHA.

O robô não importa se o export vier com menos de 90% dos bens da base (protege contra export vazio ou truncado);
nesse caso registra erro e a baixa em massa, se for real, passa por Atualizar base. Um upload manual entre
execuções fica valendo até o SPW mudar: o robô compara o export com a própria execução anterior, não com a base.

Diagnóstico: `dados/robo_spw.log` (uma linha por execução), `dados/spw/erro.png` (tela do SPW no momento do erro)
e `dados/spw/erro.html` (HTML da mesma página, para achar os seletores novos).
Se o SPW mudar o layout, os seletores ficam em `baixar_export`; o teste assistido (abaixo) repete os da exportação
em `scripts/spw_assistido.py`.

`requirements-robo.txt` (Playwright, SeleniumBase, xlrd) continua no repositório: a imagem `robo` não o usa (as dependências
estão fixas no `Dockerfile`).

### Teste assistido do SPW

`scripts/spw_assistido.sh` roda o robô com você olhando a tela dele pelo navegador: se o Google pedir o desafio de
imagens no login, você resolve e o robô continua sozinho (entra, exporta pela consulta e valida o arquivo). Serve
para testar o SPW à mão e como plano B quando o cron cai no desafio.

1. No seu computador, abra o túnel e deixe a janela aberta: `ssh -L 16080:127.0.0.1:6080 <usuário>@<servidor>`
   (se o Windows recusar a porta com `Permission denied`, troque o 16080 por outra).
2. No servidor, na pasta do sistema: `scripts/spw_assistido.sh` só testa (baixa em `dados/spw/assistido.xls` e
   valida; a base não muda); `scripts/spw_assistido.sh --importar` também importa se der certo, pelo mesmo caminho
   do robô (mesmas conferências, registro em `robo_execucoes`, aparece no Início).
3. Quando aparecer "Tela pronta", abra `http://localhost:16080/vnc.html?autoconnect=true&resize=scale`, confira o
   login do SPW e aperte Enter no terminal. Se vier o desafio de imagens, resolva e clique em Verificar (não clique
   em Entrar). Ctrl+C cancela; sem Enter em 10 min, o script desiste sozinho (ele segura o mesmo lock do robô, que
   também atende a emissão no SEI).

Por baixo: um container avulso da imagem `robo` com o Chrome do robô (mesmo perfil, `dados/spw/chrome-perfil`)
numa tela virtual (Xvfb), transmitida por VNC (x11vnc, só dentro do container) e servida no navegador pelo noVNC
(websockify) em `127.0.0.1:6080` do servidor, alcançável só pelo túnel. Os pacotes do VNC são instalados na hora
(cerca de 40 s), então a imagem do robô não muda. Usa o mesmo lock do robô (`dados/robo.lock`).

### Limpar o banco antes de entrar em produção

    scripts/apagar_termos_emitidos.sh   # só termos emitidos, seus bens e a fila de emissão (numeração recomeça do 01)
    scripts/zerar_banco.sh              # histórico de cargas (importações, execuções do robô) e emissões — mantém bens,
                                  # atribuições, pessoas, centros de custo, localizações, processos, textos, usuários
    scripts/zerar_banco.sh --inventario # idem, apagando também o inventário (eventos, leituras, fotos, sobras)
    scripts/zerar_inventario.sh         # eventos de inventário inteiros, escolhidos na lista (ou --ALL), COM as
                                  # fotos no bucket R2: antes baixa uma cópia delas em /opt/backups/termos/
                                  # fotos-inventario-<data>/ e para sem apagar nada se alguma não baixar;
                                  # --manter-fotos apaga só o banco; roda a parte do bucket no container web

Os três listam o que vai apagar, pedem confirmação (ou `--sim`) e deixam uma cópia em `dados/termos-antes-de-*.db`.
Documentos já criados no SEI não são tocados. A numeração dos termos é automática: por unidade do SEI, por tipo de
termo (centro de custo, individual, devolução) e por ano.

## Arquivos

| Arquivo | Função |
|---|---|
| `app.py` | rotas Flask |
| `app_cadastros.py` | navegação, formulários e revisão das alterações de cadastros |
| `db.py` | esquema, importação, consultas, cadastros |
| `termos_html.py` | corpo HTML dos termos (padrão gelic; tabelas 90 %) |
| `textos.py` | textos padrão dos termos e marcadores |
| `Script_Termo_Individual.py`, `Termo_de_Responsabilidade.py`, `termo_devolucao.py` | geradores `.docx` |
| `config.py` | pasta de dados (`TERMOS_DADOS` sobrepõe) |
| `main.py`, `scripts/build.bat` | programa de desktop e build |
| `Dockerfile` | dois alvos: `web` (site) e `robo` (`FROM web`, + Playwright e xlrd, atende `robo_pedidos`) |
| `compose.yml` | serviços `web` (site, porta 12012) e `robo` (trabalhador da fila, sem porta) |
| `templates/`, `static/dsgov/` | telas DSGov 3.7.0 (offline); a casca (`templates/base.html` + `templates/dsgov/_*.html`) segue a família CFC do padrão DSGov |
| `static/css/patrimonio.css` | as poucas regras CSS próprias do sistema na casca DSGov (o `static/dsgov/css/dsgov.css` é cópia byte-idêntica do padrão DSGov) |
| `painel.py`, `graficos.py` | cards de gráfico (ECharts embutido, tema DSGov) |
| `static/js/analise.js` | montagem dos gráficos da Análise na casca DSGov (formatos, total da rosca, seletores de variante) |
| `inventario.py`, `fotos.py`, `app_inventario.py` | módulo de inventário (dados, fotos no R2, rotas) |
| `usuarios.py`, `app_usuarios.py` | usuários, senhas, matriz de permissões e telas de login/usuários |
| `app_admin.py` | Tela Administração (aba Inventários; a aba Usuários é `app_usuarios.py`) |
| `scripts/apagar_termos_emitidos.sh`, `scripts/zerar_banco.sh`, `scripts/zerar_inventario.sh` | limpeza do banco antes da produção (ver acima) |
| `cofre.py` | cifra (Fernet) das senhas do SEI e do SPW guardadas por usuário; chave em `secrets/chaves.env` |
| `scripts/atualizar_base.sh` | Chama o robô do SPW dentro do container `robo` via `docker compose exec` (`--teste` usa uma cópia da base); o cron chama o mesmo script |
| `importar_spw.py` | Robô do SPW: exporta, converte e importa os bens (roda no container `robo`, por cron) |
| `scripts/spw_assistido.sh`, `scripts/spw_assistido.py` | Teste assistido do SPW: o robô com a tela visível no navegador (noVNC + túnel SSH) para resolver o desafio de imagens à mão; `--importar` importa se der certo |
| `requirements-robo.txt` | Não é usado pela imagem `robo` (dependências fixas no `Dockerfile`) |
| `robo_sei.py` | Robô do SEI: login, cria o documento no processo e inclui no bloco de assinatura |
| `atender_pedidos.py` | Trabalhador do container `robo`: atende a fila `robo_pedidos` (emissão no SEI e atualização com o SPW) |
| `segredos.py` | Lê os arquivos `secrets/*.env` (SPW, SEI) |

## Documentação

O manual operacional do Patrimônio, com o passo a passo do sistema, está em `manual/` e é publicado em <https://toniaum.github.io/sistema-patrimonio/>.

## Licença

[AGPL-3.0](LICENSE). Copyright © 2026 Antônio Rodrigues de Sousa Júnior. Os dados do acervo não fazem parte do repositório.
