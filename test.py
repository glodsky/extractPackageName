import os
import sys
from os import listdir
from os.path import isfile, join
import subprocess

CHECKNAME = 'lxml'
packageName =[] 
needs_install_packageNames=[]

def getPythonSite_packagesPath():
    path = os.environ.get("PATH",os.defpath)
    path = path.split(os.pathsep)
    for x in path:
        if (x.find("Python")>0 and x.find("Scripts")<0):
            package = x+"Lib\\site-packages"
            return package

def getPythonLibPath():
    path = os.environ.get("PATH",os.defpath)
    path = path.split(os.pathsep)
    for x in path:
        if (x.find("Python")>0 and x.find("Scripts")<0):
            package = x+"Lib"
            return package
#python -m pip install execjs

def setPackageName(path):
    global packageName
    curdir = path
    onlyfiles = [f for f in listdir(curdir) if isfile(join(curdir, f))]	
    for f in onlyfiles:        
        if f.endswith('.py'):
            target = curdir + "\\" + f 
            print target
            with open(target) as fp:
                    line = fp.readline()
                    cnt = 1    			
                    pk_shortname = ''
                    while line>0 :                           
                            span = line.strip()
                            if (len(span)<=0):
                                fp.close()
                                break
                            print ("Line {}: {}").format(cnt,line.strip())
                            if (span.startswith("import")>0):
                                    divv = span.split(' ')
                                    pk_shortname = divv[1]
                            elif (span.startswith("from")>0):
                                  divv = span.split(' ')
                                  pk_shortname = divv[1]
                                  if (divv[1].find('.')>0):
                                       pk_shortname = (divv[1].split('.'))[0]
                            else:
                                fp.close()
                                break

                            if (not pk_shortname in packageName):
                                packageName.append(pk_shortname)

                            line = fp.readline()
                            cnt += 1
            print('\n')

def checkPackagesInstallStatus(pl,libfiles):
    global packageName
    needs_install_packageNames = []
    for pname in packageName:
        bflag = 0
        print "Finding %s  "%pname
        if (pname in needs_install_packageNames):
            continue
        for dirname in pl:
            if(pname==dirname):
                print "Founded! Installed! : %s " % pname
                packageName.remove(pname)
                bflag = 1
                break
        if bflag == 1 :
            continue
        for libfile in libfiles:
            lfname = (libfile.split('.'))[0]
            if (pname == lfname):
                print "Founded! Installed! : %s " % pname
                packageName.remove(pname)
                bflag = 2
                break
        if bflag == 2 :
            continue
        print "You need to install %s" %pname
        needs_install_packageNames.append(pname)
    return needs_install_packageNames
                                
def main():
    # get sources *.py file
    global packageName
    curdir = r'C:\Users\Administrator\Desktop\Idea AutoInstallPackage 201811141129'
    setPackageName(curdir)
    print packageName

    pp = getPythonSite_packagesPath()
    print pp
    pl = os.listdir(pp)
    libpath = getPythonLibPath()
    print libpath
    libfiles = [f for f in listdir(libpath) if isfile(join(libpath, f))]
    needs_install_packageNames = checkPackagesInstallStatus(pl,libfiles)

    # to install package
    print "You need to install range :"
    print needs_install_packageNames        
    for x in needs_install_packageNames:
        status = subprocess.call("pip install " + x ,shell=True)
        if status == 0 :
            print "Download and Install Successfully! : %s " % x
        else:
            print "Error!Please contact progamer"
            
if __name__ == '__main__':
    main()

 


 
