# Apache-Airflow com docker

#### Criando a estrutura de pastas
`$ mkdir -p dags logs plugins`

#### Criando id do usuário 
`$ echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`

#### Iniciando a base de dados do Airflow
`$ docker-compose up airflow-init`

#### Subindo os serviços
`$ docker-compose up -d --build`

#### Caso o id do usuário não for criado, é necessário mudar as permissões 
`$ sudo chown -R $USER:$USER .`

#### visualizando os serviços
`$ docker ps`

#### Removendo tudo
`$ docker-compose down --volumes --remove-orphans`