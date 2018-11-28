#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
from errno import *
import sample
import  stat
import time

from fuse import FUSE, FuseOSError, Operations

class Passthrough(Operations):
    def __init__(self, root):
        self.root = root
        self.b=0
        self.dirlist = []
        self.predefineddir = [".Trash", ".Trash-1000", "autorun.inf", ".xdg-volume-info"]

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
        print("access function", path)
        full_path = self._full_path(path)
        
        if not os.access(full_path, mode):
            print("raising error!")
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        #print('chmod func')
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        #print('chown func')
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def get_metadata(self):
        now = time.time()
        st = {}
        st['st_mode'] = 0777 | stat.S_IFDIR  # stat.S_IFREG
        st['st_ino'] = 0
        st['st_dev'] = 0
        st['st_nlink'] = 1
        st['st_uid'] = os.getuid()  # file object's user id
        st['st_gid'] = os.getgid()  # file object's group id
        st['st_size'] = 100  # size in bytes
        st['st_atime'] = now  # last access time in seconds
        st['st_mtime'] = now  # last modified time in seconds
        st['st_ctime'] = now
        # st_blocks is the amount of blocks of the file object, and depends on the block size of the file system (here: 512 Bytes)
        st['st_blocks'] = (int)((st['st_size'] + 511) / 512)
        return st

    def getattr(self, path, fh=None):
        print("get attr function", path)

        full_path = self._full_path(path)
        try:
            stt = os.lstat(full_path)
            print("metadata for:", full_path)
            """st = {}
            st['st_mode'] = stt.st_mode#0777 | stat.S_IFDIR  # stat.S_IFREG
            st['st_ino'] = stt.st_ino
            st['st_dev'] = stt.st_dev
            st['st_nlink'] = stt.st_nlink
            st['st_uid'] = stt.st_uid  # file object's user id
            st['st_gid'] = stt.st_gid  # file object's group id
            st['st_size'] = stt.st_size  # size in bytes
            st['st_atime'] = stt.st_atime # last access time in seconds
            st['st_mtime'] = stt.st_mtime  # last modified time in seconds
            st['st_ctime'] = stt.st_ctime
            # st_blocks is the amount of blocks of the file object, and depends on the block size of the file system (here: 512 Bytes)
            st['st_blocks'] = stt.st_blocks#(int)((st['st_size'] + 511) / 512)
            st['st_rdev'] = stt.st_rdev
            return st"""
            return dict((key, getattr(stt, key)) for key in ('st_atime', 'st_ctime',
                                                            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size',
                                                            'st_uid'))
        except OSError:
            print("we are OS error---")
            itms = path.split("/")
            gfile_name = itms[len(itms) - 1]
            #gfile_name = path.split("/")[:-1]
            if gfile_name in [".Trash", ".Trash-1000", "autorun.inf", ".xdg-volume-info"]:
                print("oserror->predefined dir")
                return self.get_metadata()
            #gfile_name = path.split("/")[0]#--
            #if gfile_name in predefineddir:
            #    return self.get_metadata()#--
            #if gfile_name not in self.dirlist:
            #    print("oserror->not in dirlist")
            #    raise FuseOSError(ENOENT)
            if not sample.is_file_exist(gfile_name):
                print("no file folder found in gdrive: ", path)
                raise FuseOSError(ENOENT)
        except :
            print("error for:", path, "error is :", sys.exc_info()[0])
            gfile_name = path.split("/")[:-1]
            if not sample.is_file_exist(gfile_name):
                print("no file folder found in gdrive: ", path)
                raise FuseOSError(ENOENT)
            else:
                print("returning default metadata:::::::")
                return self.get_metadata()
            #return dict((key, getattr(st, key)) for key in
                        #('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        #print(dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
        #            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid')))
        print("returning default metadata-----")
        return self.get_metadata()

    def readdir(self, path, fh):
        print('readdir func')
        full_path = self._full_path(path)

        dirents = ['.', '..']
        #if os.path.isdir(full_path):
        #    dirents.extend(os.listdir(full_path))
        #call the google drive api
        file_list = []
        try:
            file_list=sample.view_names()
            #dirlist.extend(file_list)
        except:
            print("error while calling gapi")
        dirents.extend(file_list)
        #file_list=[]
        #for i in file_list:
        #    dirents.append(i['name'])
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
        #sample.delete_file(path[1:])#experi
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