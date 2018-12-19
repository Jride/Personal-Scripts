# Personal-Scripts

A set of personal python scripts

### Installation:

Clone the repo then

```
cd path/to/repo
sh setup.sh
```

This will install a pre-commit hook that compiles all of the scripts to ensure that they don't have syntax errors before allowing a commit to git.

```
for file in path/to/repo/Aliases/*
do
  source $file
done
```
