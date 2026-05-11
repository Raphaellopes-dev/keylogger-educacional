╔══════════════════════════════════════════════════════════════════════════════╗
║                            ⚠️  ATENÇÃO  ⚠️                                   ║
║                                                                              ║
║   Este é um projeto ESTRITAMENTE educacional. Foi criado para ensinar       ║
║   como keyloggers funcionam e como se defender contra eles.                 ║
║                                                                              ║
║   O USO NÃO AUTORIZADO de keyloggers em sistemas que você não possui        ║
║   ou sem permissão explícita por escrito é ILEGAL e ANTIÉTICO.              ║
║                                                                              ║
║   O uso indevido deste software pode violar:                                 ║
║   - Lei de Crimes Cibernéticos (Brasil - Lei 12.737/2012)                    ║
║   - LGPD (Lei Geral de Proteção de Dados)                                    ║
║   - Leis de Privacidade e Proteção de Dados internacionais                   ║
║   - Leis Penais locais (invasão de dispositivo, violação de sigilo)          ║
║                                                                              ║
║   VOCÊ FOI AVISADO. Use com responsabilidade e APENAS em seus próprios       ║
║   dispositivos.                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

# Keylogger Educacional

Um projeto **estritamente educacional** em Python que demonstra como o
monitoramento de entrada funciona a nível de sistema, e como detectar e se
proteger contra tais ferramentas. Criado para estudantes de cibersegurança,
hackers éticos e desenvolvedores que desejam compreender segurança defensiva.

## Aviso Ético

> ⚠️ **LEIA COM ATENÇÃO:** Este software captura **todas** as teclas digitadas.
> Ele deve ser usado **EXCLUSIVAMENTE** em dispositivos próprios ou com
> autorização explícita por escrito. O uso não autorizado constitui crime
> previsto no art. 154-A do Código Penal Brasileiro (Lei 12.737/2012) e
> legislações análogas em outros países. Os desenvolvedores **não se
> responsabilizam** pelo uso indevido desta ferramenta.

## Propósito Educacional

Este projeto foi desenvolvido para:
- Ensinar como keyloggers capturam entrada do teclado em nível de sistema
- Demonstrar técnicas de detecção de hooks de teclado suspeitos
- Capacitar profissionais de segurança a entender e se proteger contra ameaças
- Servir como base de estudo para disciplinas de segurança ofensiva e defensiva

## Funcionalidades

- **Captura de Teclas** — Registra pressionamentos com suporte completo a teclas especiais
- **Rastreamento de Janelas** — Armazena o título da janela ativa (Windows)
- **Registros com Timestamp** — Cada evento é carimbado com data/hora para análise forense
- **Rotação de Logs** — Cria automaticamente um novo arquivo de log a cada dia
- **Estatísticas de Teclas** — Analisa logs para identificar teclas mais usadas, velocidade e horários ativos
- **Verificação de Proteção** — Detecta hooks de teclado suspeitos e possíveis keyloggers
- **Modo Serviço** — Executa como um processo daemon em segundo plano

## Instalação

```bash
# 1. Clone ou baixe o projeto
# 2. Instale as dependências
pip install -r requirements.txt
```

## Como Usar

```bash
# Iniciar o keylogger (com confirmação do aviso ético)
python main.py start

# Parar o keylogger
python main.py stop

# Analisar os logs capturados
python main.py analyze

# Verificar possíveis keyloggers no sistema
python main.py protect

# Exibir status atual do monitoramento
python main.py status
```

### Fluxo de Confirmação ("I AGREE")

Ao executar `python main.py start` pela primeira vez, o WARNING.txt será
exibido. Você deverá digitar **"I AGREE"** (em maiúsculas) para confirmar
que leu e aceita os termos éticos e legais. Esta confirmação fica registrada
localmente e é solicitada novamente apenas se o arquivo de aviso for alterado.

## Estrutura do Projeto

```
keylogger-educacional/
├── main.py                 # Ponto de entrada CLI
├── requirements.txt        # Dependências Python
├── WARNING.txt            # Aviso ético (exibido na primeira execução)
├── README.md              # Este arquivo
└── keylog/                # Pacote principal
    ├── __init__.py
    ├── listener.py        # Lógica de captura de teclas
    ├── analyzer.py        # Análise e estatísticas de logs
    └── protector.py       # Detecção de keyloggers
```

## Como se Proteger Contra Keyloggers

1. **Use um Gerenciador de Senhas** — Preencha credenciais automaticamente sem digitar
2. **Ative a Autenticação de Dois Fatores (2FA)** — Mesmo que as teclas sejam capturadas, o 2FA bloqueia o acesso
3. **Teclado Virtual** — Use teclados na tela para entradas sensíveis
4. **Software Antikeylogger** — Ferramentas que detectam e bloqueiam hooks de teclado
5. **Verificações Regulares** — Execute o comando `protect` para checar hooks suspeitos
6. **Mantenha o Sistema Atualizado** — Corrija vulnerabilidades exploradas por keyloggers
7. **Monitore Processos em Execução** — Revise periodicamente processos desconhecidos

## Aviso Legal

> Este software é fornecido **exclusivamente para fins educacionais**. O autor
> não apoia ou incentiva qualquer uso ilegal ou antiético desta ferramenta. Os
> usuários são os únicos responsáveis por garantir que seu uso esteja em
> conformidade com todas as leis aplicáveis, incluindo a Lei 12.737/2012
> (Lei Carolina Dieckmann) e a LGPD (Lei 13.709/2018) no Brasil, e legislações
> equivalentes em outros países. A instalação de keyloggers em sistemas que
> você não possui ou sem permissão explícita é **crime** na maioria das
> jurisdições.

## Licença

Este projeto é distribuído exclusivamente para fins educacionais. Nenhuma
garantia é fornecida. O uso comercial ou malicioso é proibido.
