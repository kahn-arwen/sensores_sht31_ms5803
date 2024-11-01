<h1></h1>
<h2> !!! </h2>
<p>É necessário os dar os seguintes comandos no terminal para que o cógido funcione  </p>
<code>pip install gspread-dataframe</code>
<code>pip install gspread oauth2client</code>
><br><br>
<i>Não esqueça de verificar se a interface I2C está habilitada</i>
<h1></h1>
Obs. Coleta.service deverá estar localizado no caminho /lib/systemd/system
<h1></h1>
<b><h3>BAROMETERS + Google Sheets</b></h3>
O diretório **Barometers** é onde está guardado o código de comparação entre dois sensores MS5803, que recebe os dados de Temperatura e Pressão.
Dentro desse diretório, encontramos o código na linguagem Python e juntamente com a implementação da lógica 
  onde há a gravação de dados automática na planilha do Google Sheets, possibilitando a análise de dados entre o barômetro 1 e o barômetro 2.
<h1></h1>
<h5>Importante!!</h5> 
Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles: <br />
- <b>SEC_BACKUP.TXT</b> -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento). <br />
- <b>HOUR_BACKUP.TXT</b> -> Escreve de 1 em 1 hora a leitura realizada pelos sensores. <br />
- <b>DAY_BACKUP.TXT</b> -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores <br /> <br />

<p> Para que haja a distinção entre os 2 sensores : <br />
<b><i>Obs: Foram criados os arquivos e variáveis: _bar(1/2)
<ul>
<li>Bar1 = 0x77 - > Barômetro Nacional</li>
<li>Bar2 = 0x76 - > Barômetro Internacional</li>
</ul>



