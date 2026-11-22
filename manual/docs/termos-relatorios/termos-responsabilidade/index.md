---
title: Emissão de termo de responsabilidade
description: Atualizar a base do acervo a partir do relatório gerencial do SBP e emitir os termos de responsabilidade por unidade organizacional.
area: termos-relatorios
order: 1
status: review
lastReview: "2026-07-08"
systems:
  - SBP
  - SEI
procedureId: "termo-responsabilidade:emitir-termo-responsabilidade"
---

# Emissão de termo de responsabilidade

!!! info "Informações do procedimento"

    **Status editorial:** Em revisão · **Última revisão:** 08/07/2026 · **Sistemas envolvidos:** SBP, Termos-Responsabilidade

<div class="checklist-controls" data-procedure-id="termo-responsabilidade:emitir-termo-responsabilidade" role="region" aria-label="Controles do checklist">
<div class="checklist-actions">
<button type="button" class="md-button checklist-print-button" aria-label="Imprimir ou salvar este procedimento como PDF">Imprimir</button>
<button type="button" class="md-button checklist-clear-button" aria-label="Limpar progresso do checklist deste procedimento">Limpar checklist</button>
<span class="checklist-progress" aria-live="polite"></span>
</div>
<p class="checklist-disclaimer">Marcações salvas só neste navegador. Elas não constituem registro oficial nem histórico auditável.</p>
</div>

## Objetivo

Atualizar a planilha de acervo a partir do relatório gerencial do SBP e emitir os termos de responsabilidade por unidade organizacional, garantindo que os dados impressos reflitam a situação atual dos bens ativos.

## Pré-requisitos

Antes de iniciar, verifique se você possui:

- [ ] Acesso ao link gerencial do SBP com perfil que permita gerar relatórios do módulo financeiro.
- [ ] Acesso de rede à pasta `J:\colog\sepat`.
- [ ] Microsoft Excel instalado.
- [ ] Navegador padrão disponível para acessar `localhost:5000`.

!!! warning "Cuidado"

    Não altere a estrutura de colunas da planilha `acervo.xlsx`. Qualquer mudança de layout quebrará a leitura pelo sistema emissor dos termos.

## Passos

<div class="steps" markdown>

1. **Acesse o relatório de bens patrimoniais no gerencial**

    Abra o <a href="https://www3.cfc.org.br/spw/sistemasgerenciaispadronizado/chamador/login.aspx" target="_blank" rel="noopener noreferrer"> Sistema Gerencial </a> , acesse o **módulo financeiro** e, em seguida, o submódulo **bens patrimoniais**.

    ![Tela do gerencial exibindo o submódulo Bens Patrimoniais dentro do módulo Financeiro.](imagens/1_gerencial_bens_patrimoniais.png)

2. **Filtre pelos bens ativos**

    No relatório, no campo **Situação**, digite `ativo` para filtrar apenas os bens ativos.

    ![Relatório de bens patrimoniais com o filtro Situação preenchido com "ativo".](imagens/2_gerencial_filtro_ativo.png)

3. **Exporte o relatório para Excel**

    Clique em **Exportar**, selecione **Arquivo Excel** e marque a opção **check (em V)**. Baixe o arquivo gerado.

    ![Tela de exportação do relatório com a opção Arquivo Excel selecionada.](imagens/3_gerencial_exportar_planilha.png)

4. **Ajuste a planilha exportada**

    Abra a planilha baixada e **apague a coluna I**.

    !!! note "Nota"

        A remoção da coluna I é obrigatória para manter o padrão da planilha de destino, de onde o sistema emissor dos termos de responsabilidade lerá os dados.

    ![Planilha exportada com a coluna I destacada para exclusão.](imagens/4_gerencial_excluir_coluna.png)

5. **Selecione e copie o intervalo de dados**

    Clique na célula **A4** e execute, em sequência:

    - `Ctrl + Shift + →` (seleciona até a última coluna preenchida à direita)
    - `Ctrl + Shift + ↓` (estende a seleção até a última linha preenchida)
    - `Ctrl + C` (copia o intervalo)

    ![Intervalo selecionado a partir da célula A4 até a última linha e coluna com dados.](imagens/5_gerencial_copiar_celulas.png)

6. **Cole os dados em `acervo.xlsx`**

    Acesse `J:\colog\sepat` e abra a planilha destino **`acervo.xlsx`**. Selecione a célula **A2** e cole (`Ctrl + V`) o conteúdo da área de transferência.

    !!! tip "Dica"

        Após colar, os dados atualizados do SBP passam a alimentar a fonte de dados usada pelo emissor de termos de responsabilidade.

    ![Planilha acervo.xlsx com os dados colados a partir da célula A2.](imagens/6_planilha_acervoxlsx.png)

7. **Inicie o sistema emissor de termos**

    Dê **duplo clique** em `J:\colog\sepat\Termos-Responsabilidade.exe` e aguarde o carregamento da aplicação. Abrirá um terminal (tela preta), não feche essa janela, até finalizar os passos.

    !!! note "Nota"

        A aplicação é um sistema Web local. O acesso é feito pelo navegador. Futuramente a TI poderá disponibilizá-lo online ou pela intranet.

    ![Aplicação Termos-Responsabilidade.exe em processo de carregamento.](imagens/7_abrir_executavel.png)

8. **Acesse a aplicação no navegador**

    Abra o navegador e digite `localhost:5000` na barra de endereços.

    ![Tela inicial da aplicação de termos de responsabilidade em localhost:5000.](imagens/8_localhost5000.png)

9. **Gere o termo por unidade organizacional**

    Acesse **Termos por Unidade Organizacional**, selecione o termo que será impresso e gere o arquivo.

    ![Tela de seleção do termo por unidade organizacional com a opção de geração.](imagens/9_emissao_termo.png)

10. **Recupere o arquivo emitido**

    O termo será emitido em `J:\colog\sepat\`, juntamente com a planilha Excel correspondente.

    ![Pasta J:\colog\sepat exibindo o termo gerado e a planilha Excel associada.](imagens/10_recuperacao_arquivo.png)

</div>

## Resultado esperado

Ao concluir este procedimento você terá:

- Planilha `acervo.xlsx` atualizada com os bens ativos extraídos do SBP.
- Termo de responsabilidade da unidade organizacional emitido em `J:\colog\sepat\`, acompanhado da planilha Excel correspondente.

**Como confirmar:** Abra o arquivo gerado em `J:\colog\sepat\` e verifique se o termo contém os bens da unidade selecionada, com dados consistentes com a situação atual do SBP.

## Referências

- Manual de Gestão Patrimonial do CFC — disponível no portal do CFC.
- Lei n.º 4.320/1964, arts. 94 a 96 — disposições gerais sobre controle patrimonial.
- Lei n.º 14.133/2021 — Nova Lei de Licitações e Contratos, no que se refere à gestão patrimonial.
