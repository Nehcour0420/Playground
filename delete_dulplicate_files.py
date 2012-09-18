import os
import md5
from time import clock as now
def getmd5(filename):
    file_txt = open(filename,'rb').read()
    m = md5.new(file_txt)
    return m.hexdigest()
def main():
    path = raw_input("path: ")
    all_md5 = {}
    all_size = {}
    no_of_file=0
    no_of_delete=0
    start=now()
    for file in os.listdir(path):
        no_of_file += 1
        os_path=os.path.join(path,file)
        if os.path.isfile(os_path) == True:
            size = os.stat(os_path).st_size
            name_and_md5=[os_path,'']
            if size in all_size.keys():
                new_md5 = getmd5(os_path)
                if all_size[size][1]=='':
                    all_size[size][1]=getmd5(all_size[size][0])
                if new_md5 in all_size[size]:
                    print 'Delete',file
                    no_of_delete += 1
                else:
                    all_size[size].append(new_md5)
            else:
                all_size[size]=name_and_md5
    end = now()
    time_last = end - start
    print 'Total number of files:',no_of_file
    print 'Deleted number of files:',total_delete
    print 'Run time:',time_last,'seconds'
   
if __name__=='__main__':
    main()