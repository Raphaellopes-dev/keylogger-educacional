# Keylogger Educacional

Projeto educacional sobre seguranca digital.
Aprenda como keyloggers funcionam e como se proteger.

> ATENCAO: Este e um projeto ESTRITAMENTE educacional.
> Use apenas em seus proprios dispositivos.
> O uso nao autorizado e ILEGAL.

## Proposito

Este projeto foi criado para:
- Ensinar como keyloggers capturam teclas no sistema
- Demonstrar tecnicas de deteccao de ameacas
- Ajudar profissionais a se protegerem contra keyloggers

## Funcionalidades

- Captura de teclas com timestamp
- Rastreamento da janela ativa
- Rotacao de logs (arquivo novo por dia)
- Analise de estatisticas de digitacao
- Deteccao de hooks de teclado suspeitos

## Instalacao

```
git clone https://github.com/Raphaellopes-dev/keylogger-educacional.git
cd keylogger-educacional
pip install -r requirements.txt
```

## Como usar

Iniciar (com confirmacao etica):
```
python main.py start
```

Parar:
```
python main.py stop
```

Analisar logs:
```
python main.py analyze
```

Verificar seguranca:
```
python main.py protect
```

## Como se proteger

1. Use gerenciador de senhas (nao digite senhas manualmente)
2. Ative autenticacao de dois fatores (2FA)
3. Use teclado virtual para dados sensiveis
4. Mantenha o sistema atualizado
5. Monitore processos em execucao

## Aviso Legal

Este software e exclusivamente para fins educacionais.
O uso indevido pode violar leis de crimes ciberneticos
(Lei 12.737/2012 - Brasil) e leis internacionais de privacidade.

---

Feito por Raphael Lopes
