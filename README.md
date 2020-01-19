# Backup Script

This script recursively iterates through a given directory (passed in through 
the `--original` flag) and copies all the files from that directory to a given
replica directory (passed in through the `--replica` flag).

The original directory's folder structure is replicated in the replica
directory.

If a file with the same name exists in both the original and replica
directories, then the file is only updated if the file contents are not the
same.

This script also outputs any extraneous files and folders that exist in the
replica directory but do not exist in the original directory.

No files from the original directory should be modified or deleted.

Usage:
```
./backup.py -o <original folder path> -r <replica folder path>
```
