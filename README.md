<h1 align="center">
S1ckNerd
 </h1>

CLI tool for making Google Dorking a passive recon experience.
## Getting Started

-   [Usage](#usage)
-   [Install](#install)
-   [Output](#output)

## Usage
```sh
s1cknerd.py -h

usage: main.py [-h] [-i INPUT] [-o OUTPUT] [-d DORKS] [-p] [-q]

CLI tool for making Google Dorking a passive recon experience

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input list of domains (no subdomains).
  -o OUTPUT, --output OUTPUT
                        Prints CSV files to directory. The default is cwd.
  -d DORKS, --dorks DORKS
                        List of Dorks to test (optional)
  -p, --passive         Skip the validation requests and only do passive checks.
  -q, --quiet           Hides banner


```
Take a list of domains and google dork them.
```
s1cknerd.py -i domains.txt

cat domains.txt | s1cknerd.py
```
Skip requesting each URL and only do passive checks.
```
cat domains.txt | s1cknerd.py -p
```
Use another list of dorks instead of the defaults
```
cat domains.txt | s1cknerd.py -d dorks.txt
```
Only do passive checks, use another list of dorks, and change output directory
```
s1cknerd.py -i domains.txt -d dorks.txt -p -o ./dork-out/
```

## Install
**S1ckNerd** works on Windows and *Nix systems and requires Python.
```
git clone 
```
```
pip install -r requirements.txt
```
## Output
The `-o` flag is used to direct the CSV output file to a directory. Output file is comma seperated.
```
cat s1cknerd-output.csv | csvtomd
```
### s1cknerd-output.csv
|QUERY|URL|HTTP CODE|TITLE|CONTENT LENGTH|
|---|---|--|--|--|
|Dork searched|URL result from Dork|HTTP Code of request|HTTP Title|Content length of HTTP request|

#### *HTTP CODE, TITLE, and CONTENT LENGTH are only available if passive is disabled (default)
