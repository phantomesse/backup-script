Original
Replica

In original directory A, iterate through every folder and subfolder.
Replicate the entire folder structure in folder B.
For every file in original directory, if the file with the same name exists in 
the replica directory, then compare hashes. If the hashes are different, replace
the file in the replica directory with the file from the original directory.

If the file doesn't exist, then copy it to the replica directory.

The goal is to make sure that the replica directory always has the same stuff
as the first one.

If the replica directory has extra stuff that the original directory doesn't
have, then leave it alone. Print out a report of these extra things with full
paths.

Whatever you do, don't delete anything from the original directory.

Make this a python script because Aftab is stupid.

Usage:
```
./backup.py -o <original folder path> -r <replica folder path>
```
