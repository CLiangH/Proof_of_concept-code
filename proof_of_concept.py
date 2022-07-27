import SM3
import random
    
def Coprime(a, b):
    while a != 0:
        a, b = b % a, a
    if b != 1 and b != -1:
        return 1
    return 0

def gcd(a, m):
    if Coprime(a, m):
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    if u1 > 0:
        return u1 % m
    else:
        return (u1 + m) % m

def T_add(P,Q):
    if (P == 0):
        return Q
    if (Q == 0):
        return P
    if P == Q:
        aaa=(3*pow(P[0],2) + a)
        bbb=gcd(2*P[1],p)
        k=(aaa*bbb)%p 
    else:
        aaa=(P[1]-Q[1])
        bbb=(P[0]-Q[0])
        k=(aaa*gcd(bbb,p))%p 

    Rx=(pow(k,2)-P[0] - Q[0]) %p
    Ry=(k*(P[0]-Rx) - P[1])%p
    R=[Rx,Ry]
    return R



def T_mul(n, l):
    if n == 0:
        return 0
    if n == 1:
        return l
    t = l
    while (n >= 2):
        t = T_add(t, l)
        n = n - 1
    return t

a = 2
b = 2       
p = 17 #椭圆曲线参数，y^2=x^3+2x+2
G = [5, 1]
n = 19
k=2
message='Satoshi'
e=hash(message)
d = 7
Pubk = T_mul(d, G)
ID='1234567812345678'
ZZ=str(len(ID))+ID+str(a)+str(b)+str(G[0])+str(G[1])+str(Pubk[0])+str(Pubk[1])
Za=SM3.SM3_test(ZZ)

def Sign(M):
    global n,G,d,Za,k
    M_=Za+M
    e = SM3.SM3_test(M_)
    R=T_mul(k,G)
    r=(R[0]+int(e,16)) % n
    e=hash(message)
    s=(gcd(1+d, n) * (k - d * r)) % n
    return r,s

def E_Sign(m):
    global n,G,d
    k=random.randint(1,n-1)
    R=T_mul(k,G)
    r=R[0] % n
    e=hash(message)
    s=(gcd(k, n) * (e + d * r)) % n
    return r,s



#print('********************leaking k********************')

def leaking_k(r,s):
    global k
    d=(gcd(s+r,n)*(k-s))%n
    return d

#print('********************reusing k********************')

def reusing_k(r1,s1,r2,s2):
    d1=s2-s1
    d2=s1-s2+r1-r2
    d=(d1*gcd(d2,n))%n
    return d

#print('***********reusing k by different users***********')

def r_k_2(r,s,k):
    d=((k-s)*gcd(s+r,n))%n
    return d

#print('*************same d and k with ECDSA*************')


def same_dk(r1,s1,r2,s2,e1):
    d1=(s1*s2-e1)
    d2=(r1-s1*s2-s1*r2)
    d=(d1*gcd(d2,n))%n
    return d


print('********************leaking k********************')

r1,s1=Sign(message)
d1=leaking_k(r1,s1)
print('leaking k攻击结果d为:',d1)

print('********************reusing k********************')

r2,s2=Sign(message)
r3,s3=Sign(message+message)
d2=reusing_k(r2,s2,r3,s3)
print('reusing k攻击结果d为:',d2)

print('***********reusing k by different users***********')

r4,s4=Sign(message)
r5,s5=Sign(message+message)
d4=r_k_2(r4,s4,k)
d5=r_k_2(r5,s5,k)
print('reusing k by different users攻击结果d为:',d4,d5)

print('*************same d and k with ECDSA*************')

r6,s6=E_Sign(message)
r7,s7=Sign(message)
d6=same_dk(r6,s6,r7,s7,hash(message))
print('same d and k with ECDSA攻击结果d为:',d6)














    






