# SHT31 X DS18B20
I2C & 1WIRE
<table>
<tr>
<td>
<img src="https://cdn.awsli.com.br/600x700/468/468162/produto/19414360586929efad.jpg" width=200px height=200px display=inline-block>
</td>
<td>
<img src="https://www.plexishop.it/media/catalog/product/cache/3/image/650x/040ec09b1e35df139433887a97daa66f/m/o/modulo_gy-sht30-d_sensore_digitale_di_temperatura_e_umidit_2.jpg" width=200px height=200px display= inline-block>
</td>
 </tr>
</table>
<p> <b>#Configurar a raspberry para ler ambos os sensores:</b>
<p></p><i>Não esqueça de verificar se a interface I2C e 1W estão habilitadas</i>.
<b><i>Para habilitar é necessário utilizar "raspi-config" e lá na aba "interface", habilitar</i></b>
<p>Links Importantes: </p>
- https://randomnerdtutorials.com/raspberry-pi-ds18b20-python/
- https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0


<h1></h1>
<h5>Importante!!</h5> 

Todos os códigos aqui encontrados possuem a função de escrever esses dados recebidos em arquivos backup.txt, sendo eles:
- *SEC_BACKUP.TXT* -> Escreve de 5 em 5 segundos a leitura realizada pelos sensores (Bom para monitoramento).
- *HOUR_BACKUP.TXT* -> Escreve de 1 em 1 hora a leitura realizada pelos sensores.
- *DAY_BACKUP.TXT* -> Escreve de 1 em 1 dia (24 horas) a leitura realizada pelos sensores
 
*Necessário mudar caminho dos arquivos .TXT para que possam ser gravados corretamente*
<h1></h1>


