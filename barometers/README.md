# sensores_sht31_ms5803

<b><h4>BAROMETERS</h4></b>
O diretório **Barometers** é onde está guardado o código de comparação entre dois sensores MS5803, que recebe os dados de Temperatura e Pressão.
Dentro desse diretório, encontramos o código na linguagem Python.

<h1></h1>
<h5>Importante!!</h5> 
Para que haja a comparação entre os 2 sensores : \n
Bar1 = 0x77 - > Barômetro Nacional \n
Bar2 = 0x76 - > Barômetro Internacional \n
Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles: \n
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento). \n
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelos sensores. \n
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores \n
 
*Necessário mudar caminho dos arquivos .TXT para que possam ser gravados corretamente*
<h1></h1>
