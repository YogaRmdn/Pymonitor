import os
import platform
from options.colors import *

def clean_screen():
    os.system("cls" if platform.system() == "nt" else "clear")

def header():
    print(f"""{b_g}
           ___                     _ _           
          | _ \_  _ _ __  ___ _ _ (_) |_ ___ _ _ 
          |  _/ || | '  \/ _ \ ' \| |  _/ _ \ '_|
          |_|  \_, |_|_|_\___/_||_|_|\__\___/_|   V1
               |__/                              
{b_w}[1] Bima maulana  | [2] Zakfa annur rahmansyah  | [3] Yoga ramadani
*******************************************************************
{rs}""")