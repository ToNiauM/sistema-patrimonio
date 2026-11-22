#!/bin/bash
# Teste assistido do SPW: o robô faz o login com você olhando a tela dele pelo navegador (noVNC) e, se o Google
# pedir o desafio de imagens, espera você resolver; depois exporta e valida o arquivo. Ver README, "Teste
# assistido do SPW".
# Uso: ./spw_assistido.sh             -> só testa (baixa em dados/spw/assistido.xls e valida; a base não muda)
#      ./spw_assistido.sh --importar  -> se der certo, importa na base pelo mesmo caminho do robô
# Antes, no seu computador: ssh -L 16080:127.0.0.1:6080 <usuário>@<servidor>
set -uo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."

if [ $# -gt 1 ] || { [ $# -eq 1 ] && [ "$1" != "--importar" ]; }; then
  echo "Uso: $0 [--importar]" >&2
  exit 2
fi
if [ ! -t 0 ]; then
  echo "Rode num terminal: o script espera você apertar Enter quando estiver vendo a tela." >&2
  exit 1
fi
if ! docker image inspect termos-patrimonio-robo:latest >/dev/null 2>&1; then
  echo "A imagem do robô não existe. Construa com: docker compose build robo" >&2
  exit 1
fi
if ss -tln | grep -qE '[:.]6080[[:space:]]'; then
  echo "A porta 6080 já está em uso (outro teste assistido aberto?)." >&2
  exit 1
fi

# Mesmo lock do robô (atualizar_base.sh e atender_pedidos.py): o Chrome usa o mesmo perfil do robô.
exec 9>dados/robo.lock
if ! flock -w 900 9; then
  echo "Outra atualização ou emissão está em andamento há mais de 15 min; tente de novo." >&2
  exit 1
fi

# Tela virtual (Xvfb) compartilhada: x11vnc a transmite por VNC só dentro do container, e o websockify serve o
# noVNC (cliente VNC no navegador) na 6080, que o docker publica só em 127.0.0.1 do servidor. Os pacotes do VNC
# são instalados na hora, para a imagem do robô não crescer por causa de um teste.
echo "Preparando a tela do robô (instala o VNC, cerca de 40 s)..."
docker run --rm -it --init --name spw-assistido --shm-size=1g \
  -p 127.0.0.1:6080:6080 \
  -e TZ=America/Sao_Paulo \
  --env-file "$PWD/secrets/spw.env" \
  -v "$PWD/dados:/app/dados" \
  -v "$PWD/secrets:/app/secrets:ro" \
  -v "$PWD/scripts/spw_assistido.py:/app/spw_assistido.py:ro" \
  termos-patrimonio-robo:latest sh -c '
    set -e
    apt-get update -qq >/dev/null 2>&1
    apt-get install -y -qq --no-install-recommends x11vnc novnc websockify >/dev/null 2>&1
    if ! python -c "import capsolver" >/dev/null 2>&1; then
      echo "Instalando dependência Python capsolver..."
      python -m pip install --no-cache-dir -q capsolver
    fi
    Xvfb :99 -screen 0 1366x900x24 -nolisten tcp >/dev/null 2>&1 &
    export DISPLAY=:99
    sleep 1
    x11vnc -display :99 -nopw -forever -shared -rfbport 5900 -localhost -quiet >/dev/null 2>&1 &
    websockify --web /usr/share/novnc 6080 localhost:5900 >/dev/null 2>&1 &
    exec python -u /app/spw_assistido.py "$@"' sh "$@"
