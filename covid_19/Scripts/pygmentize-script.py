#!C:\hacaton\covid_19\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Pygments==2.6.1','console_scripts','pygmentize'
__requires__ = 'Pygments==2.6.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Pygments==2.6.1', 'console_scripts', 'pygmentize')()
    )
