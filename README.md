Atena
========

Setup do Ambiente local
~~~~~~~~~~~~~~~~~~~~~~~

Antes de mais nada, é necessário a instalação dos seguintes requisitos de sistema:

- `Oracle Instant Client <https://www.oracle.com/br/database/technologies/instant-client/linux-x86-64-downloads.html>`_

- `Docker <https://docs.docker.com/install/linux/docker-ce/ubuntu/>`_

Cada desenvolvedor deve ter seu usuário. Peça ao administrador do projeto a criação de
um usuário e a inclusão do usuário no grupo local ``docker``. Cada usuário deve ter
acesso via SSH, conforme `as instruções aqui <https://confluence.atlassian.com/bitbucket/set-up-an-ssh-key-728138079.html#SetupanSSHkey-ssh1>`_.

Também é recomendado para desenvolvimento o uso do `Visual Studio Code <https://code.visualstudio.com/download>`_ com a
extensão `Remote-SSH <https://code.visualstudio.com/download>`_ configurada.

Uma vez com acesso à VM de desenvolvimento, instale o `Miniconda3 Linux 64-bit <https://docs.conda.io/en/latest/miniconda.html>`_
e crie uma ambiente com *Python 3.11* chamado ``atena``. Neste ambiente, instale as
dependencias de desenvolvimento via ``pip`` em ``requirements.dev.txt``

.. code-block:: bash

   $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   $ bash Miniconda3-latest-Linux-x86_64.sh

   ## log out, then login to activate base environment ##

   (base) $ conda create -n atena python==3.11
   (base) $ conda activate atena
   (atena) $ git clone git@gitlab.ipirangacloud.com:analytics/bcg-products/atena.git
   (atena) $ pip install -r requirements.dev.txt


Criação de usuários na VM de desenvolvimento
############################################

Para criar usuários, você precisa de acesso via ``sudo``.

Na máquina local **do novo usuário**, instale o `Git Bash <https://gitforwindows.org/>`_ e
gere um conjunto de chaves com o comando ``ssh-keygen``. A chave pública estará localizada
em ``~/.ssh/id_rsa.pub``

Edite/crie o arquivo ``~/.ssh/config`` na pasta de usuário local e adicione os
parâmetros abaixo, substituindo o ``<username>``:

::

   Host ipiranga
      HostName 191.238.214.62
      Port 2222
      User <username>
      ForwardAgent yes
      DynamicForward 9998
      LogLevel QUIET

Na VM, execute o script ``setup/add-user.sh <username>`` e siga as instruções. No final será gerado
uma nova chave SSH em ``/home/<username>/.ssh/id_rsa.pub`` que deve ser adicionada ao
GitLab para permitir operações Git sem usuário/senha.


Removendo usuários na VM de desenvolvimento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para remover o usuário:

::

   $ sudo deluser <username>

Para apagar a pasta do usuário

::

   $ sudo rm -rf /home/<username>


Arquivo ``.env``
~~~~~~~~~~~~~~~~

Copie o arquivo ``env_sample`` para ``.env`` e edite conforme os comentário no arquivo.

As credenciais são gerenciadas usando o serviço **Azure Key Vault**. Como desenvolvedor,
você precisa apontar a instancia correta do serviço no arquivo ``.env``. O serviço
*Key Vault* é criado e gerido pelo Terraform. Os *secrets* que devem fazer parte do
KeyVault estão descritos no arquivo ``env_sample``. E são geridos pela equipe de
TI. **Nota:** O acesso aos `secrets` é gerido não pelo RBAC mas via
*Access Policy* do *Key Vault*.

Deve-se definir também o ``BASE_FOLDER``, que é o local onde os arquivos intermediários
e saídas dos modelos serão gravados. Em *lab*, recomenda-se que cada
desenvolvedor tenha seu próprio container. Em *dev* ou *prod*, esse valor é gerido por
TI/DevOps, usando os aquivos ``env_batch_dev`` e ``env_batch_prod``.


Executando comandos
~~~~~~~~~~~~~~~~~~~
Em desenvolvimento, o pipeline é executado via o *script* ``run.py``.

Os principais comandos são:

- ``list-tasks <dag>``: lista as tasks disponíveis no DAG ``<dag>``

- ``task <dag> <task>``: executa uma task ``<task>`` específica do DAG ``<dag>``

- ``docker <dag> <task>``: similar a ``task`` acima, mas executa no ambiente Docker,
  similar ao ambiente de produção.

O comand ``docker`` automaticamente faz o *build* do container e atribui uma tag
baseado no nome do usuário.

Por exemplo, para rodar o ``list-tasks pricing_rede_tasks``:

::

   ./run.py list-tasks pricing_rede_tasks


Para rodar o ``task pricing_rede_task task_collect``:

::

   ./run.py docker pricing_rede_task task_collect
   ou
   ./run.py task pricing_rede_task task_collect


Configuração
~~~~~~~~~~~~
A configuração do projeto é realizada através do **dags/config.py**.
As variavéis configuravéis estão documentadas nesse arquivo.
As variáveis tem valores escritas em código,
algumas outras pegam o valor definido nas variáveis de ambiente.

Existem 2 maneiras de alterar essas configurações:

- Alterar no próprio **dags/config.py**

- Alterar as variáveis de ambiente, para que o **dags/config.py** possa acessá-las


Atualizando/criando a documentação
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este projeto foi documentado usando **docstrings** no padrão **Google**.
Utilizando essas docstrings, usamos o Sphinx para gerar a documentação final.
Para montar a documentação na sua própria máquina, é só seguir os seguintes passos:

- Instale os requisitos de documentação:

::

   pip install -r requirements.docs.txt

- Entre na pasta docs e rode o comando do sphinx para gerar os docs:

::

   cd docs
   make html

- A documentação estará pronta quando aparecer a mensagem `Build finished. The HTML pages are in _build/html.`

- Para acessar a documentação, abra o arquivo **index.html** na pasta **docs/_build/html** no seu navegador de preferência.

Deployment (Lab)
~~~~~~~~~~~~~~~~~

Terraform scripts
#################

O deployment em Lab é gerenciado usando `Terraform <https://www.terraform.io/>`_ na
cloud Azure. Os scripts estão na pasta ``tf``.

Os scripts são organizados em 2 módulos, na pasta ``modules``:

- ``atena`` contendo infra específica para o aplicativo (KeyVault) e as definições
  de criação de *Service Principal* e *AD Group*

- ``batch`` contendo infra para setup do **Azure Batch**. A recomendação é, em produção,
  utilizar um Azure Batch compartilhado. Importane notar que, por padrão, o serviço
  batch tem quotas bem reduzidas e esta configuração inicializa *0 (zero) nodes*
  no *pool* de VMs.

Cada ambiente (lab, prod) tem sua pasta. Na pasta ``ipplab`` contém as configurações
específicas para Lab. Para aplicar a configuracão, primeiramente instale o Terraform e
o Azure CLI. Recomendamos criar um ambiente ``conda`` dedicado e instalar o pacote PIP
``azure-cli``

.. code-block:: bash

   (base) $ conda create -n azure python==3.11
   (base) $ conda activate azure
   (azure) $ pip install azure-cli


Você deve logar com um usuário/principal com permissões adequadas para executar o
script. No mínimo *Owner* em um *Resource Group*.

.. code-block:: bash

   (azure) $ az login

Daí, para aplicar as configurações:

.. code-block:: bash

   $ cd ipplab
   $ terraform init  # somente uma vez
   $ terraform apply


Job deployment scripts
######################

Existe um script ``deploy.py`` na raíz do projeto com dois comandos de deployment:

- ``./deploy.py build``: constroi e envia a imagem *Docker* para o *ACR*

- ``./deploy.py schedule-job``: atualiza as configurações do Job agendado no Azure Batch.

O script depende um arquivo ``deploy.json``, definido pelo *output* do script Terraform
na etapa anterior:

.. code-block:: bash

   (azure) $ PROJECT_HOME=$HOME/atena  # absolute path to the project
   (azure) $ terraform output -json deploy > $PROJECT_HOME/deploy.json

**Nota:** Você precisa estar com o Key Vault devidamente configurado.

Os commandos aceitam uma flag ``--help`` com detalhes dos parametros. Por exemplo,
para fazer o deployment de uma nova versão ``v0.0.1``, devemos fazer login no ACR.
Assumindo que o servidor ACR é ``ippacrlab.azurecr.io``

.. code-block:: bash

   (base)  $ conda activate azure
   (azure) $ az acr login -n

Então podemos construir e enviar a imagem:

.. code-block:: bash

   (atena) $ ./deploy.py build -v v0.0.1

Para agendar o DAG `pricing_rede_tasks` na imagem que criamos, você deve executar:

.. code-block:: bash

   (atena) $ schedule-job pricing_rede_tasks -v v0.0.1 -e env_batch_lab -r P1D -s 2020-03-15T04:00:00Z

O parâmetro ``-e`` permite incluir um arquivo com variáveis de ambiente que serão
passados para as tarefas durante a execução. Aqui usamos o arquivo ``env_batch_lab``,
que faz parte do repositório. Veja mais detalhes em ``env_sample``.

Os parâmetros ``-s`` e ``-r`` definem respectivamente a data de início das execuções
e a recorrencia e devem ser fornecido no padrão ``ISO-8601 Date/Time`` e
``ISO-8601 Duration`` (visão geral `aqui <https://docs.oracle.com/en/database/oracle/oracle-database/20/adjsn/iso-8601-date-time-and-duration-support.html>`_).
No exemplo dado, a primeira execução deve iniciar às 04h (UTC) do dia 15 de Mar de
2020, e se repetirá a cada 1 dia.


Visualizando a execução
#######################

Recomenda-se utilizar a ferramenta  `Azure Batch Explorer <https://azure.github.io/BatchExplorer/>`_
para visualizar as execuções do Azure Batch. No instante de execução, cada
*Job Schedule* cria um *Job* e, por sua vez, é composto de *Tasks*.

**Atenção:** Por padrão, os scripts Terraform **não alocam nenhuma VM** ao *Pool* de
execução no ambiente Lab para não gastar recursos acidentalmente. Para testar, lembre-se
de escalar adequadamente o *Pool* para no mínimo um nó.



Organização macro do pacote dags
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- O módulo de data contém a parte relacionada a coleta/aquisição de dados.

- O módulo de features contém a parte de preprocessamento e feature engineering.

   - Esse módulo contém separações por modelos (ex: pricing_rede, demand, sales...)

- O módulo de models contém a parte de modelagem.

   - Esse módulo contém separações por modelos (ex: pricing_rede, demand, sales...)

- O módulo de visualization contém a parte de geração de arquivos para visualização e envio para usuários.

   - Esse módulo contém separações por modelos (ex: pricing_rede, demand, sales...)

Caso queira checar os módulos mais afundo, vá até a seção de Modulos.

Arvore de arquivos
#########################

::

   ├── Dockerfile
   ├── README.rst
   ├── dags                      -> Pacote principal do projeto
   │   ├── __init__.py
   │   ├── common.py             -> Objetos comuns para serem utilizados em outros modulos
   │   ├── config.py             -> Modulo com parametros gerais configuraveis do projeto
   │   ├── data                  -> Modulo de aquisicao de dados
   │   │   └── queries           -> Pasta com as queries utilizadas na coleta de dados do DW
   │   ├── demand_uf_tasks.py       -> Arquivo de tasks do modelo de demanda
   │   ├── features              -> Modulo de preprocessamento de dados e geracao de features
   │   ├── io.py                 -> Modulo para operacoes de I/O de dados
   │   ├── keyvault.py           -> Modulo para acesso as credenciais no Azure KeyVault
   │   ├── logging.py            -> Modulo de configuracao dos logs
   │   ├── models                -> Modulo de modelagem preditiva, simulacao e otimizacao
   │   ├── pricing_me_tasks.py   -> Arquivo de tasks de Pricing ME
   │   ├── pricing_rede_tasks.py -> Arquivo de tasks de Pricing Rede
   │   ├── runner.py             -> Abstracao que roda uma task
   │   ├── sales_tasks.py        -> Arquivo de tasks de Previsao de Vendas Curto Prazo
   │   ├── test_pipeline.py      -> Arquivo de tasks de teste
   │   └── visualization         -> Modulo para geracao de arquivos para
   │                                visualização e envio para usuários.
   ├── data                      -> Pasta de organizacao de dados na versao local
   │   ├── interim               -> Dados intermediarios gerados por pre-preprocessamento
   │   │                            ou features
   │   ├── predictions           -> Dados de output para uso dos dashboards e usuarios
   │   ├── processed             -> Dados utilizados na etapa de modelagem
   │   └── raw                   -> Dados brutos, como vieram da fonte
   ├── deploy.py                 -> Arquivo utilizado no deployment do projeto
   ├── entrypoint.sh             -> Entrypoint do docker
   ├── env_batch_lab             -> Arquivo de env vars do ambiente LAB
   ├── env_sample                -> Arquivo de exemplo de env vars padrao
   ├── requirements.dev.txt      -> Pacores requeridos para trabalhar no desenv. do projeto
   ├── requirements.docs.txt     -> Pacores requeridos para criar a documentacao do projeto
   ├── requirements.txt          -> Pacores requeridos para rodar o projeto
   ├── run.py                    -> Arquivo utilizado rodar tasks
   ├── setup                     -> Arquivo auxiliares para setup do docker
   └── tf                        -> Arquivos terraform
