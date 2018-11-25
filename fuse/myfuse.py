#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import sample

from fuse import FUSE, FuseOSError, Operations

class Passthrough(Operations):
    def __init__(self, root):
        self.root = root
        self.b=0

    # Helpers
    # =======

    def _full_path(self, partial):
        #print("full path function")
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        print("access function")
        full_path = self._full_path(path)
        
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        #print('chmod func')
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        #print('chown func')
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        print("get attr function")
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        print(dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid')))
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        print('readdir func')
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        #call the google drive api
        file_list=sample.view()
        #file_list=[]
        for i in file_list:
            dirents.append(i['name'])
        for r in dirents:
            yield r

    def readlink(self, path):
        #print('readlink func')
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        #print('mknod func')
        return os.mknod(self._full_path(path), mode, dev)

#removes file from drive too
    def rmdir(self, path):
        print('rmdir func')
        full_path = self._full_path(path)
        sample.delete_file(path[1:])
        return os.rmdir(full_path)

# create folder in gdrive
    def mkdir(self, path, mode):
        print("mkdir function")
        # sample.create_folder(path[1:])
        m=0
        n=0
        for i in range(len(path)-1,-1,-1):
            if(path[i]=='/'):
                if(m==0):
                    m=i
                elif(n==0):
                    n=i
        #print(path[n+1:m],path[m+1:])
        sample.create_folder(path[n+1:m],path[m+1:])
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        print("unlink")
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        print("symlink")
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        print("link")
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        print("utimens")
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        
        a=os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        sample.upload(path[1:],full_path)
        return a 

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    
    def write(self, path, buf, offset, fh):    
        #done file uploading
        
        full_path = self._full_path(path)
        os.lseek(fh, offset, os.SEEK_SET)
        z=os.write(fh, buf)
        print(self.b,offset)
        return z
        
    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        print("flush")
        return os.fsync(fh)

    def release(self, path, fh):
        print("release")
        sample.delete_file(path[1:])
        a=os.close(fh)
        full_path = self._full_path(path)
        sample.upload(path[1:],full_path)
        return a


    def fsync(self, path, fdatasync, fh):
        print("fsync") 
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])

    {'st_ctime': 1543072094.0701227,
     'st_mtime': 1541789649.051559, 
     'st_nlink': 1,
      'st_mode': 33204, 
     'st_size': 356352,
      'st_gid': 1000, 
     'st_uid': 1000, 
     'st_atime': 1543072077.85412}