# Processor Performance Factors

The coursework instructions can be found [here.](https://secure.ecs.soton.ac.uk/noteswiki/images/2020_gem5_assignment_v1.pdf)

# Compilation

To compile, you can run the commands
```
pdflatex --shell-escape report.tex
pdflatex --shell-escape report.tex
bibtex report
pdflatex --shell-escape report.tex
```

and `report.pdf` should appear!

Alternatively, I reccomend using the command
```
latexmk --pdf --shell-escape report --pvc -r <(echo '$pdf_previewer = "zathura"')
```
or something like it.
This will auto-recompile and display any changes as you make them.

# Graphs

Each of the graphs is compiled seperately using the
[standalone package](https://ctan.org/pkg/standalone?lang=en). You can
edit the line `\usepackage[mode=...]{standalone}` in `report.tex` to
change the method of compilation, if you need that.

# Sections

Each of the sections has a file in the directory `sections/`. The file is
simply input into the main report.tex file, and therefore is not a complete
LaTeX document.

# Structure

We're writing our report in LaTeX because it's fashionable, and we
like to be smug.

The directory structure works something like this...

```
|-csv               ; Directory containing our CSV results!
| |                 ;  (whose we use we can decide soon)
| |-A               ; Each question has its own subdirectory.
| | |- arm-crc.csv  ; The files are named with the arch and benchmark
| | `- ...          ;  that they contain information for.
| |-B
| | `- ...
| |-C
| | `- ...
| `-D
|   `- ...
|
|-graphs            ; A directory containing graphs and figures!
| |- parta-cpi.tex  ; Each of these is a tex file with
| `- ...            ;  \documenttype{standalone}
|
|-run_scripts       ; A directory containing any scripts or things we used to
| |- hugo.py        ;  make our data. Not for the report or anything, but just
| `- ...            ;  for posterity.
|
|-sections          ; A directory containing each of the sections of our report.
| |- partA.tex      ;  Each of the sections is simply \input into our final pdf.
| |- partB.tex      ;  Unlike the graphs, there is no precompilation, and they
| |- partC.tex      ;  do not need to compile standalone or anything. Just
| `- partD.tex      ;  write the content of the sections themselves.
```
