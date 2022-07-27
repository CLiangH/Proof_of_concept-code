项目目标
=

verify the some pitfalls with proof-of-concept code

代码解析
=

__leaking k__
___________________

泄露随机数k从而丢失d.

传入参数r,s,k,则d的计算式为：

d=$(s+r)^{-1}$ * (k-s) mod n

__reusing k__
___________________

重用k导致d泄露.

传入参数r1,s1,r2,s2(使用同一个k进行签名)，则d的计算式为：

d1=s2-s1

d2=s1-s2+r1-r2

d=(d1/d2) mod n

__reusing k by different users__
______________________________________

两个不同的人使用同一个k，则其中一个人可以推出另一个人的d.

假设A使用k签发了(r1,s1),B使用k签发了(r2,s2)，则两者对应的d分别为：

dB=((k-s2)/(s2+r2)) mod n

dA=((k-s1)/(s1+r1)) mod n

__same d and k with ECDSA__
____________________________________

使用相同的d和k签发了SM2和ECDSA.

假设使用d和k签发的ECDSA为(r1,s1),签发的SM2为(r2,s2),则d的计算式为：

d=((s1s2-e1)/(r1-s1s2-s1r2)) mod n

运行指导
=

代码可直接运行

运行截图
=

![inage](https://github.com/CLiangH/Picture/blob/main/proof1.png)

















