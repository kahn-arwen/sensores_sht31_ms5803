<h1></h1>
<h2> !!! </h2>
<p>É necessário os dar os seguintes comandos no terminal para que o cógido funcione  </p>
<code>pip install adafruit-circuitpython-sht31d</code>
<code>pip install smbus</code>
<code>sudo apt-get install i2c-tools</code>
<h1></h1>
<b><h3>BACKUP_DIA_HORA.C</h3></b>
<b><h3>BACKUP_PYTHON.PY</h3></b>
Ambos os códigos a seguir faz a leitura do sensor SHT31, possibilitando a captura dos dados sobre : Temperatura e Umidade.
Escrevendo as informações adquiridas nos seguintes arquivos:
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelo sensor (Bom para monitoramento).
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelo sensor.
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelo sensor
<h1></h1>
<h5>Importante</h5> Mudar caminho dos arquivos .TXT para que possam ser gravados corretamente.

