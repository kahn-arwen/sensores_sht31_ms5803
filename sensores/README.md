<b><h4>SHT_MS.PY</h4></b>
O código a seguir realiza a leitura dos 2 sensores (SHT31 + MS5803), podendo coletar as informações de Temperatura, Umidade e Pressão. E recebendo informações, ele grava nos seguintes arquivos:
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento).
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelos sensores.
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores

<h1></h1>
<h5>Importante</h5> Mudar caminho dos arquivos .TXT para que possam ser gravados corretamente.
<h1></h1>



<b><h4>SENSORES.PY</h4></b>
O código a seguir realiza a leitura dos 2 sensores. Caso 1 não esteja sendo reconhecido, ele tentará ler somente as informações do outro sensor restante, 
e escrevendo suas informações recebidas em arquivos Backup, sendo eles:
- SHT -> Sensor de temperatura e umidade
- MS -> Sensor de temperatura e pressão
- Sensores -> Ambos sensores sendo lidos juntos (SHT31+MS5803)

e tendo como parâmetro Sec ( Escreve a cada 5 segundos ) - Hour ( Escreve de 1 em 1 hora ) - Day ( Escreve de 1 em 1 dia(24h) )

Caso não consiga ler ambos, ele enviará uma mensagem mostrando qual erro ocorreu.
<h2> !!! </h2>
<p>É necessário os dar os seguintes comandos no terminal para que o cógido funcione  </p>
<code>pip install ms5803py</code>
<code>sudo pip3 install adafruit-circuitpython-sht31d</code>
<code>pip install smbus</code>
<code>sudo apt-get install i2c-tools</code>
