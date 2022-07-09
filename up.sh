FILE=.env

if [ ! -e $FILE ]
then
    echo "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > $FILE
    echo "Configuração salva no arquivo ${FILE}"
fi

docker-compose up airflow-init && docker-compose up -d --build