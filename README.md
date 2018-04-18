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
1. PostgreSQL 10.x
2. PgBouncer 1.8.x
3. Firewalld 0.4.4
4. Nginx 1.12.2
5. Redis
6. Miniconda