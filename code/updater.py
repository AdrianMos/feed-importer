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
    
    def Download(self):
        #delete directory if exists, gitpython can only clone in an empty folder
        self._DeleteFolder(self.tempUpdateRepositoryPath)        
        
        self._updateRepo = Repo.clone_from(url = self.gitUrl, 
                                           to_path = self.tempUpdateRepositoryPath, 
                                           branch="master") 
    
    def IsUpdateRequired(self):
        if self._localRepo == None or self._updateRepo == None:
            raise ValueError
        return self._localRepo.head.commit.hexsha != self._updateRepo.head.commit.hexsha
    
    def GetSoftwareUpdateMessage(self):
        sha = self._getRepositorySha(self._localRepo)
        msg = '  Software actual: '  + \
                   self._getRepositoryDate(self._localRepo) + \
                   '   SHA: ' + sha[len(sha)-14:]
        
        sha = self._getRepositorySha(self._updateRepo)
        msg = msg +  '\n'  +\
                  '  Software nou:    '  +\
                  self._getRepositoryDate(self._updateRepo)  +\
                  '   SHA: ' + sha[len(sha)-14:]

        return msg                          
    
    def Install(self):
        # run the software migration batch script
        # the script installs the new software and keeps the old configurations
        batchLocation = os.path.join(self.softwarePath, 'upgrade', 'migrate.bat')
        print('Updater.Install called()')
        os.startfile(batchLocation)
        
    def GetCurrentSoftwareVersion(self):
        sha = self._getRepositorySha(self._localRepo)
        msg = 'Versiune  '  + self._getRepositoryDate(self._localRepo) + \
              '   SHA: ' + sha[len(sha)-14:] 
        return msg 
        
    def _DeleteFolder(self, path):
        if os.path.exists(path):
            shutil.rmtree(path, onerror=self._RemoveReadonly)
        
    def _RemoveReadonly(self, fn, path, excinfo):
        try:
            os.chmod(path, stat.S_IWRITE)
            fn(path)
        except Exception as exc:
            print ("Skipped:", path, "because:\n", exc)
        
    def _getRepositorySha(self, repo):
         return  format(str(repo.head.commit.hexsha))
       
    def _getRepositoryDate(self, repo):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(repo.head.commit.committed_date))
    
