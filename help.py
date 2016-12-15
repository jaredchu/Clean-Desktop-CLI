__author__ = 'jaredchu'

helpStr = [
    '',
    '-- CleanDesk Help --',
    '',
    'Args:',
    '-f : File only',
    '-d : Directory only',
    '--test : Create some file and folder for test',
    '--version : Show current version of program',
    '--contain [text] : Filter file and folder by [text]',
    '--target [target_dir] : Target folder need to clean by [target_dir]',
    '--help : Show help',
    '',
    '-- End CleanDesk Help --',
    ''
]

def get_help():
    for str in helpStr:
        print(str)