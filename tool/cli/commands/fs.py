from nubia import command, argument
from termcolor import cprint, colored
import mmap

from ...parsers.ggpk import GGPK

@command
@argument("path", type=str, description="Index path", positional=True)
def loadGGPK(path: str, file: str = None):
    """
    Loads a ggpk into the context
    """
    with open(path, "rb") as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmapFile:
            ggpk = GGPK(mmapFile)
            cprint("Indexing...")
            ggpk.index(mmapFile)
            cprint("Indexed!")
            ggpk.render()
