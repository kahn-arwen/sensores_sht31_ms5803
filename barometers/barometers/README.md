
<b><h3>BAROMETERS</b></h3>
O diretório **Barometers** é onde está guardado o código de comparação entre dois sensores MS5803, que recebe os dados de Temperatura e Pressão.
Dentro desse diretório, encontramos o código na linguagem Python.
<h1></h1>
<h5>Correção do Código:</h5>
<p>Foi acrescentado no código as variáveis: </p>
<p>- 'hour' = Onde você colocará o horário desejado para receber os dados recolhidos durante o dia (24h) </p>
<p>- 'hours' = Definição de horários no formato hh:mm:ss para retorno de dados de 1 em 1 hora (exata)</p>
<h1></h1>
<h5>Importante!!</h5> 
Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles: <br />
- <b>SEC_BACKUP.TXT</b> -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento). <br />
- <b>HOUR_BACKUP.TXT</b> -> Escreve de 1 em 1 hora a leitura realizada pelos sensores. <br />
- <b>DAY_BACKUP.TXT</b> -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores <br /> <br />

<p> Para que haja a distinção entre os 2 sensores : <br />
Bar1 = 0x77 - > Barômetro Nacional <br />
Bar2 = 0x76 - > Barômetro Internacional <br /><br />
<b><i>Obs: Foram criados os arquivos: _bar(1/2)
<h1></h1>
<h2> !!! </h2>
<p>É necessário os dar os seguintes comandos no terminal para que o cógido funcione  </p>
<code>pip install ms5803py</code>
<code>pip install smbus</code>
<code>sudo apt-get install i2c-tools</code>


