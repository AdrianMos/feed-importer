from git import Repo
import pathlib
import shutil
import os
import stat
import time


class Updater(object):
     
    def __init__(self, gitUrl, gitBranch, softwarePath):
        self.gitUrl = gitUrl
        self.gitBranch = gitBranch
        self.softwarePath = softwarePath
        self.tempUpdateRepositoryPath = os.path.join(softwarePath, 'upgrade', 'git-repo')

        self._localRepo = Repo(self.softwarePath)
        print('Software instalat')
        self._print_repository(self._localRepo)
        
    
    def Download(self):
        #delete directory if exists, gitpython can only clone in an empty folder
        self._deleteFolder(self.tempUpdateRepositoryPath)        
        
        self._updateRepo = Repo.clone_from(url = self.gitUrl, 
                                           to_path = self.tempUpdateRepositoryPath, 
                                           branch="master") 
        print('Ultima versiune de software')
        self._print_repository(self._updateRepo)
    
    def _deleteFolder(self, path):
        if os.path.exists(path):
            shutil.rmtree(path, onerror=self._remove_readonly)
        
    def _remove_readonly(self, fn, path, excinfo):
        try:
            os.chmod(path, stat.S_IWRITE)
            fn(path)
        except Exception as exc:
            print ("Skipped:", path, "because:\n", exc)
    

    def _print_repository(self, repo):
        print('  ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(repo.head.commit.committed_date)) 
              + ' SHA:' + format(str(repo.head.commit.hexsha)))
        #print('  Last commit for  is {}.'.format(str(repo.head.commit.hexsha)))
       

    def isUpdateAvailable(self):
        if self._localRepo == None or self._updateRepo == None:
            raise ValueError
        
        return self._localRepo.head.commit.hexsha != self._updateRepo.head.commit.hexsha
        
    def Install(self):
        # run the software migration batch script
        # the script installs the new software and keeps the old configurations
        batchLocation = os.path.join(self.softwarePath, 'upgrade', 'migrate.bat')
        print('Updater.Install called()')
        #os.startfile(batchLocation)
