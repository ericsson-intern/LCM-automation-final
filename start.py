
import main
import pyfiglet
import click
import os
import shutil
import cli.colourer



header = pyfiglet.figlet_format("MavenBox")

@click.group()
def interface():
    '''
It is a utility-package to manage and batch-process all/selected gerrit projects 
for POM-dependency version-updation or injection. And, raises gerrit-commit for 
changed repositories through Build-Master authority.\n
Contact: Pulkit Garg (wittycodes@gmail.com) - Intern, Ericsson-Chennai\n

    '''
    pass



@interface.command()

@click.option(
     '--csv', '-f',prompt='Artifacts CSV_Path',default = './artifacts.csv',
    
    help='Enter file_path of csv (groupid:version) containing all artifacts to process')
@click.option(
    '--local','-l',prompt='Search in local-cache for repositories instead?',
    is_flag=True, default = True,
    help='')
@click.option(
    '--reviewers', '-r',prompt="Add Reviewers", default = '$',
    help='Enter list of reviewers to add to further gerrit-commits')   




def update(csv ,local, reviewers=None):
    
    if csv.startswith('"'):
        csv='\\\\'.join(csv[1:-1].split('\\'))
            
    print('\n\n\n\n\n')

    
    # if not local:
    #     # local_cache = os.path.abspath(main.COLLECTION_ROOT)
    #     try:
    #         shutil.rmtree(local_cache)
    #     except:
    #         if os.path.isdir(local_cache):
    #             # logging.error("Unable to remove local_cache: root permission denied")
    #             raise
    #         else:
    #             pass
    #             # logging.critical("local_cache not found. New instance will be created.")
    #     else: 
    #         pass
    #         # logging.critical("local_cache purged successfully")
                

    main.update_interface(csv ,reviewers)
    # logging.critical("TASKS COMPLETED. DONE. Have a nice day!")
    
    


if __name__ == "__main__":
    print(header)
    interface()


