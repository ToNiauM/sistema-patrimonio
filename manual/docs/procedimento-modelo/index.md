---
title: Procedimento modelo patrimonial
description: Gabarito de referência para procedimentos patrimoniais. Demonstra a estrutura esperada — frontmatter, objetivo, pré-requisitos, passos, capturas, alertas, resultado e referências.
---

# Procedimento modelo patrimonial

!!! note "Nota"

    **Este é um gabarito copiável**, não um procedimento operacional real. Copie este arquivo ao criar um novo procedimento e preencha com o conteúdo real.

## Como usar este gabarito

1. Crie uma pasta dentro da área correspondente em `manual/docs/`, no formato `area/procedimento/`.
2. Copie este arquivo como `index.md` dentro da nova pasta.
3. Preencha a **frontmatter** (os campos entre `---`) com os metadados do procedimento.
4. Substitua o conteúdo de cada seção pelo texto operacional real.
5. Coloque as capturas de tela numeradas em `imagens/` dentro da mesma pasta.
6. Execute `mkdocs build --strict` (dentro de `manual/`) para verificar se os links, as imagens e a estrutura estão corretos, e inclua o procedimento no `nav:` do `manual/mkdocs.yml`, na área correspondente.

---

## Frontmatter obrigatória

Todo procedimento real deve incluir os seguintes metadados no cabeçalho do arquivo:

```yaml
---
title: Nome do procedimento
description: Resumo em uma frase do que o procedimento faz.
area: slug-da-area
order: 1
status: review
lastReview: "AAAA-MM-DD"
systems:
  - SBP
  - SEI
procedureId: "area:nome-do-procedimento"
---
```

| Campo | Descrição | Valores aceitos |
|-------|-----------|-----------------|
| `title` | Título visível na página e no menu | Texto livre |
| `description` | Resumo para busca e meta descrição | Texto livre |
| `area` | Slug canônico da área operacional | `entrada`, `movimentacao-transferencia`, `desfazimento-baixa`, `depreciacao`, `inventario`, `termos-relatorios`, `processos-sei` |
| `order` | Ordem de exibição dentro da área | Número inteiro (1, 2, 3…) |
| `status` | Estado editorial | `complete` (Completo), `partial` (Parcial), `review` (Em revisão) |
| `lastReview` | Data da última revisão | Data no formato `"AAAA-MM-DD"` (entre aspas) |
| `systems` | Sistemas utilizados no procedimento | Lista com `SEI`, `SBP`, `SGA` |
| `procedureId` | Identificador único no formato `area:nome` | Texto sem espaços, ex: `entrada:incorporar-bem` |

!!! warning "Cuidado"

    A data em `lastReview` deve ficar **entre aspas** no arquivo. Sem as aspas, o YAML interpreta `2026-06-25` como uma subtração (2026 − 6 − 25).

---

## Estrutura do conteúdo

### Checklist automático

Os **Pré-requisitos** (escritos como `- [ ]`) e os **Passos** (dentro de `<div class="steps" markdown>`) viram automaticamente caixas de verificação interativas com persistência local. Para ativar, copie o bloco de informações do procedimento e o bloco `checklist-controls` abaixo e posicione-os logo após o título:

```md
!!! info "Informações do procedimento"

    **Status editorial:** Em revisão · **Última revisão:** DD/MM/AAAA · **Sistemas envolvidos:** SBP, SEI

<div class="checklist-controls" data-procedure-id="area:nome-do-procedimento" role="region" aria-label="Controles do checklist">
<div class="checklist-actions">
<button type="button" class="md-button checklist-print-button" aria-label="Imprimir ou salvar este procedimento como PDF">Imprimir</button>
<button type="button" class="md-button checklist-clear-button" aria-label="Limpar progresso do checklist deste procedimento">Limpar checklist</button>
<span class="checklist-progress" aria-live="polite"></span>
</div>
<p class="checklist-disclaimer">Marcações salvas só neste navegador. Elas não constituem registro oficial nem histórico auditável.</p>
</div>
```

O `procedureId` deve ser o mesmo valor declarado na frontmatter do procedimento. As marcações ficam isoladas por procedimento — marcar itens em um procedimento não afeta outro.

!!! note "Nota"

    O aviso exibido pelo componente ("Marcações salvas só neste navegador...") é proposital e obrigatório. Ele informa ao usuário que o checklist é local e não constitui registro oficial.

### Objetivo

Descreva em um parágrafo curto **quando** este procedimento deve ser utilizado, **qual problema ele resolve** e **qual resultado ele produz**. Evite termos técnicos sem explicação — o leitor pode não ter experiência prévia.

**Exemplo:** Use este procedimento quando for necessário incorporar um bem móvel adquirido por compra ao patrimônio do órgão. O resultado é o registro do bem no SBP com número de tombamento gerado.

### Pré-requisitos

Antes de iniciar, verifique se você possui:

- [ ] Acesso ao sistema SBP com perfil de **Registrador de Bens**.
- [ ] Nota fiscal ou documento equivalente que comprove a aquisição.
- [ ] Número do processo SEI de aquisição (se aplicável).
- [ ] Aprovação do responsável pelo setor para realizar o registro.

!!! warning "Cuidado"

    Se você não tiver o perfil adequado no sistema, não avance. Solicite o acesso ao setor de TI antes de iniciar o procedimento.

### Passos

Envolva a lista numerada dos passos em `<div class="steps" markdown>` … `</div>` (com uma linha em branco depois da abertura e antes do fechamento) e recue o conteúdo de cada passo em 4 espaços. Cada passo pode ter uma captura, texto explicativo e alertas.

<div class="steps" markdown>

1. **Ação principal** — descrição do que fazer e onde.

    ```md
    ![Captura demonstrativa 1: texto alternativo descrevendo a tela](./imagens/1_descricao.png)
    ```

    !!! tip "Dica"

        Dica opcional para agilizar ou evitar erro comum neste passo.

2. **Próxima ação** — siga a sequência lógica do fluxo.

    ```md
    ![Captura demonstrativa 2: texto alternativo](./imagens/2_descricao.png)
    ```

3. **Continue** — adicione quantos passos forem necessários.

    !!! note "Nota"

        Observação explicativa sobre campo, formato ou exceção.

</div>

!!! danger "Perigo"

    Alertas de perigo ou ações que podem causar perda de dados.

> **Sobre as capturas:** use o formato `N_descricao.ext` (ex.: `1_tela-login.png`, `2_formulario-bem.jpg`). O número inicial do arquivo corresponde ao passo. Os exemplos acima aparecem como blocos de código apenas para demonstrar a sintaxe — em um procedimento real, escreva a linha `![alt](./imagens/N_descricao.png)` diretamente (sem o bloco de código) para que a imagem seja renderizada.

### Resultado esperado

Ao concluir este procedimento você terá:

- [ ] Item ou documento gerado.
- [ ] Próximo passo ou ação pendente.

**Como confirmar:** Descreva como verificar se o resultado foi alcançado.

### Referências

- Manuais, normas ou links úteis.
- Instruções normativas relacionadas.
- Processos ou documentos de referência.

---

## Convenções editoriais

- Use linguagem direta e voz ativa: "Acesse o sistema", não "O sistema deve ser acessado".
- Explique siglas na primeira menção: **SBP** (Sistema de Bens Patrimoniais).
- Prefira listas de verificação (`- [ ]`) nos pré-requisitos e checklists.
- Use admonitions para destacar: `!!! tip "Dica"` (dica), `!!! note "Nota"` (observação), `!!! warning "Cuidado"` (cuidado), `!!! danger "Perigo"` (perigo).
- Limite cada passo a uma captura. Se precisar de mais telas, divida o passo.
- Mantenha o Tom de respeito e clareza — o leitor pode estar executando o procedimento pela primeira vez.
