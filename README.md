# sensores_sht31_ms5803
<h2> !!! </h2>
<p>É necessário os dar os seguintes comandos no terminal para que o código funcione corretamente  </p>
<code>pip install ms5803py</code>
<code>sudo pip3 install adafruit-circuitpython-sht31d</code>
<code>pip install smbus</code>
<code>sudo apt-get install i2c-tools</code><br><br>
<i>Não esqueça de verificar se a interface I2C está habilitada</i>
<h1></h1>
<b><h4>TEMP_UMI_SENSOR</h4></b>
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEAnJ29exhYAwGashW_eJUodFbDI3EbSVMww&s" width=400px height=40px>
<img src="https://www.plexishop.it/media/catalog/product/cache/3/image/650x/040ec09b1e35df139433887a97daa66f/m/o/modulo_gy-sht30-d_sensore_digitale_di_temperatura_e_umidit_2.jpg" width=400px height=40px>
O diretório **temp_umi_sensor** é onde está guardado os códigos referentes ao sensor SHT31, que recebe os dados de Temperatura e Umidade.
Dentro desse diretório, encontramos o código na linguagem C e Python.

<b><h4>PRESSURE_SENSOR</h4></b>
O diretório **pressure_sensor** é onde está guardado os códigos referentes ao sensor MS5803, que recebe os dados de Temperatura e Pressão.
Dentro desse diretório, encontramos o código na linguagem Python.

<b><h4>SENSORES</h4></b>
O diretório **sensores** é onde está guardado os códigos referentes aos sensores SHT31 e MS5803.
Recebendo os dados de Temperatura, Umidade e Pressão. Dentro desse diretório, encontramos o código na linguagem Python.

<b><h4>BAROMETERS</h4></b>
O diretório **Barometers** é onde está guardado o código de comparação entre dois barômetros MS5803.
Recebendo os dados de Temperatura, Umidade e Pressão. Dentro desse diretório, encontramos o código na linguagem Python.

<h1></h1>
<h5>Importante!!</h5> 

Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles:
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento).
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelos sensores.
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores
 
*Necessário mudar caminho dos arquivos .TXT para que possam ser gravados corretamente*
<h1></h1>
