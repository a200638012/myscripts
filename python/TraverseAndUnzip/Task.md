# Project
Traverse a dir and unzip the zipped file into the same dir, Then generate a report

## Step
1. input a dir name
2. Traverse the dir
3. list all zipped file as a file tree into {dir}/report/{dir}.md
4. unzipped all zipped file into a new dir which have the same name with the zipped file
5. Traverse the dir and check whether have zipped file, do step 4 until the dir has no zipped files
5. generate a report show the zipped file and unzipped file
6. delete all zipped files after all files unzipped
7. list all files in the dir as a file tree {dir}/report/{dir}_unzipped.md
