# deploy-cloud
Configuração de servidores cloud usando Fabric3

# Deploy Cloud

Esse projeto visa configurar máquinas em cloud usando python Fabric3.

## Como desenvolver?
1. Clone o repositório
2. Crie um virtualenv com Python 3.x
3. Ative o virtualenv
4. Instale as dependências

```
git clone https://github.com/weibemoura/deploy-cloud.git
conda create -n deploy python=3.6.5 pip
source activate deploy
cd deploy
pip install -r requirements.txt
```

# Instalação

É necessário criar um arquivo .env antes de rodar qualquer comando
Ex: env/local.env

1. PostgreSQL 10.x
```
./contrig/update.sh
./contrig/postgresql.sh
```
2. PgBouncer 1.8.x
```
./contrig/update.sh
./contrig/pgbouncer.sh
```
3. Firewalld 0.4.4
```
./contrig/update.sh
./contrig/firewalld.sh
```
4. Nginx 1.12.2
```
./contrig/update.sh
./contrig/nginx.sh
```
5. Redis
```
./contrig/update.sh
./contrig/redis.sh
```
6. Miniconda
```
./contrig/update.sh
./contrig/miniconda.sh
```