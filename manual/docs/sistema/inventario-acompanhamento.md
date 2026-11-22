---
title: "Inventário: acompanhamento"
description: Acompanhar qualquer inventário pelo painel, pelo relatório com filtros e pela planilha, sem conferir bens.
area: sistema
order: 8
status: review
lastReview: "2026-10-23"
systems:
  - Sistema de Patrimônio
procedureId: "sistema:inventario-acompanhamento"
---

# Inventário: acompanhamento

!!! info "Informações do procedimento"

    **Status editorial:** Em revisão · **Última revisão:** 23/10/2026 · **Sistemas envolvidos:** Sistema de Patrimônio

<div class="checklist-controls" data-procedure-id="sistema:inventario-acompanhamento" role="region" aria-label="Controles do checklist">
<div class="checklist-actions">
<button type="button" class="md-button checklist-print-button" aria-label="Imprimir ou salvar este procedimento como PDF">Imprimir</button>
<button type="button" class="md-button checklist-clear-button" aria-label="Limpar progresso do checklist deste procedimento">Limpar checklist</button>
<span class="checklist-progress" aria-live="polite"></span>
</div>
<p class="checklist-disclaimer">Marcações salvas só neste navegador. Elas não constituem registro oficial nem histórico auditável.</p>
</div>

## Objetivo

Acompanhar o andamento de um inventário (aberto, fechado ou finalizado) e extrair os resultados: quantos bens
foram localizados, quais estão divergentes ou não localizados, quem leu o quê, conservação e fotos.

## Quem pode

**Consulta de inventários** e **Administrador** — em todos os eventos. A função Consulta de inventários não
lê bens; quem tem também a função Inventário lê só nos eventos da própria comissão.

## Antes de começar

- [ ] Ter a função Consulta de inventários (ou Administrador).

## Acompanhar

<div class="steps" markdown>

1. **Abra Inventário › Eventos**

    No alto, o inventário corrente com os números do andamento e os botões **Salas** e **Relatório**; abaixo,
    os **outros inventários** (fechados e finalizados), cada um com o botão do relatório.

    ![Tela Inventário para a Consulta de inventários: o evento aberto e a lista Outros inventários.](img/a01-acompanha-inicio.png)

    ![Menu da Consulta de inventários: Eventos, o inventário aberto, Painel, Relatório e Ajuda.](img/a02-menu-acompanha.png)

2. **Para ver as salas, clique em Salas**

    A tabela mostra o andamento por sala. O aviso azul lembra que você pode consultar, mas não ler bens; o
    olho de cada linha abre a sala em modo consulta: as abas Pendentes, Divergentes e Localizados, a busca e
    a ficha de cada bem (menu ⋮ › Detalhes, com o cadastro, a leitura e as fotos) ficam disponíveis; leitura,
    lote e fotos ficam desligados.

    ![Salas do evento em modo consulta, com o aviso Você não faz parte da comissão deste evento.](img/a03-evento-consulta.png)

    ![Sala em modo consulta: campo de leitura desligado e a mensagem Somente consulta.](img/a04-sala-consulta.png)

3. **Abra o Painel**

    Cartões com bens no escopo, localizados (com o percentual), divergentes, pendentes, sobras e salas
    iniciadas, e gráficos por situação, por integrante, por conservação, por andar e por sala. Clicar num
    gráfico abre o relatório já filtrado. Em evento finalizado, os números ficam **congelados** no
    encerramento.

    ![Painel de um inventário finalizado, com os cartões e os primeiros gráficos.](img/a05-painel.png)

    ![Painel: gráficos de situação, leituras por integrante e conservação informada.](img/a06-painel-graficos.png)

4. **Abra o Relatório e aplique os filtros**

    Filtre por sala, situação (localizado, divergente, não localizado), integrante, conservação, com ou sem
    foto e por texto (número, descrição, quem usa, observação). Clique nos títulos das colunas para ordenar.
    A miniatura da foto abre a foto ampliada.

    ![Relatório do inventário com os filtros, os botões Aplicar, Limpar, Incluir fotos e Exportar .xlsx, e a lista de bens.](img/a07-relatorio.png)

    ![Relatório filtrado pela situação Divergente.](img/a08-relatorio-filtrado.png)

5. **Para levar ao Excel, clique em Exportar .xlsx**

    A planilha segue os filtros aplicados. Marque **Incluir fotos** para trazer as fotos dentro da planilha
    (exige o Excel do Microsoft 365; no Excel antigo aparece `#NOME?`).

</div>

## O que acontece depois / onde confere

- Os números do Painel, do Relatório e da lista de salas são os mesmos.
- Evento finalizado não muda mais, mesmo quando a base de bens é atualizada.

## Erros comuns e mensagens

| Situação | Explicação |
|---|---|
| *Relatório pesado. N fotos no filtro* | O `.xlsx` com fotos pode demorar a abrir; filtre mais ou exporte sem fotos. |
| `#NOME?` nas fotos da planilha | O Excel não é o Microsoft 365; exporte sem fotos. |
| Não vejo Painel nem Relatório | A sua função é só Inventário; peça a Consulta de inventários. |
