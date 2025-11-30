#!/usr/bin/venv python3
###############################################
#  Dusza Árpád Országos Programozói           #
#   Emlékverseny - I. Forduló | Hagyományos   #
###############################################
#  2025 / 2026                                #
#                                             #
#  Team: KVM                                  #
#  Team participants:                         #
#    - Kis Vilmos Bendegúz                    #
#    - Menyhárd Nándor                        #
#    - Vigh-Bucz Hunor                        #
###############################################

import sys
import data.ui.init as windowManager
from data.prototypes.test_processor import start

def main() -> None:
    windowManager.init()
    if len(sys.argv) == 1:
        print("Használat: python main.py [--ui | <test_dir_path>]")
        sys.exit(1)
    
    if sys.argv[1] == "--ui":
        ## GUI Stuff
        #gdparser.parse() 
        windowManager.init()
        # Don't touch dis, go to data/ui/

    else:
        ## Test mode
        start(sys.argv[1])

if __name__ == "__main__":
    main()
    sys.exit(0)