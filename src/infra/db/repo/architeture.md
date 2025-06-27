Ok, eu recebi o conselho de sempre salvar a ideia por trás da minha arquitetura em um arquivo chamado "architeture.md"
E eu estou enrolando fazer isso a muito tempo, mas é melhor começar logo kkkk
Somente esboçando aqui, vou escrever em português mesmo, depois pego e vou raduzindo na mão para o inglês.
Graças a Deus existe a extensão "generate markdown structure" ksksks

repositories/
├── base/                   # Pacote de operações base
│   ├── __init__.py         # Interface with all base classes
│   ├── base.py             # Main class
│   ├── deletters.py        # Delete operations
│   ├── getters.py          # Read operations
│   ├── insertteers.py      # Create operations Operações
│   ├── models.py           # Shared models
│   └── updatters.py        # Update operations
├── session/                # Pacote de gerenciamento de sessão tlg
│   ├── __init__.py         # Interface com session_scope
│   └── session_manager.py  # Session manager
├── __init__.py             # Inicialização do módulo e interface com os repositórios (por agora só tem produtos né kkkk)
├── models.py               # Isso aqui tá sendo desenvolvido ainda, é mais para fins typing, acho que não está com o nome adequado 
└── produtos.py             # Produtos repository
