<h1></h1>
<h2> !!! </h2>
<p>É necessário os dar os seguintes comandos no terminal para que o código funcione corretamente  </p>
<code>pip install ms5803py</code>
<code>pip install smbus</code>
<code>sudo apt-get install i2c-tools</code>
<h1></h1>
<b><h3>MS5803.PY</h3></b>
O código a seguir faz a leitura do sensor MS5803, possibilitando a captura dos dados sobre : Temperatura e Pressão.
Escrevendo as informações adquiridas nos seguintes arquivos:
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelo sensor (Bom para monitoramento).
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelo sensor.
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelo sensor
<h1></h1>
<h5>Importante</h5> Mudar caminho dos arquivos .TXT para que possam ser gravados corretamente.

