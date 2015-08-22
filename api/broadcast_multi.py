# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding:utf-8 -*-
# 参考: https://sites.google.com/site/tibracode/python/socket

import socket
import fcntl
import sys
import time
import multiprocessing


def ifCheck(g_ifname):
  if_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    result = fcntl.ioctl(if_sock.fileno(), 0x8915, (g_ifname + '\0' * 32)[:32])
  except IOError:
    if_sock.close()
    return None
  if_sock.close()
  return socket.inet_ntoa(result[20:24]).split(".")


def send_broadCast(g_sock, g_cmd, g_BROADCAST_ADDRESS, g_PORT, g_send_protcess_result):
  print "[multiprocess] send_broadCast : start send broadcast at "
  for retry_count in range(1,5):
    try:
      g_sock.sendto(g_cmd, (g_BROADCAST_ADDRESS, g_PORT))
      time.sleep(0.02)
      print "hogehoge"
    except socket.error, err_msg:
      print err_msg
      result_msg = "[multiprocess] send_broadCast - err"
      g_send_protcess_result.put(result_msg)
      print "[multiprocess:(end)send_broadCast]:end"
    g_send_protcess_result.put(0)


def recev_broadCast(g_sock, g_recev_protcess_result):
  address_list = []
  print "[thread:(start)recev_broadCast]:start"
  while True:
    try:
      msg = g_sock.recv(8192)
      if ( address_list in address ) : address_list.append(address)
    except socket.timeout, err_msg:
      print "[thread:(end)recev_broadCast]:end"
      return g_recev_protcess_result.put(address_list)
    except socket.error, err_msg:
      print err_msg
      print "[thread:(end)recev_broadCast]: socket error"
      return g_recev_protcess_result.put(-1)
    g_recev_protcess_result.put(address_list)


def main_broadCast(g_l2id, g_port):
  HOST = ""
  PORT = int(g_port)
  IF_TARGET = "gr" + g_l2id
  send_protcess_result = multiprocessing.Queue()
  recev_protcess_result = multiprocessing.Queue()

  if_chank = (ifCheck(IF_TARGET))
  if if_chank is None : return {}
  else :
    IF_ADDRESS = if_chank[0] + "." + if_chank[1] + "." + if_chank[2] + "." + if_chank[3]
    BROADCAST_ADDRESS = if_chank[0] + "." + if_chank[1] + "." + if_chank[2] + ".255"

  # クライアントソケット
  client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, IF_TARGET)
  client_sock.bind((HOST,PORT))
  client_sock.settimeout(0.1)

  # ブロードキャスト送受信 - インスタンスの作成
  send_broadcast_job = multiprocessing.Process(target=send_broadCast, args=(client_sock, "get ip", BROADCAST_ADDRESS, PORT, send_protcess_result))
  recev_broadcast_job = multiprocessing.Process(target=recev_broadCast, args=(client_sock, recev_protcess_result))

  # マルチプロセス起動
  send_broadcast_job.start()
  recev_broadcast_job.start()
  send_broadcast_job.join()
  recev_broadcast_job.join()

  # プロセス戻り値取得
  send_job_result = send_protcess_result.get()
  address_list = recev_protcess_result.get()
 
  #debug
  print address_list

  # closing
  client_sock.close()

  #debug
  devices = {1:{'ip': '192.168.11.8', 'mac': 'b8:27:eb:29:e5:57'}}
  #devices = {1:{'ip': 'xxx.xxx.xxx.xxx', 'mac': '00:00:00:00'}, 2:{'ip': 'yyy.yyy.yyy.yyy', 'mac': '0F:0F:0F:0F'}}
  return devices
