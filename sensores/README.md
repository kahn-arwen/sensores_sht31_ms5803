O código a seguir realiza a leitura dos 2 sensores. Caso 1 não esteja sendo reconhecido, ele tentará ler somente as informações do outro sensor restante, 
e escrevendo suas informações recebidas em outro arquivo Backup, sendo eles:
SHT -> Sensor de temperatura e umidade
MS -> Sensor de temperatura e pressão
Sensores -> Ambos sensores sendo lidos juntos (SHT31+MS5803)

Caso não consiga ler ambos, ele enviará uma mensagem mostrando qual erro ocorreu.
