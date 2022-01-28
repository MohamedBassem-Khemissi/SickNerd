<h1 align="center">
SickNerd
 </h1>

CLI tool for making Google Dorking a passive recon experience. **SickNerd** aims to slowly enumerate Google Dorks via
the `googlesearch` API then requests found pages for metadata. By default it sleeps between queries, randomizes
user-agent, retries 429 and failed requests recursively, and prints output after each query. Validation requests are
done when all of the dorks have been collected. **SickNerd** comes with a default list of dorks aimed at finding
sensitive files but accepts input files and can dork multiple domains at once. Dorks can be fetched from GHDB or put in
an input file and are run at random.

## Getting Started

- [Usage](#usage)
- [Install](#install)
- [Output](#output)

## Usage

```sh
sicknerd.py -h

usage: sicknerd.py [-h] [-i INPUT] [-o OUTPUT] [-f FETCH | -d DORKS] [-p] [-q]
                   [-y YEARS] [-m MAX]

CLI tool for making Google Dorking a passive recon experience

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input list of domains (no subdomains).
  -o OUTPUT, --output OUTPUT
                        Prints CSV files to directory. The default is cwd.
  -f FETCH, --fetch FETCH
                        Fetches lists of dorks from GHDB. Accepts one of the
                        following: all, footholds, dir, web, files, servers,
                        errors, juicy, passwords, shopping, login, devices,
                        vulns (optional)
  -d DORKS, --dorks DORKS
                        List of Dorks to test (optional)
  -p, --passive         Skip the validation requests and only do passive
                        checks.
  -q, --quiet           Hides banner
  -y YEARS, --years YEARS
                        Number of years to fetch dorks from. Default is 2.
  -m MAX, --max MAX     Max number of results per query. Default is 30.

Process finished with exit code 0

```

Take a list of domains and google dork them.

```
sicknerd.py -i domains.txt

cat domains.txt | sicknerd.py
```

Skip requesting each URL and only do passive checks.

```
cat domains.txt | sicknerd.py -p
```

Use another list of dorks instead of the defaults

```
cat domains.txt | sicknerd.py -d dorks.txt
```

Only do passive checks, use another list of dorks, and change output directory

```
sicknerd.py -i domains.txt -d dorks.txt -p -o ./dork-out/
.▄▄ · ▪   ▄▄· ▄ •▄  ▐ ▄ ▄▄▄ .▄▄▄  ·▄▄▄▄  
▐█ ▀. ██ ▐█ ▌▪█▌▄▌▪•█▌▐█▀▄.▀·▀▄ █·██▪ ██ 
▄▀▀▀█▄▐█·██ ▄▄▐▀▀▄·▐█▐▐▌▐▀▀▪▄▐▀▀▄ ▐█· ▐█▌
▐█▄▪▐█▐█▌▐███▌▐█.█▌██▐█▌▐█▄▄▌▐█•█▌██. ██ 
 ▀▀▀▀ ▀▀▀·▀▀▀ ·▀  ▀▀▀ █▪ ▀▀▀ .▀  ▀▀▀▀▀▀• 
Loaded 3 dorks...
[*] Starting file searches...
Max 30 results per query
Found 3 results from site:apple.com filetype:txt
Found 1 results from site:cia.gov filetype:txt
Found 1 results from site:fbi.gov filetype:txt
Found 30 results from site:apple.com inurl:admin
Found 0 results from site:cia.gov inurl:admin
Found 0 results from site:fbi.gov inurl:admin
Found 30 results from site:apple.com filetype:pdf
Found 30 results from site:cia.gov filetype:pdf
Found 30 results from site:fbi.gov filetype:pdf
Found 0 results from site:apple.com db_password filetype:env
Found 0 results from site:cia.gov db_password filetype:env
Found 0 results from site:fbi.gov db_password filetype:env
[*] Validating results...
Writing 125 results to file
```

Fetch dorks from Google Hacking Database and run vuln dorks from the past two years with max 20 results per query.

```
sicknerd.py -i urls.txt -f vulns -y 2 -m 20
.▄▄ · ▪   ▄▄· ▄ •▄  ▐ ▄ ▄▄▄ .▄▄▄  ·▄▄▄▄  
▐█ ▀. ██ ▐█ ▌▪█▌▄▌▪•█▌▐█▀▄.▀·▀▄ █·██▪ ██ 
▄▀▀▀█▄▐█·██ ▄▄▐▀▀▄·▐█▐▐▌▐▀▀▪▄▐▀▀▄ ▐█· ▐█▌
▐█▄▪▐█▐█▌▐███▌▐█.█▌██▐█▌▐█▄▄▌▐█•█▌██. ██ 
 ▀▀▀▀ ▀▀▀·▀▀▀ ·▀  ▀▀▀ █▪ ▀▀▀ .▀  ▀▀▀▀▀▀• 
Requesting data from https://www.exploit-db.com/google-hacking-database...
Searching for vulns dorks from the past 2 years...
Loaded 214 dorks...
[*] Starting file searches...
Max 20 results per query
Found 0 results from site:apple.com inurl:wp-content/plugins/final-tiles-grid-gallery-lite
Found 0 results from site:cia.gov inurl:wp-content/plugins/final-tiles-grid-gallery-lite
Found 0 results from site:fbi.gov inurl:wp-content/plugins/final-tiles-grid-gallery-lite
[*] CTRL + C pressed! Starting validation then writing output...
[*] Validating results...
Writing 0 results to file
Writing 0 results to file
```

## Install

**SickNerd** works on Windows and *Nix systems and requires Python.

```
git clone 
```

```
pip install -r requirements.txt
```

## Output

The `-o` flag is used to direct the CSV output file to a directory. Output file is comma seperated.

```
cat sicknerd-output.csv | csvtomd
```

### sicknerd-output.csv

|QUERY|URL|HTTP CODE|TITLE|CONTENT LENGTH| |---|---|--|--|--| |Dork searched|URL result from Dork|HTTP Code of
request|HTTP Title|Content length of HTTP request|

#### *HTTP CODE, TITLE, and CONTENT LENGTH are only available if passive is disabled (default)
