# 📝 Backlog Front-end: Atividade 02

## 🏗️ 1. Setup & Estrutura Base
- [✅] **Configurar Ambiente:** Verificar instalação do `flet` no ambiente gerenciado pelo `uv`.
- [✅] **Organizar Diretórios:** - Criar `app/ui/assets/` para recursos visuais.
    - Criar `app/ui/components/` para widgets reutilizáveis.
- [✅] **Main Entry Point:** Configurar o `main.py` para inicializar a aplicação Flet apontando para a interface.

## 🎨 2. Desenvolvimento da Interface (UI)
- [ ] **Layout Principal:** Definir a estrutura da janela (tamanho, título e tema).
- [ ] **Componentes de Entrada:** - Implementar campo de texto para entrada manual.
    - Criar botão de ação para captura de áudio (interface).
- [ ] **Componentes de Saída:** - Criar área de exibição para o texto traduzido/Morse.
    - Adicionar feedback visual de carregamento (ProgressRing).
- [ ] **Refatoração:** Isolar componentes repetitivos em `components/`.

## 🔗 3. Integração com API (Comunicação)
- [ ] **Configurar Client HTTP:** Instalar e configurar `httpx` ou `requests`.
- [ ] **Serviços de Tradução:** Criar funções assíncronas para consumir os endpoints do Alessandro.
- [ ] **Tratamento de Exceções:** - Lógica para lidar com timeout da API.
    - Exibição de mensagens de erro (SnackBars) para o usuário.
- [ ] **Gerenciamento de Estado:** Garantir que a UI atualize assim que a resposta da API chegar.

## 🧪 4. Validação e Ajustes
- [ ] **Testes de Interface:** Verificar comportamento da UI com diferentes tamanhos de janela.
- [ ] **Logs de Front-end:** Implementar chamadas ao sistema de logging em `utils/`.
- [ ] **Revisão de Assets:** Garantir que ícones e mídias estão carregando corretamente em `assets/`.