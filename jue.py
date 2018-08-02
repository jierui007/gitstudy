#!/usr/bin/python3.7
#-*-coding:utf-8-*-
for m in range(1,10):
    for n in range(1,10):
        if m>=n:
            print('%sx%s=%s'%(m,n,m*n),end=' ')
    print()

