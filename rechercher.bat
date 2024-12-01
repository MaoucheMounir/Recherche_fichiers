@echo off
call activate workspace11
cd /d "C:\_Programmation\recherche_fichiers"
python rechercher.py  %*
pause
