#!/usr/bin/env python3

import sys
import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

# Credenciales generadas en la vista de twitter para Developers
consumer_key    = 'HJs1tKcqZRVAxPlPMoBMaietr'
consumer_secret = 'xqg5ktgZMtZVVk56oGfcI1Rmr5kx2GDE5Tv1vIJgwxAIjlfPkv'
access_token    = '1001625991955955712-pV1Efg8TiTLVKeLCLULesTeIjqkJqJ'
access_secret   = 'b9KH3P8ASPDD8E8wCzHsB32IgTQDZjTBr12MKaS2Vev4m'

# Se crea esta clase que hereda de StreamListener en tweepy StreamListener
class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket #el socket de streaming por donde se enviaran los tweets
		
    # Se sobreescribe el metodo on_data() para que reenvie los tweets al socket y a la vez se impriman en pantalla
    def on_data(self, data):
        try:
            message = json.loads( data )
            print( message['text'].encode('utf-8', errors="replace") )  #obtenemos solo el texto del tweet
            self.client_socket.send( message['text'].encode('utf-8', errors="replace") )
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def if_error(self, status):
        print(status)
        return True

# Este es el metodo que crea el objeto de conexion a twitter
def send_tweets(c_socket, filter_word):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=[filter_word])



if __name__ == "__main__":
    new_skt = socket.socket()   	# Creamos el objeto socket
    host = "127.0.0.1"
    port = 5555     				# Puerto que se usara para esuchar las peticiones de spark y enviar los tweets
    new_skt.bind((host, port))

    print("Esuchando y esperando conexion en el puerto: %s" % str(port))

    new_skt.listen(5)                 # Esperamos hasta que el cliente se conecte antes de comenzar el Streaming
    c, addr = new_skt.accept()        # Cuando recibimos una conexion se acepta, esto devuelve el socket por donde se abrio la conexion

    print("Se acepto la conexion de: " + str(addr))
    # Comenzamos a enviar los tweets por el socket filtrando por aquellos que contengan la palabra indicada por defecto o dada por argumento
    filter_word = "football"
    if len(sys.argv) >= 2:
        filter_word = sys.argv[1]
    send_tweets(c, filter_word)

