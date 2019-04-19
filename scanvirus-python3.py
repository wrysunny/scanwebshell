#!/usr/bin/env python3
#!-*- coding:utf-8 -*-
import sys
import json
import requests
import urllib3
urllib3.disable_warnings()
from requests_toolbelt.multipart.encoder import MultipartEncoder


def upload_file(upload_file):
    url = 'https://scanner.baidu.com/enqueue'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0','Content-Type': 'text/html; charset=UTF-8','X-Requested-With': 'XMLHttpRequest'}

    multipart_encoder = MultipartEncoder(
        fields = {
            'archive': (upload_file,open(upload_file, 'rb'),'application/octet-stream')
        },boundary = '------WebKitFormBoundaryFPAYnfyb2UEXGkBp'
    )

    headers['Content-Type'] = multipart_encoder.content_type

    r = requests.post(url, headers=headers, data=multipart_encoder, timeout=10, verify=False)
    #print(r.request.headers, r.request.body)
    if r.status_code == 200:
        s = json.loads(r.content)
        if s['status'] == 0:
            print(f"result: {s['url']}\n") 
            return s['url']
        else:
            print("Please check.\n")
            exit(1)
    else:
        print(f"Error,code:{r.status_code}\n Please check network.")

def result_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0','Content-Type': 'text/html; charset=UTF-8'}
    r = requests.get(url=url, headers=headers, timeout=10, verify=False).content
    result = json.loads(r)
    #print(result)
    filemd5 = result[0]['md5']
    total =result[0]['total']
    detected = result[0]['detected']
    print(f"File MD5: {filemd5}\nTotal: {total}\nVirus File: {detected}\n   INFO:  ")
    for i in range(0,int(total)):
        if result[0]['data'][i]['descr'] != None:
            path = result[0]['data'][i]['path']
            descr = result[0]['data'][i]['descr']
            print(f"Virus Path: {path}\nVirus Type: {descr}")

if __name__=="__main__":
    if len(sys.argv) < 3 :
        print(f"\nexample: python {sys.argv[0]} -f <files>\n")
        exit(0)
    print(f"scanning: {sys.argv[2]}")
    check_url = upload_file(sys.argv[2])
    result_url(check_url)