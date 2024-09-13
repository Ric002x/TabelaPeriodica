# ⚛️ Atomic Discoveries

## 📚 Introdução

Bem-vindo ao projeto **Atomic Adventures**. Este website foi criado com o propósito de disseminar conhecimentos científicos de maneira interativa, acessível e criativa. Nossa missão é tornar o aprendizado de ciências uma experiência envolvente, utilizando recursos digitais para incentivar a curiosidade e o entendimento profundo dos conceitos científicos.


## 📦 Tecnologias Utilizadas e Dependências do Projeto

 - **Python: 3.12.3**
	- Usado para desenvolver todo o backend do site, incluindo views, models e a lógica principal do aplicativo.

 - **Django: 5.0.6**
	- Framework utilizado para o desenvolvimento do site, responsável por configurar e administrar toda a estrutura de desenvolvimento web.

 - **Node.js: v20.14.0 (JavaScript)**
	- Usado para desenvolver a interatividade do site com o usuário, incluindo animações e botões de ativação.

 - **HTML**

 - **CSS**

 - **Pytest e Pytest-Django**

	- **Pytest** é um framework que auxilia na criação de testes funcionais escaláveis para aplicações e bibliotecas.

	- **Pytest-Django** é um plugin do Pytest que fornece ferramentas úteis para testes em aplicações Django.
	
 - **Coverage**
	- Ferramenta usada para monitorar e verificar quais partes do código backend estão sendo cobertas pelos testes.


## 🏛️ Arquitetura do Projeto
O projeto foi construído seguindo as práticas recomendadas de estruturação de arquivos e banco de dados para projetos Django.

**Diretório do Projeto**

O Django possui uma estruturação de arquivos que separa o diretório principal do projeto das demais dependências e aplicativos. No diretório principal do projeto, encontram-se as configurações fundamentais, como segurança, definições de desenvolvimento, configurações de banco de dados, rotas de URLs e outras configurações essenciais, incluindo os arquivos de configuração para WSGI e ASGI, que são responsáveis pelo gerenciamento do servidor de aplicação.

Esse arquivo principal é criado a partir do comando:
```bash
django-admin startproject "nome_do_projeto" .
```
No caso deste projeto, ele foi nomeado como "periodic_table", refletindo o objetivo central do projeto.

 - **Observação**:
	> O ponto ao final do comando é importante, pois determina que os arquivos do projeto sejam criados na raiz do diretório atual. Sem o ponto, o comando criaria uma pasta adicional com o nome do projeto, o que poderia complicar o desenvolvimento ao adicionar um nível desnecessário de diretórios.


A partir desse comando, foi criado:
 - **Diretório: peridic_table (nome dado ao projeto)**
	Esse diretório trará o seguintes arquivos:

	- **__init__.py**: Marca o diretório como um pacote Python.

	- **asgi.py**: Configuração para a interface ASGI, usada para aplicações assíncronas.

	- **wsgi.py**: Configuração para a interface WSGI, usada para servir a aplicação em produção.

	- **settings.py**: Contém todas as configurações do projeto, incluindo segurança, banco de dados e outras definições essenciais. Além disso, o settings.py configura quais apps serão "executados" junto ao projeto. Ou seja, ao criar um novo app, ele deve ser registrado no settings.py na lista INSTALLED_APPS. Isso garante que o Django reconheça e inclua o app na aplicação, permitindo que suas rotas, modelos e views sejam integrados ao projeto.

	- **urls.py**: Define as rotas e URLs que serão mapeadas para as views do projeto.

 - **Arquivo manage.py**
	- Script para gerenciar toda a aplicação Django, permitindo executar comandos administrativos, como iniciar o servidor de desenvolvimento, migrar banco de dados, e criar apps.

**Verificação do Projeto**

Com essa estrutura, o projeto já está parcialmente configurado e pronto para o desenvolvimento. Para verificar se tudo foi configurado corretamente, basta utilizar o comando:
```bash
python manage.py runserver
```
Esse comando inicia o servidor de desenvolvimento local, que pode ser acessado em
http://127.0.0.1:8000/.

**Diretórios de Apps**

Além do diretório principal, o Django também é estruturado em apps individuais, que são módulos independentes e reutilizáveis, cada um focado em uma funcionalidade específica do sistema. Cada app pode conter suas próprias rotas, modelos, views e templates, permitindo uma organização modular e escalável do código. No caso desse projeto, por exemplo, temos:

 - **Users**: Gerencia toda a funcionalidade relacionada aos usuários, como autenticação, perfis e permissões.

 - **Learn Lab**: Lida com a criação, exibição e gerenciamento das atividades educacionais dentro da plataforma.

 - **Elements**: Responsável pela exibição e manipulação dos dados relacionados aos elementos químicos na tabela periódica.

A criação de um diretório de app é feita com o comando:
```bash
python manage.py startapp "nome_do_app""
```

Cada diretório de app criado inicia com os seguintes arquivos:

 - **__init__.py**: Marca o diretório como um pacote Python.

 - **admin.py**: Configura a interface de administração do Django para o app.

 - **apps.py**: Configura as opções do app.

 - **models.py**: Define os modelos de dados para o app.

 - **tests.py**: Contém testes unitários para o app.
 
 - **views.py**: Define as views do app.

Durante o desenvolvimento, é comum fazer algumas modificações na estrutura dos diretórios dos apps para melhorar a organização:

1. **Adicionar o arquivo urls.py**: Para gerenciar as URLs específicas de cada app.

2. **Substituir o arquivo tests.py por um diretório tests**: Permite a criação de diferentes arquivos de teste, separados por funcionalidade, como testes para views e templates ou testes para models.

3. **Criar os diretórios templates e static**:

	- **templates**: Para organizar os arquivos de estruturação HTML.

	- **static**: Para organizar arquivos estáticos, como CSS, imagens e JavaScript. É necessário configurar os diretórios static no arquivo settings.py do projeto. Para mais informações, consulte a documentação sobre arquivos estáticos em: [Como Manusear Arquivos Estáticos](https://docs.djangoproject.com/en/5.1/howto/static-files/).

**Diretório de Mídias**

Além dos arquivos estáticos, dependendo das necessidades do projeto, pode ser necessário configurar um diretório de mídias, que é utilizado para armazenar arquivos enviados pelos usuários, como imagens de perfil, documentos e outros arquivos. O diretório de mídias é configurado tanto no arquivo settings.py quanto no urls.py do diretório principal do projeto.

 - **Configuração do Diretório de Mídias**
	- O diretório de mídias é, por padrão, criado na raiz do projeto e é configurado para receber os arquivos enviados pelos aplicativos. Sua estrutura básica é:

```
 |-- media
	|-- app1
	|-- app2
	|-- app3...
```
Aqui, cada subdiretório dentro de media pode corresponder a um app específico ou a um tipo de mídia.

 - **Configuração em settings.py**: No arquivo settings.py, você deve adicionar as seguintes configurações para definir o diretório de mídias e a URL de acesso:

	```python
	MEDIA_URL = '/media/'
	MEDIA_ROOT = os.path.join(BASE_ROOT, 'media')
	```

	- **MEDIA_URL**: Define a URL pública para acessar os arquivos de mídia.
	- **MEDIA_ROOT**: Define o caminho absoluto para o diretório onde os arquivos de mídia serão armazenados.

 - **Configuração em urls.py**: No arquivo urls.py do diretório principal do projeto, adicione a configuração para servir arquivos de mídia durante o desenvolvimento:

	```python
	# Importações necessárias para configuração
	from django.conf import settings
	from django.conf.urls.static import static

	urlpatterns = [
		# Rotas Inciais do Projeto
	]

	## Configurando o arquivo media
	if settings.DEBUG:
		urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	```


## 🔧 Instalação e Configuração

Para configurar e executar o projeto Atomic Discoveries em sua máquina local, siga as etapas abaixo:

1. Certifique-se de ter os seguintes pré-requisitos instalados:

 - Python
 - Pip
 - Virtualenv


2. Crie um diretório que irá receber os arquivos do projeto. Esta etapa pode ser realizada através da interface do seu sistema operacional ou via comandos no shell/prompt de comando:

```bash
mkdir "nome_do_diretorio"
```

Lembre-se, o diretório será criado na pasta onde o terminal está sendo executado. Para escolher a pasta onde será criado o diretório, antes de criá-lo, utilize o comando:

```bash
cd "caminho_da_pasta"
```

3. Acesse o diretório criado e clone o repositório git:

```bash
git clone git@github.com:Ric002x/TabelaPeriodica.git .
```

> O ponto ao final do comando é necessário para que os arquivos do repositório sejam colocados diretamente na raiz do diretório.


4. Crie e ative o ambiente virtual (Opcional, mas recomendado):

4.1 Crie o ambiente utilizando o comando:

 - No Windows:
```bash
python -m venv "nome_do_ambiente"
```

 - No macOS/Linux:
```bash
python3 -m venv "nome_do_ambiente"
```

 > É recomendado dar o nome de `venv` (virtual environment)

4.2 Ative o ambiente utilizando o comando:

 - No Windows:
```bash
.\venv\Script\activate
```
	
 - No macOS/Linux:
```bash
source venv/bin/activate
```


5. Instale as denpendências:

```bash
pip install -r requirements.txt
```

6. Renomeie o arquivo de variáveis de ambiente:

```bash
mv .env-example .env
```


7. Execute as migrações do banco de dados com o comando:

```bash
python manage.py migrate
```

 > Esse comando irá realizar a criação de tabelas da base de dados


8. Importe os dados principais do site:

Os arquivos necessários para a importação de dados estão localizados nos diretórios dos apps, seguindo o caminho padrão: `/app/management/commands/`

Para realizar as importações, utilize os seguintes comandos:

```bash
python manage.py import_elements
```

> Esse comando irá importar os elementos químicos e suas respectivas informações para o banco de dados.

```bash
python manage.py import_levels
```

```bash
python manage.py import_subjects
```

> Esses comandos irão importar dados de turmas e matérias, essenciais para a criação de atividades no app *learn_lab*.


9. Execução de testes:

Para executar os testes, abra o terminal na pasta raiz do projeto, com o ambiente virtual ativado, e utilize um dos seguintes comandos:

```bash
python manage.py test
```

Ou

```bash
pytest
```

Ambos os comandos executarão todos os testes presentes nos diretórios dos apps.

Os testes disponíveis são testes unitários, que garantem a verificação de funções específicas do site, como views, templates e models.


10. Inciar o Servidor de Desenvolvimento:

Após a execução dos testes e a confirmação de que todos foram bem-sucedidos, você pode iniciar o servidor de desenvolvimento para verificar o site em funcionamento utilizando o comando:

```bash
python manage.py runserver
```

O servidor estará disponível em: http://127.0.0.1:8000

> Em caso de falha dos testes, entre em contato na seção de Suporte.


## 📝 Descrição dos Apps


### App 1: Tabela Peridoca (table_elements)

O app Tabela Periódica, temática principal do site, é projetado para explorar detalhadamente os elementos químicos da tabela periódica. Este aplicativo fornece uma visão abrangente sobre os elementos, desde uma visão geral da tabela até informações detalhadas sobre cada elemento individualmente.

**Funcionalidades Principais:**

- **Página Inicial**: Serve como ponto de partida para navegação no site.

- **Tabela Periódica**: Exibe a tabela periódica completa com informações básicas sobre cada elemento.

- **Detalhes dos Elementos**: Fornece uma página dedicada para cada elemento químico, com detalhes aprofundados sobre suas propriedades e aplicações.

- **Políticas do Site**: Inclui uma página com as diretrizes e políticas do site para garantir a conformidade e transparência.


### App 2: Usuários (users)

O app Usuários é responsável pela gestão e controle das funcionalidades relacionadas aos usuários do site. Ele gerencia o processo de cadastro, login e logout, e oferece funcionalidades adicionais que estão disponíveis exclusivamente para usuários registrados.

**Funcionalidades Principais:**

- **Cadastro e Login**: Permite que novos usuários se registrem no site e que usuários existentes façam login para acessar suas contas.

- **Perfil de Usuário**: Oferece uma seção de perfil onde os usuários podem visualizar e gerenciar suas informações pessoais, como nome de usuário, endereço de e-mail, imagem de perfil e senha.

- **Administração de Dados**: Facilita a atualização e manutenção dos dados do usuário, assegurando que as informações pessoais estejam sempre atualizadas e seguras.

- **Funcionalidades Exclusivas**: Algumas funções do site, como a personalização do perfil e o acesso a certas seções e recursos, estão disponíveis apenas para usuários registrados.

Objetivo: O app Usuários é fundamental para a gestão da interação dos usuários com o site, oferecendo uma experiência personalizada e segura. Embora o acesso básico ao site não exija cadastro, as funcionalidades avançadas e personalizadas estão disponíveis exclusivamente para usuários que se registram e mantêm uma conta ativa.


### App 3: Laboratório de Atividades (learn_lab)

Descrição: O app Laboratório de Atividades é dedicado à gestão de atividades educacionais postadas pelos usuários do site. Este aplicativo permite o gerenciamento completo de atividades, incluindo a postagem, edição, exclusão e visualização de conteúdos educacionais criados pelos usuários.

**Funcionalidades Principais:**

- **Postagem de Atividades**: Os usuários podem criar e publicar atividades educacionais, como exercícios e jogos didáticos, que serão disponibilizados para outros usuários.

- **Gestão de Conteúdo**: Permite a edição e exclusão de atividades já postadas, garantindo que o conteúdo possa ser atualizado ou removido conforme necessário.

- **Documentação em PDF**: Cada atividade deve ser acompanhada por um arquivo PDF que contenha todas as informações necessárias para a implementação em sala de aula. Este PDF é acessível para download pelos demais usuários.

- **Recomendações de Criação**: A página de criação de atividades oferece recomendações e diretrizes para ajudar os usuários a criar conteúdos de qualidade.

- **Sistema de Avaliação**: As atividades podem ser avaliadas por outros usuários, que podem deixar comentários sobre a qualidade e a utilidade das atividades. O acesso a essas funcionalidades exige que o usuário esteja registrado no site.

Objetivo: O Laboratório de Atividades visa proporcionar um espaço interativo e colaborativo para a criação e compartilhamento de recursos educacionais. Ele facilita a publicação e a avaliação de materiais didáticos, incentivando a participação ativa dos usuários e a melhoria contínua dos conteúdos oferecidos.


## 💻 Uso do Site

Nesta seção, abordaremos como o usuário pode navegar e interagir com o site Atomic Adventures. Você encontrará descrições das principais páginas, orientações sobre como utilizar as funcionalidades disponíveis, e dicas para maximizar sua experiência no site.

### Base do Site

#### Cabeçalho e Rodapé

O site conta com dois elementos fundamentais para a navegação: o Cabeçalho (header) e o Rodapé (footer). Ambos estão presentes em todas as páginas do site, garantindo fácil acesso às principais áreas de navegação e links importantes.

 - **Cabeçalho:**

	![Cabeçalho](.site_images/cabeçalho(header).png)

	- **Logo**: A logo do site é um elemento visual que também funciona como um link para a página principal. Ela foi estilizada para ter um caráter único e acolhedor, refletindo a identidade do projeto.

	- **Área de navegação**: Nesta seção, os usuários encontram links para as principais páginas do site, como a Tabela Periódica, Atividades, e as políticas do site. A navegação é simples e direta, facilitando o acesso a diferentes partes do site.

	- **Controle de usuário**: Essa área oferece acesso rápido aos links de login e cadastro. Para usuários autenticados, o controle de usuário se expande, permitindo acesso ao perfil e às publicações feitas pelo próprio usuário.

 - **Rodapé**:

	![Rodapé](.site_images/rodape(footer).png)

	- **Contato**: Esta seção inclui informações de contato, como email, telefone, e links para redes sociais (Instagram e LinkedIn). É uma forma de manter a comunicação aberta com a comunidade e os visitantes do site.

	- **Navegação**: O rodapé também contém links para as principais seções do site, como a Tabela Periódica, Atividades, e a página de cadastro. Esses links oferecem uma navegação rápida para áreas essenciais.

	- **Políticas do Site**: Nesta parte, estão disponíveis links para as políticas de privacidade, termos de uso, e aviso legal, garantindo que os usuários tenham fácil acesso às informações legais e de privacidade do site.

### App: Tabela Periódica (table_elements)

#### 1. Página Principal

A página principal do site funciona como uma "landing page", oferecendo uma introdução clara ao propósito do site e suas principais funcionalidades. Logo no início, o usuário encontra a Introdução, uma seção de destaque que o convida a explorar o site.

![imagem inical do site](.site_images/pagina_inicial.png)

 - **Introdução**: Esta seção contém uma breve descrição do site, acompanhada de um botão que direciona o usuário diretamente à Tabela Periódica, o tema central do site.

 - **Outras Área de Exploração0**: Além da tabela periódica, o site também tem como objetivo, explorar demais áreas da ciências, como a física e biologia. Na qual haverá páginas dedicadas a ensinamentos sobre cada assunto. (ainda não desenvolvido)

 - **Sobre o site**: Nesta seção, o site apresenta e enfatiza seus principais objetivos e propostas para a comunidade, que são:

	> "Facilitar o Acesso ao Conhecimento Científico";

	> "Fomentar a Colaboração e a Contribuição da Comunidade";

	> "Estimular a Criatividade e o Interesse pela Ciência";

	> "Promover a Educação Interativa e Prática".

#### 3. Tabela Periódica

A página da Tabela Periódica, temática principal do site, oferece uma apresentação rápida dos elementos químicos. Ela foi projetada para ser simples e intuitiva, permitindo aos usuários acessar rapidamente as informações mais relevantes sobre cada elemento.s

##### Visualização da Tabela

A tabela é exibida em um formato tradicional, com cada elemento apresentado em seu respectivo bloco. As informações essenciais disponíveis para cada elemento incluem:

 - Nome do Elemento

 - Número Atômico

 - Símbolo Químico

 - Massa Atômica

![Tabela Periodica](.site_images/tabela_periodica.png)

##### Campo de pesquisa

Existem duas opções de visualização dos elementos: em formato de tabela e em formato de lista. Na página da tabela, há um campo de busca que permite ao usuário pesquisar um elemento pelo nome ou número atômico. Essa pesquisa direciona o usuário para uma página que apresenta os elementos no formato de lista.

##### Páginas Individuais dos Elementos:

Além da visão geral fornecida na tabela, cada elemento químico possui uma página própria, onde são apresentadas informações detalhadas sobre o elemento, organizadas nas seguintes seções:

![Detalhes de um emento](.site_images/descricao_elemento.png)

 - **Cabeçalho do Elemento**: Inclui o Nome, Classificação, Número Atômico, Símbolo e Massa Atômica.

 - **Botões de Navegação**: Permitem ao usuário navegar facilmente entre o elemento anterior e o próximo na tabela.

 - **Introdução do Elemento**: Apresenta uma descrição geral do elemento e uma imagem representativa.

 - **Sobre os Elétrons**: Fornece detalhes sobre a quantidade de partículas subatômicas (prótons, elétrons e nêutrons), a representação do átomo no modelo de Bohr e a distribuição dos elétrons nas camadas eletrônicas.

 - **Propriedades Físicas**: Inclui informações como Peso Atômico, Densidade, Ponto de Fusão, Ponto de Ebulição e Estado Físico.

 - **Propriedades Atômicas**: Apresenta a configuração eletrônica e as variações de íons do elemento.

 - **História e Descoberta**: Relata a história do elemento e como ele foi descoberto.

 - **Propriedades Químicas**: Descreve as propriedades químicas do elemento, incluindo sua reatividade e compostos comuns.

 - **Aplicações**: Explica os usos do elemento na indústria, na ciência e no cotidiano.

 - **Fatos Interessantes**: Traz curiosidades e informações adicionais sobre o elemento.

 - **Referências**: Lista os artigos, sites e livros utilizados para a pesquisa das informações apresentadas.

#### 4. Políticas do Site

O site conta com uma página única que determina as políticas do site, separado pelas sessões de Políticas de Privacidade, Termos de Uso e Aviso Legal.

**Políticas de Privacidade**:

A seção de Políticas de Privacidade detalha como o site Atomic Discoveries coleta, utiliza e protege as informações pessoais dos usuários. As informações são usadas para gerenciar contas, melhorar serviços e enviar comunicações. O site adota medidas de segurança para proteger os dados, não os compartilhando com terceiros, exceto por motivos legais. Além disso, os usuários têm o direito de acessar, corrigir ou excluir suas informações pessoais, bem como gerenciar e solicitar a remoção de conteúdos postados.

**Termos de Uso**:

Esta seção aborda as regras que os usuários devem seguir ao utilizar o site Atomic Discoveries. Ela inclui orientações sobre a criação e manutenção de contas, uso responsável do conteúdo e do site, e proteção da propriedade intelectual. Também são abordadas as responsabilidades dos usuários em relação ao conteúdo que publicam e as condições sob as quais o site pode modificar esses termos. Além disso, a seção explica que o site pode conter links para terceiros, cujos conteúdos não são de responsabilidade do Atomic Discoveries.

**Aviso Legal**:

Esta seção esclarece que o conteúdo do site Atomic Discoveries é exclusivamente para fins informativos e educacionais, sem garantias de precisão ou adequação. O site e seus operadores não se responsabilizam por danos decorrentes do uso das informações fornecidas. O Aviso Legal também destaca que o conteúdo de terceiros, como links e informações de usuários, não é de responsabilidade do site. Além disso, a seção explica que o uso do site não estabelece qualquer relação profissional e que o conteúdo pode ser alterado sem aviso prévio.

### App: Usuários (users)

O app Users é um componente do site que gerencia todas as funcionalidades relacionadas aos usuários. Ele permite a criação e manutenção de perfis de usuários, oferecendo recursos para registro, login, atualização de informações pessoais, e gerenciamento de perfis, incluindo a atualização de fotos de perfil. Além disso, o app controla o acesso a páginas restritas do site, como dashboards personalizados, e possibilita futuras expansões para funcionalidades como atividades salvas e interações entre usuários. Ele foi projetado com foco na segurança e usabilidade, integrando autenticação robusta e opções de personalização para melhorar a experiência do usuário.

#### Gerenciamento de Cadastro e Autenticação

A funcionalidade de Gerenciamento de Cadastro e Autenticação no app Users é responsável por todas as etapas essenciais do processo de registro e autenticação dos usuários no site.

**Cadastro de Usuário**

Durante o cadastro, o sistema exige que o usuário forneça informações básicas, como Nome, Sobrenome, Nome de Usuário, E-mail e Senha. Para garantir a precisão na criação da senha e reduzir a chance de erros, o formulário de cadastro inclui dois campos de senha, onde o usuário deve digitar a senha escolhida em ambos os campos. O sistema compara esses valores para verificar se são idênticos, impedindo o registro caso haja discrepância. Além disso, o processo de cadastro inclui uma etapa de confirmação de aceitação dos Termos de Uso do site. O usuário deve marcar uma opção específica que indica sua concordância com os termos antes de prosseguir, garantindo que todos os usuários estejam cientes das políticas do site.

**Autenticação de Usuário**

Após o cadastro bem-sucedido, o usuário pode realizar o login no site. A autenticação é feita verificando as credenciais fornecidas (Nome de Usuário e Senha) contra as armazenadas no banco de dados, assegurando que somente usuários registrados e autenticados possam acessar as funcionalidades protegidas do site.

**Logout Seguro**

Para finalizar a sessão, o app oferece uma funcionalidade de logout que permite ao usuário sair de sua conta de forma segura. O logout encerra a sessão ativa e limpa as informações de autenticação do navegador, garantindo que nenhum dado sensível permaneça acessível após a saída.

Todo esse processo é crucial para assegurar que apenas usuários autenticados tenham acesso a áreas restritas do site, mantendo a segurança e a integridade da plataforma.

#### Gerenciamento de Perfil

O Gerenciamento de Perfil no app Users oferece aos usuários a capacidade de modificar suas informações pessoais diretamente através do site. Caso necessitem corrigir algum erro cometido durante o cadastro ou atualizar suas informações, os usuários podem alterar dados como Nome, Sobrenome, Nome de Usuário, E-mail, Foto de Perfil e Senha. Essa funcionalidade é essencial para garantir que as informações de cada usuário estejam sempre atualizadas e precisas.

Atualmente, o sistema permite a troca de senha diretamente no perfil, mas ainda não inclui uma opção para redefinir a senha em caso de esquecimento. Esse recurso está em fase de desenvolvimento e será implementado no futuro, garantindo uma experiência ainda mais completa e segura para os usuários.

#### Gerenciamento de Atividades

A funcionalidade de Gerenciamento de Atividades no app Users permite aos usuários a administração completa das atividades que eles criaram no site. Esta área é acessível diretamente através do perfil do usuário, oferecendo um controle centralizado sobre o conteúdo gerado por eles.

**Acesso e Edição de Atividades**

Os usuários podem visualizar uma lista de todas as atividades que criaram, organizadas em uma interface intuitiva. Cada atividade inclui opções para edição e exclusão. O usuário pode selecionar qualquer atividade da lista para modificá-la, o que permite atualizar detalhes como título, descrição e outros campos específicos.

**Exclusão de Atividades**

Além da edição, o usuário tem a opção de excluir atividades. A exclusão remove permanentemente a atividade do sistema. A confirmação de exclusão é necessária para evitar remoções acidentais, garantindo que o usuário esteja ciente de que a ação é irreversível.

### App: Laboratório de Atividades (learn_lab)

O app Learn Lab é uma plataforma desenvolvida para fomentar a criação, publicação e compartilhamento de atividades educacionais interativas, com um foco especial em ciências. Este app oferece um ambiente onde usuários podem explorar e contribuir com atividades didáticas que abrangem várias disciplinas.

#### Acesso e Funcionalidades

 - **Acesso Público**: A página do Learn Lab e as atividades criadas pela comunidade são acessíveis publicamente, sem a necessidade de autenticação. Isso permite que qualquer visitante explore as atividades disponíveis sem precisar se registrar ou fazer login.

 - **Funcionalidades para Usuários Autenticados**: A autenticação no site desbloqueia funcionalidades adicionais para usuários registrados. Esses recursos incluem:

 - **Criação de Atividades**: Usuários autenticados podem criar e publicar suas próprias atividades educacionais, preenchendo formulários com informações detalhadas como título, descrição, matéria e arquivos adicionais.

 - **Edição de Atividades**: Após a publicação, os usuários têm a capacidade de editar suas atividades para atualizar ou corrigir informações.

 - **Avaliação e Comentários**: Usuários autenticados podem avaliar e comentar sobre atividades criadas por outros usuários, oferecendo feedback e contribuindo para a melhoria do conteúdo disponível.

#### Configuração do app

O app oferece uma estrutura para criação, gerenciamento e pesquisa de atividades educacionais. Aqui está um resumo das principais características e funcionalidades do aplicativo:

 - **Estrutura das Atividades**

Cada atividade criada no Learn Lab inclui os seguintes campos:

 - **Título**: Nome da atividade.

 - **Descrição**: Explicação detalhada sobre o propósito e os objetivos da atividade.

 - **Conteúdo**: Detalhes adicionais e instruções relacionadas à atividade.

 - **Matéria**: Área temática à qual a atividade está associada.

 - **Turma**: Nível escolar ou série para a qual a atividade é apropriada.

 - **Arquivo** PDF: Documento indexado pelo usuário que pode fornecer materiais adicionais ou recursos complementares.

 - **Pesquisa e Navegação**
	O app oferece algumas opções de pesquisa para facilitar a localização de atividades:

	- **Pesquisa por Nível de Turma**: Permite filtrar atividades com base no nível escolar.

	- **Pesquisa por Matéria**: Facilita a busca por atividades relacionadas a disciplinas específicas.

	- **Campo de Busca Geral**: Disponível no topo da página, permite pesquisar atividades usando termos presentes no título, descrição e conteúdo.

 - **Processo de Submissão e Aprovação**

	- **Envio e Aprovação**: Após o envio de uma atividade, ela não é imediatamente exposta à comunidade. Em vez disso, a atividade passa por uma revisão por um moderador para garantir que está em conformidade com as diretrizes do site.

	- **Alterações Antes da Aprovação**: Durante o período de revisão, os usuários podem modificar a atividade conforme necessário.

	- **Alterações Após Aprovação**: Se um usuário desejar modificar uma atividade após sua aprovação, será informado de que a atividade passará por uma nova análise. Isso assegura que as alterações continuem a respeitar as diretrizes do site.

 - **Sistema de Avaliação**

	- **Avaliação por Estrelas**: Cada usuário pode deixar uma avaliação de uma atividade com valores de 1 a 5. Esses valores são representados por estrelas, estilizados por CSS

	- **Comentário Opcional**: Juntamente com a nota, o usuário pode adicionar um comentário sobre a atividade. Este campo é opcional.

	- **Limitação de Avaliações**: Cada usuário é permitido a uma única avaliação por atividade, garantindo que o feedback seja consistente e controlado.

	- **Edição e Exlusão**: O usuário poderá editar ou excluir sua avalição caso seja necessário.

#### Estrutura Visual do App Learn Lab

Ao acessar o Learn Lab através do cabeçalho (header) ou rodapé (footer) do site, os usuários são direcionados para a página de lista de atividades, que serve como a página principal do aplicativo. Aqui estão os detalhes sobre a estrutura visual e funcional da página:

**Página de Lista de Atividades**

 - **Exibição Principal**: A página lista as atividades criadas pelos usuários, proporcionando uma visão geral acessível das opções disponíveis.

 - **Card de Atividade**

	- **Informações Básicas**: Cada atividade listada na página principal é representada por um card que exibe informações essenciais. Essas informações incluem:

		- **Título**: O nome da atividade.
		- **Turma**: O nível de ensino ou série para o qual a atividade é destinada.
		- **Matéria**: A disciplina associada à atividade.
		- **Conteúdo**: Um resumo breve ou tópico principal abordado pela atividade.
		- **Autor**: O nome do usuário que criou a atividade.

	- **Imagem de Pré-visualização**:

		- Uma imagem da primeira página do PDF enviado também é exibida no card. Esta imagem serve como uma pré-visualização visual da atividade.
		- No momento, essa funcionalidade ainda está em desenvolvimento, e a geração dessa imagem a partir do PDF será implementada no futuro.

 - **Limitação de Itens**: A view é configurada para exibir apenas 20 atividades por vez, garantindo uma navegação organizada e evitando sobrecarga de informações.

 - **Paginação**:

	- **Configuração de Paginação**: Para gerenciar a visualização de atividades em excesso, foi implementada uma paginaçao simples. Os usuários podem navegar entre diferentes páginas para acessar mais atividades conforme necessário.

	- **Experiência do Usuário**: A paginação é projetada para ser intuitiva e fácil de usar, permitindo que os usuários se movam entre as páginas sem dificuldades.

 - **Busca de Atividades**

	- **Filtro de Atividades**: Nos cards de atividade, os itens de Turma e Matéria são interativos. Ao clicar em qualquer um desses itens, o usuário será redirecionado para uma página que exibe exclusivamente as atividades relacionadas àquela Turma ou Matéria específica. Por exemplo, ao clicar em "Matemática" em um card, o usuário será levado a uma página que lista apenas as atividades de Matemática disponíveis no site.

	- **Campo de Busca Global**:

		- Localizado no topo da página principal do Learn Lab, o campo de busca permite ao usuário realizar pesquisas mais detalhadas.
		- A busca pode ser realizada utilizando termos contidos no título, descrição, ou conteúdo das atividades, proporcionando uma maneira rápida e eficiente de encontrar atividades relevantes.

**Página de Detalhes de Atividade**
A Página de Detalhes de Atividade é projetada para fornecer uma visão completa e aprofundada sobre cada atividade disponível no app Learn Lab. Aqui estão os principais componentes e funcionalidades desta página:

 - **Descrição da Atividade**: Além das informações básicas, a descrição da atividade é exibida nesta página, oferecendo uma explicação mais detalhada e contexto adicional fornecido pelo criador da atividade. Isso ajuda os usuários a entenderem melhor o propósito e a aplicação da atividade.

 - **Botão de Download**: Um botão de download está disponível nesta página, permitindo que os usuários baixem o arquivo PDF da atividade diretamente para seus dispositivos. Essa funcionalidade facilita o acesso e o uso offline das atividades.

 - **Sessão de Avaliações**: Logo abaixo dos detalhes da atividade, há uma sessão dedicada às avaliações feitas por outros usuários. Essa área inclui:
	
	- **Formulário de Avaliação**: Exclusivo para usuários autenticados, o formulário permite que os usuários avaliem a atividade com uma nota em formato de estrelas (de 1 a 5) e deixem um comentário opcional.

	- **Gestão da Avaliação**: Após submeter uma avaliação, o usuário tem a opção de editar ou excluir sua avaliação, garantindo que suas impressões sobre a atividade possam ser ajustadas conforme necessário.

	- **Botão de Denunciar**: Para garantir que as avaliações sigam as diretrizes do site, há um botão de denúncia associado a cada avaliação. Este recurso permite que outros usuários sinalizem avaliações que possam conter conteúdo impróprio, ofensivo, ou que violem as políticas do site. As denúncias serão revisadas por moderadores para garantir a conformidade com as regras da comunidade.

**Página de Criação e Edição de Atividades**
A Página de Criação e Edição de Atividades é onde os usuários podem criar suas novas atividades ou editar essas atividades já existentes. Embora compartilhem a mesma estrutura básica, essas páginas possuem algumas diferenças importantes quanto ao uso e à aparência.

 - **Página de Criação**

	- **Instruções Guiadas**: Para auxiliar os usuários na criação de atividades eficazes, esta página oferece orientações detalhadas. Essas instruções incluem recomendações sobre como preencher corretamente cada campo do formulário e dicas para criar um PDF bem-estruturado e de fácil compreensão. O objetivo é garantir que as atividades criadas estejam em conformidade com as diretrizes do site e mantenham uma boa qualidade.

	- **Formulário de Criação**: O formulário é simples e direto, solicitando informações essenciais como Título, Descrição, Conteúdo, Matéria, Turma, e o arquivo PDF. Essas informações ajudarão a categorizar e exibir a atividade corretamente no site.

 - **Página de Edição**:
	
	- **Campos Pré-Preenchidos**: Ao acessar a página de edição, todos os campos do formulário estarão automaticamente preenchidos com as informações previamente fornecidas pelo usuário ao criar a atividade. Isso facilita a edição, permitindo que o usuário altere apenas os campos que deseja modificar, sem a necessidade de recomeçar todo o processo.
	
	- **Revisão de Atividades Editadas**: Conforme mencionado anteriormente, se a atividade que está sendo editada já tiver sido aprovada anteriormente, qualquer alteração feita pelo usuário irá requerer uma nova análise por parte dos moderadores do site. Isso é essencial para garantir que as modificações não comprometam as diretrizes e a qualidade do conteúdo disponibilizado na plataforma.

  
## ✒️ Próximas Atualizações

Embora o site já tenha as funcionalidades essenciais prontas e funcionando, ainda há várias adições e melhorias planejadas para aprimorar a experiência do usuário e expandir as capacidades do site. Entre as próximas atualizações esperadas, estão:

- **Atualizações de Backend**:
    - **"Esqueci minha senha"**: Desenvolver uma view que permita ao usuário alterar sua senha a partir do e-mail, em caso de esquecimento ou perda da senha.
	
    - **Imagem do PDF**: Desenvolver um script que transforma a primeira folha do PDF em uma imagem para ser mostrada no template de atividades.

	- **Visualização de Perfil**: Implementação de uma view personalizada que permite acessar as informações básicas de um usuário, como nome, sobrenome e biografia. Além disso, possibilita a visualização das atividades criadas por esse usuário.

- **Atualizações de Frontend**:
    - **Expansão de Conteúdo**: Adicionar mais detalhes e informações sobre os elementos químicos para enriquecer o conteúdo disponível e oferecer uma visão mais abrangente. Incluir links para sites que promovem software de jogos educativos e simuladores de experiências.

    - **Otimização para Dispositivos Móveis**: Melhorar a responsividade do site para garantir uma experiência fluida em todos os dispositivos, incluindo smartphones e tablets.


Estas atualizações visam tornar o site ainda mais útil e agradável para os usuários, e estamos ansiosos para implementar essas melhorias nas próximas versões.


## 📜 Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](./LICENSE) para mais detalhes.


## 💬 Contato

Se você tiver dúvidas, sugestões ou encontrar problemas, sinta-se à vontade para entrar em contato.

Você pode me encontrar e me contatar através das minhas redes sociais na [OverView do GitHub](https://github.com/Ric002x).

Agradeço pelo seu interesse no projeto! 😁