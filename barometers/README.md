<h1></h1>
<h2> !!! </h2>
<p>É necessário os dar os seguintes comandos no terminal para que o código funcione corretamente </p>
<code>pip install ms5803py</code>
<code>pip install smbus</code>
<code>sudo apt-get install i2c-tools</code>
<s>Não esqueça de verificar se a interface I2C está habilitada</s>

<h1></h1>
<b><h3>BAROMETERS</b></h3>
O diretório **Barometers** é onde está guardado o código de comparação entre dois sensores MS5803, que recebe os dados de Temperatura e Pressão.
Dentro desse diretório, encontramos o código na linguagem Python.

<h1></h1>
<h5>Importante!!</h5> 
Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles: <br />
- <b>SEC_BACKUP.TXT</b> -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento). <br />
- <b>HOUR_BACKUP.TXT</b> -> Escreve de 1 em 1 hora a leitura realizada pelos sensores. <br />
- <b>DAY_BACKUP.TXT</b> -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores <br /> <br />

<p> Para que haja a distinção entre os 2 sensores : <br />
Bar1 = 0x77 - > Barômetro Nacional <br />
Bar2 = 0x76 - > Barômetro Internacional <br /><br />
<b><i>Obs: Foram criados os arquivos: _bar1, _bar2 onde há as informações separadas de cada sensor. Porém foi criado o arquivo que contém os dados recebidos por ambos (hour_backup.txt, day_backup.txt)</i></b>

<i>**Necessário mudar caminho dos arquivos .TXT para que possam ser gravados corretamente </i>
