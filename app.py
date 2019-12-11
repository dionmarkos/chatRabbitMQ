import pika
import time
import threading

def threadReceber():
    while True:
        thread = threading.Thread(target=receber, args=())
        thread.daemon = True
        thread.start()
        enviar()

def receber():
    try:
        conexao = pika.BlockingConnection(pika.ConnectionParameters(host))
        canal = conexao.channel()
        canal.queue_declare(queue=usuario)
        canal.basic_consume(queue=usuario, auto_ack=True, on_message_callback=callback)
        canal.start_consuming()
        canal.close()
        conexao.close()
    except Exception as exception:
        print('Erro ao inicar servidor de recebimento. {}', exception)

def callback(ch, method, properties, body):
    print("-> %r" % body.decode())

def enviar():
    try:
        conexao = pika.BlockingConnection(pika.ConnectionParameters(host))
        canal = conexao.channel()
        canal.queue_declare(queue=usuario_recebimento)
        mensagem = usuario + ' disse: ' + input('-> ')
        canal.basic_publish(exchange='', routing_key=usuario_recebimento, body=mensagem)
        canal.close()
        conexao.close()
    except Exception:
        print('Erro ao enviar mensagem.')

def main():
    global usuario
    global host
    global usuario_recebimento
    usuario = input('Digite seu nome de usuário -> ')
    host = input('Digite o IP ou deixe em branco para "localhost" -> ')
    usuario_recebimento = input('Digite o nome do usuário com quem você quer iniciar a conversa -> ')
    if host == '':
        host = 'localhost'
    while True:
        threadReceber()

if __name__== "__main__":
  main()
