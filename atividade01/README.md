# Exercício: Fundamento da Computação Digital - UFPA

[![Download PDF](https://img.shields.io/badge/Download-PDF-red?style=for-the-badge&logo=adobe-acrobat-reader)](https://github.com/reali-705/fundamentos_comunicacao_digital/raw/main/atividade01/main.pdf)

Este repositório contém a resolução da lista de exercícios sobre Sinais e Espectros da disciplina de Fundamentos da Comunicação Digital. O projeto utiliza uma estrutura modular em **LaTeX** para facilitar a colaboração via **Git** entre os membros do grupo. O layout é baseado no modelo de artigos da SBC (Sociedade Brasileira de Computação), garantindo uma apresentação profissional e padronizada.

## 🛠️ Stack Técnica

- **Linguagem:** *LaTeX*
- **Gráficos e Sinais:** TikZ e Pgfplots (para geração de ondas senoidais e espectros via código)
- **Compilador:** MiKTeX (pdflatex)
- **Editor:** VS Code + *LaTeX Workshop*
- **Padronização:** Layout baseado no modelo de artigos da SBC (Sociedade Brasileira de Computação).

## 🚀 Configuração do Ambiente Local

Para compilar este currículo na sua máquina (Windows), siga estes passos:

1. Instalação do Compilador

    Baixe e instale o [MiKTeX](https://miktex.org/download)

    > Dica: Durante a instalação, selecione a opção "Always install missing packages on-the-fly" para evitar erros de pacotes ausentes (como o fontawesome5).

2. Configuração do VS Code (opcional, mas recomendado)

    Instale a extensão *LaTeX Workshop* e adicione as seguintes configurações ao seu settings.json para manter o diretório limpo:

    ```json
    "latex-workshop.latex.autoClean.run": "onBuilt",
    "latex-workshop.latex.clean.fileTypes": [
        "*.aux", "*.bbl", "*.blg", "*.idx", "*.ind",
        "*.lof", "*.lot", "*.out", "*.toc", "*.fdb_latexmk",
        "*.fls", "*.log", "*.synctex.gz"
    ]
    ```

## 🏗️ Como Utilizar

Utilizando a extensão *LaTeX Workshop* no VS Code, você pode compilar o currículo e limpar os arquivos auxiliares com atalhos personalizados:

### Compilação (Build)

Para compilar o currículo e gerar o PDF final:

- Atalho no VS Code: `Ctrl + Alt + B`

### Limpeza de Arquivos "Lixo" (Cleanup)

O *LaTeX* gera diversos arquivos auxiliares (`*.aux`, `*.log`) para gerenciar referências e navegação. Para removê-los e manter apenas o código-fonte e o PDF:

- Atalho no VS Code: `Ctrl + Alt + C`

## 📂 Estrutura Modular

O projeto foi refatorado para centralizar a lógica de formatação na pasta `core/`, separando-a do conteúdo das questões:

```bash
main.tex            # Arquivo mestre que orquestra a compilação 
core/               # "Coração" do projeto (configurações)
  ├── setup.tex     # Pacotes, macros de unidades (Hz, kHz) e estilos 
  ├── metadata.tex  # Dados do grupo, professor e título do trabalho 
  └── header.tex    # Cabeçalho padrão SBC para múltiplos autores
subsections/        # Conteúdo bruto das resoluções
  ├── questao01.tex
  ├── questao02.tex
  ├── questao03.tex
  └── ...
```

---

## Autores

- [![GitHub](https://img.shields.io/badge/-%23121011.svg?style=flat-square&logo=github&logoColor=white) Alessandro Reali Lopes Silva](https://github.com/reali-705)
- [![GitHub](https://img.shields.io/badge/-%23121011.svg?style=flat-square&logo=github&logoColor=white) Caio Barbosa Correa](https://github.com/caiiocb)
- [![GitHub](https://img.shields.io/badge/-%23121011.svg?style=flat-square&logo=github&logoColor=white) Felipe Lisboa Brasil](https://github.com/FelipeBrasill)
