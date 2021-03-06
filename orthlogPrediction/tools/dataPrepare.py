import re
import subprocess
import os
import os.path

def faSize(path):
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1] == '.fa':
            with open(path+"/"+os.path.splitext(filename)[0]+".size", "w+") as f:
                faToSize = subprocess.Popen(['faSize','-detailed',path+"/"+filename],stdout=f)
                faToSize.wait()
def faTwoBit(path):
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1] == '.fa':
            faToTwoBit = subprocess.Popen(['faToTwoBit',path+"/"+filename,path+"/"+filename+".2bit"])
            faToTwoBit.wait()

def targetGffExtend(inGff,size,extend,outGff):
    f = open(inGff,"r")
    f1 = open(outGff,"w")
    rChromSizes=readSize(size)
    lines=f.readlines()
    for l in lines:
        l=l.rstrip("\n")
        if l.find("mRNA")!=-1:
            arr = l.split("\t")            
            if int(arr[3])-int(extend) <=1:
                arr[3]=1
            else:
                arr[3]=int(arr[3])-int(extend)
            if int(arr[4])+int(extend) >=int(rChromSizes[arr[0]])+1:
                arr[4]=int(rChromSizes[arr[0]])+1
            else:   
                arr[4]=int(arr[4])+int(extend)
            arr = [str(x) for x in arr]
            out = "\t".join(arr)       
            f1.write(out+"\n")
        else:
            pass
    f.close()
    f1.close()
            
        

def sizeToBed(size,refGenome):
    f=open(size,"r")
    path = os.path.splitext(size)[0]
    lines=f.readlines()
    bed=open(path+".bed",'w')
    for l in lines:
        l=l.rstrip("\n")
        arr=l.split("\t")
        out=arr[0]+"\t0\t"+arr[1]+"\n"
        bed.write(out)
    bed.close()

def readSize(ChromSizes):
        f=open(ChromSizes,"r")
        lines=f.readlines()
        size={}
        for l in lines:
                l=l.rstrip("\n")
                arr=l.split("\t")
                size[arr[0]]=arr[1]
        return size
        f.close()

def gffToPslBed(gff,rChromSize):
        rChromSizes=readSize(rChromSize)
        f=open(gff,"r")
        psl=open(gff+".psl",'w')
        bed=open(gff+".bed",'w')
        lines=f.readlines()
        count=0
        for l in lines:
                l=l.rstrip("\n")
                arr=l.split("\t")
                count+=1
                if l.find("mRNA")!=-1:
                        blockCount=0
                        tBaseInsert=0
                        tName=arr[0]
                        qName=re.search(r'ID=([^;]+);',arr[-1]).group(1)
                        strand=arr[6]
                        tStart=int(arr[3])-1
                        tEnd=int(arr[4])
                        qChromSize = tEnd-tStart
                        output = str(qChromSize)+"\t"+str(0)+"\t" \
                                +str(0)+"\t"+str(0)+"\t"+str(0)+"\t"+str(0)+"\t" \
                                +str(0)+"\t"+str(0)+"\t" \
                                +strand+"\t"+qName+"\t"+str(qChromSize)+"\t"   \
                                +str(0)+"\t"+str(qChromSize)+"\t" \
                                +tName+"\t"+str(rChromSizes[tName])+"\t"+str(tStart)+"\t"+str(tEnd)+"\t" \
                                +str(1)+"\t"+str(qChromSize)+",\t"+str(0)+",\t"+str(tStart)+",\n"
                        psl.write(output)
                        bed.write(tName+"\t"+str(tStart)+"\t"+str(tEnd)+"\n")
                else:
                        pass
                                       
        f.close()
        psl.close()
        bed.close()
def gffToPslNoExtend(gff,rChromSize):
        rChromSizes=readSize(rChromSize)
        f=open(gff,"r")
        psl=open(gff+".noextend.psl",'w')
        lines=f.readlines()
        count=0
        for l in lines:
                l=l.rstrip("\n")
                arr=l.split("\t")
                count+=1
                if l.find("mRNA")!=-1:
                        blockCount=0
                        tBaseInsert=0
                        tName=arr[0]
                        qName=re.search(r'ID=([^;]+);',arr[-1]).group(1)
                        strand=arr[6]
                        tStart=int(arr[3])-1
                        tEnd=int(arr[4])
                        qChromSize = tEnd-tStart
                        output = str(qChromSize)+"\t"+str(0)+"\t" \
                                +str(0)+"\t"+str(0)+"\t"+str(0)+"\t"+str(0)+"\t" \
                                +str(0)+"\t"+str(0)+"\t" \
                                +strand+"\t"+qName+"\t"+str(qChromSize)+"\t"   \
                                +str(0)+"\t"+str(qChromSize)+"\t" \
                                +tName+"\t"+str(rChromSizes[tName])+"\t"+str(tStart)+"\t"+str(tEnd)+"\t" \
                                +str(1)+"\t"+str(qChromSize)+",\t"+str(0)+",\t"+str(tStart)+",\n"
                        psl.write(output)
                else:
                        pass

        f.close()
        psl.close()
def targetGffNoExtend(inGff,outGff):
    f = open(inGff,"r")
    f1 = open(outGff,"w")
    lines=f.readlines()
    for l in lines:
        l=l.rstrip("\n")
        if l.find("mRNA")!=-1:
            f1.write(l+"\n")
        else:
            pass
    f.close()
    f1.close()

def gffToSize(inGff):
    f1 = open(inGff+".size","w")
    for x in open(inGff):
        x = x.rstrip("\n")
        if x.find("mRNA")!=-1:
            arr = x.split("\t")
            geneId =re.search(r'ID=([^;]+);',arr[-1]).group(1)
            size = int(arr[4])-int(arr[3])+1
            out = geneId+"\t"+str(size)+"\n"
            f1.write(out)
        else:
            pass
    f1.close()
