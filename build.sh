#!/bin/bash
#
# My script to compile everything - Requires latexmk and zathura

latexmk --pdf --shell-escape report --pvc -r <(echo '$pdf_previewer = "zathura"')
