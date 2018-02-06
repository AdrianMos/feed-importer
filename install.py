from git import Repo
import pathlib
import shutil
import os
import stat
import time


def remove_readonly(fn, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        fn(path)
    except Exception as exc:
        print ("Skipped:", path, "because:\n", exc)

#def delete_folder(pth) :
#    for sub in pth.iterdir() :
#        if sub.is_dir() :
#            delete_folder(sub)
#        else :
#            sub.unlink()
#    pth.rmdir() # if you just want to delete dir content, remove this line

def print_repository(repo):
    print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))
    print('Commit date:'
          + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(repo.head.commit.committed_date)))

def download_latest_repository(gitRepository, storeToPath):
    # delete directory if exists, gitpython can only clone in an empty folder
    if os.path.exists(storeToPath):
        shutil.rmtree(storeToPath, onerror=remove_readonly)
    repo = Repo.clone_from(gitRepository, storeToPath, branch='master')
    

def isLocalRepositoryOutdated(localRepo, remoteRepo):
    return localRepo.head.commit.hexsha != remoteRepo.head.commit.hexsha


MSG_CHECKING_SOFTWARE_UPDATES = "Verificam actualizarile de software"    

try:

    repoPath = os.getcwd()
    oneFolderUp = os.path.dirname(os.getcwd())
    tempRepoPath = os.path.join(oneFolderUp, 'temp-git-repo')

    
    #tempRepoPath = os.path.join(os.getcwd(), os.pardir, 'temp_repo')
    print('temp repo path: ' + str(tempRepoPath))

    print(MSG_CHECKING_SOFTWARE_UPDATES)
    githubRepository = download_latest_repository(gitRepository = 'https://github.com/AdrianMos/feed-importer.git',
                                                  storeToPath = tempRepoPath)
    print_repository(githubRepository)
   
    
    localRepository = Repo(os.getcwd())
    print_repository(localRepository)


    if isLocalRepositoryOutdated(localRepository, githubRepository)
        print('\nExista o versiune mai noua de software')
        print('\nConfirmati instalarea?')

        # run the software migration batch script
        # the script installs the new software but keeps the old configurations
        batchLocation = os.path.join(tempRepoPath, 'upgrade', 'migrate.bat')
        #os.startfile(batchLocation)
        
    else:
        print('\nAveti ultima versiune de software')


except Exception as ex
    print('\n\n Eroare: ' + repr(ex) + '\n')
