---
title: Cadastros
description: Manter centros de custo, localizações, pessoas e processos SEI — incluir, editar, vincular, transferir, atribuir bens, encerrar e excluir.
area: sistema
order: 5
status: review
lastReview: "2026-10-22"
systems:
  - Sistema de Patrimônio
procedureId: "sistema:cadastros"
---

# Cadastros

!!! info "Informações do procedimento"

    **Status editorial:** Em revisão · **Última revisão:** 22/10/2026 · **Sistemas envolvidos:** Sistema de Patrimônio

<div class="checklist-controls" data-procedure-id="sistema:cadastros" role="region" aria-label="Controles do checklist">
<div class="checklist-actions">
<button type="button" class="md-button checklist-print-button" aria-label="Imprimir ou salvar este procedimento como PDF">Imprimir</button>
<button type="button" class="md-button checklist-clear-button" aria-label="Limpar progresso do checklist deste procedimento">Limpar checklist</button>
<span class="checklist-progress" aria-live="polite"></span>
</div>
<p class="checklist-disclaimer">Marcações salvas só neste navegador. Elas não constituem registro oficial nem histórico auditável.</p>
</div>

## Objetivo

Os cadastros dizem **quem responde por cada bem**:

- o **centro de custo** (setor) e o seu responsável;
- as **localizações** (salas) de cada centro — um bem ativo numa localização entra no termo do centro;
- as **pessoas** que têm bens de uso individual — um bem atribuído a uma pessoa sai do termo do setor e
  entra no termo individual;
- os **processos SEI** usados para emitir cada tipo de termo.

Os bens e as localizações vêm do SPW; aqui você só define os vínculos.

## Quem pode

- Administrador e Operador: consultar, incluir, editar, vincular, transferir, atribuir, encerrar processos.
- **Só o Administrador**: excluir centro de custo, remover vínculo de localização, excluir pessoa e excluir
  processo.

## Antes de começar

- [ ] Ter a sigla, o nome, a função, a matrícula e o e-mail do responsável (centro de custo).
- [ ] Ter o nome completo, a matrícula, o e-mail e a unidade no SEI (pessoa com bens individuais).
- [ ] Ter o número do processo SEI aberto para os termos do ano.

As quatro áreas ficam em **Cadastros**, no menu, em abas. Todas têm busca, filtros, ordenação (clique no
título da coluna) e paginação de 10, 20 ou 50 registros. Formulários com erro mantêm o que foi digitado.
Toda exclusão, remoção de vínculo ou transferência passa por uma **tela de confirmação** que mostra o que
vai mudar.

## Centros de custo

![Cadastros › Centros de custo: busca, itens por página, tabela com centro, responsável, função e as ações Editar, Localizações e Excluir.](img/c01-centros-lista.png)

<div class="steps" markdown>

1. **Para incluir, clique em Novo centro de custo**, preencha os campos e clique em **Salvar**

    Sigla e nome do responsável são obrigatórios. A **matrícula** e a **função** vão para o texto do termo; o
    **e-mail** é usado no pedido de assinatura; **Unidade no SEI** só é preciso quando a sigla da unidade
    no SEI for diferente da sigla do centro.

    ![Formulário Novo centro de custo preenchido: sigla GEX-EXEMPLO, responsável, função, matrícula e e-mail.](img/c02-centro-novo.png)

2. **Confira a mensagem e o registro destacado na lista**

    *Centro de custo … cadastrado. Você já pode vincular suas localizações.*

    ![Lista de centros de custo com o novo centro destacado.](img/c03-centro-salvo.png)

3. **Para alterar, clique em Editar**, corrija e clique em **Salvar alterações**

    Mudar a sigla mantém as localizações e as referências dos termos. No fim do formulário aparecem as
    localizações vinculadas e o link para gerenciá-las.

    ![Editar centro de custo GEX-REIP com as localizações vinculadas no fim.](img/c04-centro-editar.png)

4. **Para excluir (só administrador), clique em Excluir e confira a confirmação**

    ![Confirmar exclusão do centro: aviso do que acontece com as localizações e os botões Cancelar e Confirmar exclusão.](img/c05-centro-excluir-confirmar.png)

    Clique em **Confirmar exclusão**. Aparece *Centro de custo … excluído.*

    ![Lista de centros de custo com a mensagem de sucesso da exclusão.](img/c06-centro-excluido.png)

    !!! warning "Cuidado"

        Centro com **bens ativos sob sua guarda não pode ser excluído**: primeiro transfira as localizações
        para outro centro.

    ![Confirmação bloqueada: o centro tem 62 bens ativos sob guarda; mova as localizações antes de excluir.](img/c07-centro-excluir-bloqueado.png)

</div>

## Localizações

![Cadastros › Localizações: aviso de bens de termo individual sem pessoa, filtros por centro e situação, e o quadro Mover selecionadas para.](img/c08-localizacoes-lista.png)

### Vincular uma localização sem centro de custo

Quando o SPW traz uma sala nova (ou um vínculo é removido), os bens ativos dela ficam **sem centro de custo**
e não entram em termo nenhum. O aviso amarelo mostra quantas localizações estão nessa situação.

<div class="steps" markdown>

1. **Clique em Resolver vínculos** (ou filtre **Situação: Sem centro de custo**)

    ![Localizações filtradas por Sem centro de custo, com o aviso de 1 localização com bens ativos sem centro.](img/c11-localizacoes-sem-centro.png)

2. **Clique em Vincular centro na linha, escolha o centro de custo e clique em Salvar**

    ![Formulário Vincular localização com a localização e o centro de custo escolhidos.](img/c12-localizacao-vincular.png)

3. **Confira a mensagem** *Localização vinculada ao centro de custo.*

    ![Lista de localizações com a mensagem de sucesso.](img/c13-localizacao-vinculada.png)

</div>

### Alterar o centro de uma localização

<div class="steps" markdown>

1. **Na linha da localização, clique em Alterar centro e escolha o centro de destino**

    ![Alterar centro da localização: a localização, o centro atual e o centro de destino escolhido.](img/c14-localizacao-alterar.png)

2. **Clique em Revisar alteração e confira origem e destino**

    ![Confirmar transferência de localizações: tabela com registro, origem e destino.](img/c15-localizacao-revisar.png)

3. **Clique em Confirmar transferência**

    Os bens continuam na mesma localização; a responsabilidade passa ao centro de destino. Atribuições
    individuais são mantidas.

    ![Lista de localizações com a mensagem 1 localização movida para o centro de destino.](img/c16-localizacao-transferida.png)

</div>

### Transferir várias localizações de uma vez

<div class="steps" markdown>

1. **Filtre pelo centro, marque as localizações na tabela e escolha o centro em Mover selecionadas para**

    O contador mostra quantas foram marcadas. A seleção vale só para a página atual e é limpa ao buscar,
    filtrar ou mudar de página.

    ![Quadro Mover selecionadas para com o centro de destino escolhido e 2 localizações selecionadas.](img/c17-localizacoes-lote.png)

2. **Clique em Revisar transferência, confira e clique em Confirmar transferência** (ou **Cancelar**)

    ![Confirmação da transferência de duas localizações, com origem e destino.](img/c18-localizacoes-lote-revisar.png)

</div>

### Remover o vínculo (só administrador)

<div class="steps" markdown>

1. **Na linha, clique em Remover vínculo, confira e clique em Confirmar remoção**

    Os bens não são excluídos nem mudam de localização; se houver bens ativos, a localização fica sem centro
    de custo.

    ![Confirmar remoção do vínculo da localização, com origem e destino Sem centro de custo.](img/c09-localizacao-remover.png)

    ![Mensagem Vínculo da localização removido e o aviso de localização com bens ativos sem centro.](img/c10-localizacao-removida.png)

</div>

!!! note "Nota"

    A localização **TERMOS INDIVIDUAIS** do SPW nunca pertence a um centro de custo: os bens dela seguem a
    pessoa. O aviso *bem(ns) de termo individual sem pessoa atribuída* lista os que ainda precisam ser
    atribuídos em Pessoas.

## Pessoas

![Cadastros › Pessoas: busca e tabela com nome, e-mail, bens atribuídos e as ações Editar, Ver bens e Excluir.](img/c19-pessoas-lista.png)

<div class="steps" markdown>

1. **Para incluir, clique em Nova pessoa**, preencha e clique em **Salvar**

    O nome fica em maiúsculas. **Unidade no SEI** é necessária para emitir o termo individual no SEI.

    ![Formulário Nova pessoa preenchido com nome, matrícula, e-mail e unidade no SEI.](img/c20-pessoa-nova.png)

2. **A tela da pessoa abre com a mensagem de sucesso**

    Nela aparecem matrícula, e-mail, os botões **Editar**, **Voltar à lista de pessoas** e **Ver termo
    individual**, e o quadro **Atribuir um patrimônio**.

    ![Tela da pessoa recém-cadastrada, com o quadro Atribuir um patrimônio.](img/c21-pessoa-salva.png)

3. **Para atribuir um bem, digite o número do patrimônio e clique em Consultar patrimônio**

    A confirmação mostra o bem, a localização, a situação e **quem responde por ele hoje** (centro ou outra
    pessoa).

    ![Confirmar atribuição do patrimônio: o bem, o responsável atual e a pessoa de destino.](img/c22-pessoa-atribuir.png)

4. **Clique em Confirmar atribuição**

    O bem passa a constar na lista da pessoa e **sai do termo do centro de custo**.

    ![Tela da pessoa com a mensagem Bem atribuído e 1 bem sob responsabilidade individual.](img/c23-pessoa-atribuida.png)

5. **Para tirar um bem da pessoa, clique em Remover vínculo na linha do bem e confirme**

    O bem volta a seguir o centro da sua localização.

    ![Confirmar remoção do vínculo do bem com a pessoa.](img/c24-pessoa-remover-vinculo.png)

6. **Para corrigir nome, matrícula, e-mail ou unidade, clique em Editar**

    Os bens atribuídos e os termos já registrados acompanham a mudança de nome.

    ![Formulário Editar pessoa.](img/c25-pessoa-editar.png)

7. **Para excluir (só administrador), clique em Excluir pessoa e confirme**

    As atribuições são removidas; os bens passam a seguir o centro da localização.

    ![Confirmar exclusão da pessoa, com o bem que deixa de ser atribuído.](img/c26-pessoa-excluir.png)

    ![Lista de pessoas com a mensagem Pessoa excluída.](img/c27-pessoa-excluida.png)

</div>

## Processos SEI

Cada tipo de termo (centro de custo, individual e devolução) usa **um processo vigente**. Sem processo
vigente, o termo daquele tipo não pode ser emitido.

![Cadastros › Processos SEI: cartões com o processo vigente de cada tipo de termo, filtros e a tabela de processos.](img/c28-processos-lista.png)

<div class="steps" markdown>

1. **Clique em Novo processo**, escolha o tipo de termo, preencha a descrição e o número e mantenha
   **Usar como processo vigente** marcado

    ![Formulário Novo processo preenchido, com Usar como processo vigente marcado.](img/c29-processo-novo.png)

2. **Clique em Salvar e confira a substituição**

    Se já houver um vigente do mesmo tipo, o sistema mostra o atual e o novo. Os termos já registrados
    continuam com o processo original.

    ![Confirmar substituição do processo vigente: tipo, processo atual e novo.](img/c30-processo-substituir.png)

3. **Clique em Confirmar alteração**

    ![Lista de processos com a mensagem Processo incluído como vigente e o novo número no cartão do tipo.](img/c31-processo-incluido.png)

4. **Para encerrar um processo, clique em Encerrar e confira**

    O tipo de termo fica **sem processo vigente** até você definir outro.

    ![Confirmar encerramento do processo, com o aviso de que o tipo ficará sem processo vigente.](img/c32-processo-encerrar.png)

5. **Para voltar a usar um processo encerrado, clique em Tornar vigente e confirme**

    ![Confirmar processo vigente: o tipo, o processo atual e o que passa a valer.](img/c34-processo-tornar-vigente.png)

    ![Lista de processos com a mensagem Processo marcado como vigente.](img/c35-processo-vigente.png)

6. **Excluir (só administrador)** — só é possível para processo **sem termos registrados**; os demais se
   encerram

    ![Lista de processos com a mensagem Processo excluído e o tipo sem processo vigente.](img/c33-processo-excluir.png)

</div>

## Baixar todos os cadastros

No fim de cada lista, **Baixar todos os cadastros** gera a planilha `cadastros.xlsx` (centros, localizações,
pessoas e atribuições e, quando há, os inventários). A volta dessa planilha (carga em massa) é feita pelo
administrador em [Atualizar base](textos-atualizar-base.md#carregar-a-planilha-de-cadastros-so-administrador).

## O que acontece depois / onde confere

- A mensagem verde no topo e o registro destacado na lista.
- Os termos dos centros e pessoas afetados podem passar a **desatualizado** — emita de novo em
  [Termos](termos.md).
- Na ficha do bem, o centro de custo e o responsável individual atualizados.

## Erros comuns e mensagens

| Mensagem | O que fazer |
|---|---|
| *Confira os campos indicados. Seus dados foram mantidos para correção.* | Corrija o campo em vermelho e salve de novo. |
| *Já existe um centro de custo com esta sigla.* / *Esta pessoa já está cadastrada.* | Use a busca e edite o registro existente. |
| *Informe um e-mail válido.* | Corrija o e-mail. |
| *… tem N bens ativos sob guarda. Mova as localizações…* | Transfira as localizações antes de excluir o centro. |
| *Este processo tem termos registrados; encerre-o em vez de excluir.* | Use Encerrar. |
| *Bem N não encontrado na base.* | Confira o número (bens novos só aparecem depois da atualização da base). |
| *Os dados mudaram ou a revisão expirou. Confira o resumo e confirme novamente.* | Alguém mudou o mesmo cadastro, ou a confirmação ficou aberta mais de 30 minutos. Confira e confirme de novo. |
