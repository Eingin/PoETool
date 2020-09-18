#!/usr/bin/env python3

from nubia import command, argument
from termcolor import cprint, colored
import sys
import struct
from io import IOBase

from ...utils.fnv import fnv64a
from ...parsers.bundle import GGGBundle
from ...parsers.index import BundleIndex

@command
class Bundle:
    "Command for handling bundle files"

    @command
    @argument("path", type=str, description="Index path", positional=True)
    @argument("file", type=str, description="File to lookup")
    def index(self, path: str, file: str = None):
        """
        Loads a decompressed bundle index
        """
        with open(path, "rb") as reader: 
            index = BundleIndex(reader)
            cprint("bundleCount={}".format(colored(index.bundleCount, "green")))
            cprint("fileCount={}".format(colored(index.fileCount, "green")))
            cprint("pathCount={}".format(colored(index.pathCount, "green")))
            if(file != None):
                fileHash = fnv64a(file.lower() + "++")
                cprint("file hash={}".format(colored(hex(fileHash), "red")))
                fileInfo = index.files.get(fileHash)
                if(fileInfo != None):
                    cprint("Found file!")
                    bundleInfo = index.bundles[fileInfo.bundleIndex]
                    cprint("bundle={}".format(colored(bundleInfo.name, "green")))
                    cprint("section={} - {}".format(
                        colored(hex(fileInfo.fileOffset), "green"),
                        colored(hex(fileInfo.fileOffset + fileInfo.fileSize), "green")
                    ))
                else:
                    cprint("Unable to find file :(")

    @command
    @argument("path", type=str, description="Bundle file path", positional=True)
    def load(self, path: str):
        """
        Loads a bundle file into the context
        """
        with open(path, "rb") as reader: 
            bundle = GGGBundle(reader)
            cprint("uncompressedSize={}".format(colored(bundle.uncompressedSize, "green")))
            cprint("payloadSize={}".format(colored(bundle.payloadSize, "green")))
            cprint("headerSize={}".format(colored(bundle.headerSize, "green")))
            cprint("startCompressor={}".format(colored(bundle.header.startCompressor, "green")))
            cprint("uncompressedSize={}".format(colored(bundle.header.uncompressedSize, "green")))
            cprint("payloadSize={}".format(colored(bundle.header.payloadSize, "green")))
            cprint("chunkCount={}".format(colored(bundle.header.chunkCount, "green")))
            cprint("chunkSize={}".format(colored(bundle.header.chunkSize, "green")))

    @command
    @argument("inPath", type=str, description="Bundle file path", positional=True)
    @argument("outPath", type=str, description="Output path for decompressed data")
    def decompress(self, inPath, outPath: str = ""):
        """
        Attempts to decompresses the open bundle file and optionally saves the reuslting data into a file
        """
        with open(inPath, "rb") as reader: 
            bundle = GGGBundle(reader)

            cprint("Starting decompression...", "cyan")
            result = bundle.decompress(reader)
            if result > 0:
                cprint("Decompression finished {}".format(result), "cyan")
                if outPath != "":
                    cprint("Saving to {}".format(outPath))
                    with open(outPath, "wb") as writer:
                        writer.write(bundle.decompressedBuffer)
                    cprint("Saved")
            else:
                cprint("Decompression failed!", "red")
