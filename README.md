# Sistema de Registro de Pesagens
Este aplicativo Django registra pesagens de veículos utilizando integração com balanças Toledo e câmeras Hikvision. Ele automatiza a captura de pesos e imagens, garantindo controle completo sobre as pesagens de entrada e saída.

Funcionalidades
Registro de Pesagem de Entrada:

Captura automática do peso através da integração com a balança Toledo.
Captura de imagem associada utilizando a câmera Hikvision.
Inserção manual da placa do veículo e número do documento.
Armazenamento do peso no banco de dados e da imagem localmente.
Registro de Pesagem de Saída:

Procedimento semelhante à pesagem de entrada.
Inserção dos mesmos dados da entrada (placa e documento).
Geração de Ticket de Pesagem:

Consolida as informações das pesagens de entrada e saída.
Calcula e exibe a diferença de peso.
Permite exportar o ticket para registro ou entrega ao cliente.
Pré-requisitos
Django para o backend.
Banco de dados compatível (ex.: MySQL ou PostgreSQL).
Integração configurada com:
Balança Toledo para captura automática de pesos.
Câmera Hikvision para captura de imagens.
Instalação
Clone este repositório:

bash
Copiar código
git clone https://github.com/seuusuario/seurepositorio.git
Instale as dependências do projeto:

bash
Copiar código
pip install -r requirements.txt
Configure o banco de dados no arquivo settings.py.

Aplique as migrações:

bash
Copiar código
python manage.py migrate
Configure a integração com os dispositivos:

Balança Toledo: Instruções de integração.
Câmera Hikvision: Instruções de integração.
Inicie o servidor:

bash
Copiar código
python manage.py runserver
Uso
Registro de Pesagem de Entrada:

Insira os dados necessários (placa, documento).
Confirme o peso capturado automaticamente.
Salve o registro.
Registro de Pesagem de Saída:

Localize o registro de entrada correspondente.
Insira os mesmos dados (placa, documento).
Confirme o peso capturado.
Salve o registro.
Gerar Ticket de Pesagem:

Acesse a opção de geração de ticket.
Revise os dados consolidados (entrada, saída, diferença de peso).
Exporte o ticket.
Estrutura do Projeto
Modelos:

RegistroPesagem: Armazena informações de entrada e saída.
Campos principais:
placa
numero_documento
peso_entrada, data_entrada
peso_saida, data_saida
Integrações:

Balança Toledo: Comunicação via protocolo específico.
Câmera Hikvision: Captura de imagens em tempo real.
Contribuição
Contribuições são bem-vindas! Siga os passos:

Fork o repositório.
Crie um branch para suas alterações:
bash
Copiar código
git checkout -b minha-feature
Envie um Pull Request.
