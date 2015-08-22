# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding:utf-8 -*-

# 参考: https://sites.google.com/site/tibracode/python/socket

import socket
import fcntl
import sys
import time
import threading


def ifCheck(g_ifname):
  if_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    result = fcntl.ioctl(if_sock.fileno(), 0x8915, (g_ifname + '\0' * 32)[:32])
  except IOError:
    if_sock.close()
    return None
  if_sock.close()
  return socket.inet_ntoa(result[20:24]).split(".")


class send_broadCast(threading.Thread):
  def __init__(self, g_send_sock, g_cmd, g_BROADCAST_ADDRESS, g_PORT):
    threading.Thread.__init__(self)
    self.g_send_sock = g_send_sock
    self.g_cmd = g_cmd
    self.g_BROADCAST_ADDRESS = g_BROADCAST_ADDRESS
    self.g_PORT = g_PORT
  def run(self):
    print "[thread:(start)send_broadCast]:start"
    #while True:
    #  try:
    self.g_send_sock.sendto(self.g_cmd, (self.g_BROADCAST_ADDRESS, self.g_PORT))
    time.sleep(0.02)
    #  except socket.error, err_msg:
    #    break
    print "[thread:(end)send_broadCast]:end"
    return 0


class recev_broadCast(threading.Thread):
  def __init__(self, g_recev_sock):
    threading.Thread.__init__(self)
    self.g_recev_sock = g_recev_sock
  def run(self):
    address_list = "hoge"
    print "[thread:(start)recev_broadCast]:start"
    while True:
      try:
        msg = self.g_recev_sock.recv(8192)
        if ( address_list in address ) : address_list.append(address)
      except socket.error, err_msg:
        print "[thread:(end)recev_broadCast]:end"
        return address_list
    return 0


def main_broadCast(g_l2id, g_port):
  HOST = ""
  PORT = int(g_port)
  IF_TARGET = "gr" + g_l2id

  if_chank = (ifCheck(IF_TARGET))
  if if_chank is None : return {}
  else :
    IF_ADDRESS =  if_chank[0] + "." + if_chank[1] + "." + if_chank[2] + "." + if_chank[3]
    BROADCAST_ADDRESS = if_chank[0] + "." + if_chank[1] + "." + if_chank[2] + ".255"

  # 送信用クライアントソケット
  send_client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  send_client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, IF_TARGET)
  send_client_sock.bind((HOST,PORT))
  send_client_sock.settimeout(0.1)
  # 受信用クライアントソケット
  recev_client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  recev_client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, IF_TARGET)
  recev_client_sock.settimeout(0.1)

  # スレッド処理: ブロードキャスト送受信
  send_thread = send_broadCast(send_client_sock, "get ip", BROADCAST_ADDRESS, PORT)
  recev_thread = recev_broadCast(recev_client_sock)

  send_thread_rtn = send_thread.start()
  address_list = recev_thread.start()
  send_thread.join()
  recev_thread.join()
  print address_list

  # closing
  send_client_sock.close()
  recev_client_sock.close()

  #debug
  devices = {1:{'ip': '192.168.11.8', 'mac': 'b8:27:eb:29:e5:57'}}
  #devices = {1:{'ip': 'xxx.xxx.xxx.xxx', 'mac': '00:00:00:00'}, 2:{'ip': 'yyy.yyy.yyy.yyy', 'mac': '0F:0F:0F:0F'}}
  return devices
