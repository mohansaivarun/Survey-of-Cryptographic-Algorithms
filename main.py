#import libraries
from tkinter import messagebox as mb
from tkinter import *
import os
from tkinter.filedialog import askopenfilename,asksaveasfilename
from timeit import default_timer
import pyDes as DES
import pyaes as AES
from xlsxwriter import *

def openfile():
    global name
    name = askopenfilename(initialdir=os.curdir,filetypes =(("TIF File", "*.txt"),("All Files","*.*")),title = "Choose a file.")
    if name=="":
        error="Please Try Again..."
        file_path.set(error)
    else:
        file_path.set(name)

def EncryptText():
    global name,m1,m2,m3,m4,m5,m6,et1,et2,et3,et4,et5,et6,window,l,edone
    #Ceasar Cipher Method
    st=default_timer()
    f=open(name,"r")
    s=f.read()
    skey=4
    for i in s:
        p=chr(ord(i)+skey)
        m1+=p
    f.close()
    end=default_timer()
    et1=end-st

    #ROT13 Method
    st=default_timer()
    f=open(name,"r")
    s=f.read()
    a_m,n_z=[chr(i) for i in range(97,110)],[chr(i) for i in range(110,123)]
    for i in s:
        if(i in a_m):m2+=n_z[a_m.index(i)]
        elif(i in n_z):m2+=a_m[n_z.index(i)]
        else:m2+=i
    f.close()
    end=default_timer()
    et2=end-st
    
    #Transposition
    st=default_timer()
    f=open(name,"r")
    s=f.read()
    c=0
    for i in s:
        c+=1
        m3+=i
        if(c%5==0):
            l.append(m3)
            m3=""
            c=0
    if(m3!=""):l.append(m3)
    m3=""
    if(len(l[-1])<5):
        y=""
        for i in range(5-len(l[-1])):
            y+=" "
        l[-1]=l[-1]+y
    for i in range(5):
        for j in range(len(l)):
            m3+=l[j][i]
    f.close()
    end=default_timer()
    et3=end-st
    
    #Multiplication Cipher
    st=default_timer()
    f=open(name,"r")
    k,c=[i for i in range(26)],[chr(i) for i in range(97,123)]
    s=f.read()
    key=7
    for i in s:
        if(i.isupper()):
            a=((k[c.index(i.lower())])*key)%26
            m4+=c[k.index(a)]
        elif(i.islower()):
            a=((k[c.index(i)])*key)%26
            m4+=c[k.index(a)]
        else:m4+=i
    f.close()
    end=default_timer()
    et4=end-st

    #Data Encryption Standard DES
    st=default_timer()
    f=open(name,"r")
    s=f.read()
    key=b"12345678"
    des_obj=DES.des(key,padmode=DES.PAD_PKCS5)
    m5=des_obj.encrypt(s)
    f.close()
    end=default_timer()
    et5=end-st

    #Advanced Encryption Standard AES
    st=default_timer()
    f=open(name,"r")
    s=f.read()
    key=b"1_2_3_4_5_6_7_8_"
    aes_obj=AES.AESModeOfOperationCTR(key)
    m6=aes_obj.decrypt(s)
    f.close()
    end=default_timer()
    et6=end-st

    edone=True
    f=open("Cipher Text.txt","w+")
    t1="1) Ceaser Cipher = "+str(m1)
    t2="2) ROT13 Cipher = "+str(m2)
    t3="3) Transposition Cipher = "+str(m3)
    t4="4) Multiplicative Cipher = "+str(m4)
    t5="5) Data Encryption Standard Cipher = "+str(m5)
    t6="6) Advanced Encryption Standard Cipher = "+str(m6)
    f1=open(name,"r")
    f.write("For the Plain Text - "+"'"+f1.read()+"'"+"\n\n")
    f.write(t1+"\n"+t2+"\n"+t3+"\n"+t4+"\n"+t5+"\n"+t6+"\n")
    f.close()
    f1.close()
    mb.showinfo("Success","Encryption Complete")
    
def DecryptText():
    global name,m1,m2,m3,m4,m5,l,window,d1,d2,d3,d4,d5,d6,dt1,dt2,dt3,dt4,dt5,dt6,ddone
    #Ceasar Cipher
    st=default_timer()
    skey=4
    for i in m1:
        m=chr(ord(i)-skey)
        d1+=m
    end=default_timer()
    dt1=end-st
        
    #ROT13 Cipher
    st=default_timer()
    a_m,n_z=[chr(i) for i in range(97,110)],[chr(i) for i in range(110,123)]
    for i in m2:
        if(i in a_m):d2+=n_z[a_m.index(i)]
        elif(i in n_z):d2+=a_m[n_z.index(i)]
        else:d2+=i
    end=default_timer()
    dt2=end-st

    #Transposition
    st=default_timer()
    t,k,t1="",0,[]
    for i in m3:
        k+=1
        t+=i
        if(k==len(l)):
            t1.append(t)
            t=""
            k=0
    for i in range(len(l)):
        for j in range(5):
            t+=t1[j][i]
    d3=t.rstrip()
    end=default_timer()
    dt3=end-st
    
    #Multiplicative Cipher
    l1,l2=[1,3,5,7,9,11,15,17,19,21,23,25],[1,9,21,15,3,19,7,23,11,5,17,25]
    st=default_timer()
    k,c=[i for i in range(26)],[chr(i) for i in range(97,123)]
    key,d4=7,""
    k_i=l2[l1.index(key)]
    for i in m4:
        if(i!=" "):
            a=(k[c.index(i)]*k_i)%26
            d4+=c[a]
        else:d4+=i
    end=default_timer()
    dt4=end-st

    #Data Encryption Standard DES
    st=default_timer()
    s=m5
    key=b"12345678"
    des_obj=DES.des(key,padmode=DES.PAD_PKCS5)
    enc_str=des_obj.decrypt(s)  #gives Byte String
    conv_enc_str=enc_str.decode("utf-8")
    d5=conv_enc_str
    end=default_timer()
    dt5=end-st

    #Advanced Encryption Standard AES
    st=default_timer()
    s=m6
    key=b"1_2_3_4_5_6_7_8_"
    aes_obj=AES.AESModeOfOperationCTR(key)
    d6=aes_obj.decrypt(s).decode("utf-8")
    end=default_timer()
    dt6=end-st
    
    ddone=True
    mb.showinfo("Sucess","Decryption Complete")

def submit():
    global edone,ddone,window
    if(edone==True and ddone==True):
        dest=asksaveasfilename(initialdir=os.curdir,filetypes =(("Excel Workbook", "*.xlsx"),("All Files","*.*")),title = "Choose a file.")+".xlsx"
        if dest=="":
            mb.showerror("Oops","You haven't choosen any File...")
            return None        
        T,et,dt=[et1+dt1,et2+dt2,et3+dt3,et4+dt4,et5+dt5,et6+dt6],[et1,et2,et3,et4,et5,et6],[dt1,dt2,dt3,dt4,dt5,dt6]
        names=["Ceaser Cipher","ROT13 Cipher","Trasposition Cipher","Multiplicative Cipher","DES","AES"]
        wbook=Workbook(dest)
        total=wbook.add_worksheet("Analysis")
        enc=wbook.add_worksheet("Encryption")
        dec=wbook.add_worksheet("Decryption")
        
        #To write in total sheet
        total.write("A2","Name ofAlgorithm")
        total.write("D2","Time")
        for i in range(6):
            total.write("A%i"%(i+3),names[i])
            total.write("D%i"%(i+3),T[i])
        chart=wbook.add_chart({"type":"column"})
        chart.add_series({'categories':'=Analysis!$A$3:$A$8','values': '=Analysis!$D$3:$D$8'})
        chart.set_x_axis({'name':"Name of Algorithm"})
        chart.set_y_axis({'name':"Time in sec"})
        total.insert_chart("F2",chart)

        #To write in enc sheet
        enc.write("A2","Name ofAlgorithm")
        enc.write("D2","Time")
        for i in range(6):
            enc.write("A%i"%(i+3),names[i])
            enc.write("D%i"%(i+3),et[i])
        chart=wbook.add_chart({"type":"column"})
        chart.add_series({'categories':'=Encryption!$A$3:$A$8','values': '=Encryption!$D$3:$D$8'})
        chart.set_x_axis({'name':"Name of Algorithm"})
        chart.set_y_axis({'name':"Time in sec"})
        enc.insert_chart("F2",chart)

        #To write in dec sheet
        dec.write("A2","Name ofAlgorithm")
        dec.write("D2","Time")
        for i in range(6):
            dec.write("A%i"%(i+3),names[i])
            dec.write("D%i"%(i+3),dt[i])
        chart=wbook.add_chart({"type":"column"})
        chart.add_series({'categories':'=Decryption!$A$3:$A$8','values': '=Decryption!$D$3:$D$8'})
        chart.set_x_axis({'name':"Name of Algorithm"})
        chart.set_y_axis({'name':"Time in sec"})
        dec.insert_chart("F2",chart)
        mb.showinfo("Success","Opening Your Survey. Please Wait ...")
        wbook.close()
        os.startfile(dest)
    elif(edone==True and ddone==False):mb.showinfo("Oops","Please Decrypt to Start Survey")
    elif(edone==False and ddone==False):mb.showinfo("Failure","Please Encrypt and Decrypt First")
    window.destroy()
     
name,m1,m2,m3,m4,m5,m6="","","","","","",""
et1,et2,et3,et4,et5,et6=0,0,0,0,0,0  #Encryption Times
dt1,dt2,dt3,dt4,dt5,dt6=0,0,0,0,0,0  #Decryption Times
d1,d2,d3,d4,d5,d6,l="","","","","","",[]
edone,ddone=False,False
window=Tk()
window.geometry("500x450")
window.resizable(width=False, height=False)
window.configure(bg="#005aaf")
window.title("Encryption and Decryption")
Label(window,text="A Survey on the Cryptographic Encryption Algorithms ",font=("Calibri",15,"bold"),bg="#005aaf",fg="white").place(x=20,y=15)
select=Button(window,text="Select File",bg="white",fg="#005aaf",command=openfile)
select.place(x=10,y=160)
file_path=StringVar()
file_path.set("Please Select a file")
filename=Label(window,textvariable=file_path,bg="#005aaf",fg="white")
filename.place(x=100,y=160)
Button(window, text = "Encrypt",bg="white",fg="#005aaf",command=EncryptText).place(x=125,y=250)
Button(window, text = "Decrypt",bg="white",fg="#005aaf",command=DecryptText).place(x=320,y=250)
Button(window, text = "Get Survey",bg="white",fg="#005aaf",command=submit).place(x=225,y=350)
window.mainloop()
