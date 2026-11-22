---
title: Sistema de Patrimônio e Inventário — visão geral
description: O que o Sistema de Patrimônio faz, quem usa e o que cada função pode fazer.
area: sistema
order: 0
status: review
lastReview: "2026-10-22"
systems:
  - Sistema de Patrimônio
  - SEI
  - SPW
procedureId: "sistema:visao-geral"
---

# Sistema de Patrimônio e Inventário

!!! info "Informações desta parte do manual"

    **Status editorial:** Em revisão · **Última revisão:** 22/10/2026 · **Sistemas envolvidos:** Sistema de Patrimônio, SEI, SPW

O **Sistema de Patrimônio** é o sistema web da Gerência de Serviços Administrativos (Geserv) do CFC para
cuidar do acervo de bens no dia a dia. Ele reúne, num só lugar:

- a **consulta do acervo** — pesquisa por número, descrição, pessoa ou centro de custo, a ficha de cada bem e
  a **Análise** com filtros, gráficos e exportação para Excel;
- os **Termos de Responsabilidade** (por centro de custo e individuais) e os **Termos de Devolução**, com
  emissão no SEI, cópia para colar no SEI e download em `.docx`, e o histórico de tudo o que foi emitido;
- os **cadastros** que dizem quem responde por cada bem: centros de custo, localizações, pessoas e os
  processos SEI usados nos termos;
- a **atualização da base de bens** a partir do SPW, o sistema oficial de patrimônio (automática todo dia
  útil, ou sob demanda);
- o **inventário físico** por evento: comissão, salas, leitura das plaquetas pelo celular, fotos, sobras,
  painel e relatório.

Os bens, os números de patrimônio, as descrições e as localizações vêm do **SPW**. O Sistema de Patrimônio
**não altera** o SPW: ele lê o cadastro de lá e acrescenta o que o SPW não tem (responsáveis, termos,
inventário).

!!! note "Sobre as imagens deste manual"

    As telas foram capturadas de uma **cópia** do sistema, com os bens e as localizações reais e **todas as
    pessoas trocadas por nomes fictícios** ("Servidor Fictício 01", "Ana Exemplo"...). Os números de
    documentos e de termos digitados nos exemplos também são fictícios. O sistema em produção pode estar com
    outra aparência de tela (outra "casca" visual), mas os menus, os botões e os passos são os mesmos.

## Quem usa e o que cada um pode fazer

Cada usuário recebe uma ou mais **funções**. As funções **se somam**: quem tem duas funções faz o que as duas
permitem. O menu, os atalhos do Início e a Ajuda mostram só o que as suas funções permitem.

| O que dá para fazer | Administrador | Operador | Consulta | Inventário | Consulta de inventários |
|---|:-:|:-:|:-:|:-:|:-:|
| Entrar, trocar a senha, Meus acessos, Ajuda | ✔ | ✔ | ✔ | ✔ | ✔ |
| Início, pesquisa, ficha do bem, Análise e exportação | ✔ | ✔ | ✔ | — | — |
| Ver termos, prévias e termos emitidos | ✔ | ✔ | ✔ | — | — |
| Emitir termo (SEI, Copiar para o SEI, Baixar .docx), anotar documento e enviar e-mail | ✔ | ✔ | — | — | — |
| Cadastros: incluir, editar, vincular, transferir, atribuir | ✔ | ✔ | — | — | — |
| Cadastros: **excluir** (centro, localização, pessoa, processo) | ✔ | — | — | — | — |
| Textos dos termos | ✔ | ✔ | — | — | — |
| Atualizar base: carregar a planilha de bens e baixar as planilhas | ✔ | ✔ | — | — | — |
| Atualizar base: **Atualizar com SPW** e **carregar a planilha de cadastros** | ✔ | — | — | — | — |
| Inventário: ver os eventos e as salas | ✔ todos | — | — | só os da sua comissão | ✔ todos |
| Inventário: ler plaquetas, fotos, sobras, marcar em lote | só na sua comissão | — | — | só na sua comissão | — |
| Inventário: painel, relatório e planilha | ✔ | — | — | — | ✔ |
| Administração: criar, abrir, fechar, finalizar e excluir inventários; comissão | ✔ | — | — | — | — |
| Administração: usuários e funções | ✔ | — | — | — | — |

!!! tip "Dica"

    Quem tem **só** a função Inventário entra direto na tela do Inventário, sem pesquisa, Análise nem termos.
    Para a conferência em campo, isso é tudo de que se precisa — e funciona no celular.

## Por onde começar

<div class="grid cards" markdown>

-   __[Entrar e a sua conta](entrar.md)__

    ---

    Primeiro acesso, troca de senha, sair e Meus acessos (SEI e SPW).

-   __[Navegação, pesquisa e ajuda](navegacao.md)__

    ---

    Início, menu, lupa de pesquisa, ajuda de cada tela e uso no celular.

-   __[Consultar bens e Análise](pesquisa-analise.md)__

    ---

    Pesquisa, ficha do bem, filtros, gráficos e exportação.

-   __[Termos de Responsabilidade e Devolução](termos.md)__

    ---

    Gerar, emitir no SEI, copiar, baixar, anotar documento e enviar o pedido de assinatura.

-   __[Cadastros](cadastros.md)__

    ---

    Centros de custo, localizações, pessoas e processos SEI.

-   __[Textos e Atualizar base](textos-atualizar-base.md)__

    ---

    Dizeres dos termos e atualização dos bens a partir do SPW.

-   __[Inventário: guia rápido da comissão](inventario-comissao.md)__

    ---

    Roteiro de bolso: leitor sem fio no celular, o que fazer em cada situação e a quem recorrer.

-   __[Inventário: conferência nas salas](inventario-conferencia.md)__

    ---

    Leitura das plaquetas, divergências, sobras, fotos e marcação em lote.

-   __[Inventário: acompanhamento](inventario-acompanhamento.md)__

    ---

    Painel, relatório e planilha de qualquer inventário.

-   __[Administração](administracao.md)__

    ---

    Criar e conduzir inventários; usuários e funções.

-   __[Glossário](glossario.md)__

    ---

    Termo de responsabilidade, centro de custo, localização, evento, sala, comissão, SPW, SEI...

</div>

## Como o sistema se liga às outras rotinas deste manual

- A base de bens vem do **SPW** — o mesmo "Sistema Gerencial" usado no procedimento
  [Emissão de termo de responsabilidade](../termos-relatorios/termos-responsabilidade/index.md), passos 1 a 3
  (exportar o relatório de bens). No Sistema de Patrimônio a atualização é automática; a planilha exportada à
  mão só é necessária quando o robô não consegue entrar no SPW (veja
  [Atualizar base](textos-atualizar-base.md#atualizar-a-base-de-bens)).
- Os **termos** são assinados no **SEI**. O sistema cria o documento no processo e o coloca no bloco de
  assinatura; a assinatura e a tramitação continuam no SEI.
- As **movimentações** e **baixas** de bens continuam sendo registradas no SPW/SBP; depois da atualização
  da base, o Sistema de Patrimônio mostra o que mudou e marca os termos que ficaram desatualizados.
