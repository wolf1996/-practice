# Агрегатор результатов анализа кода
## Поддерживаемые анализаторы
+ clang ([scan-build](http://clang-analyzer.llvm.org/scan-build.html))
+ [cppcheck](http://cppcheck.sourceforge.net/)

## Инструкция
Версия Python 

> Python 3.4.3

точка входа 

>	agregator.py

## использование

> agregator.py [-h] [--config CONFIG] path

где 
CONFIG - путь до конфигурационного файла
path - путь до анализируемого кода 

## Пример запуска
### комманда запуска 

< agregator.py --config test.cfg /pathtocode/>

### test.cfg

<#Application section
 [app]
 #default logfile log.txt
 logfile = log2.txt
 #analyzers section, flags in flags section, other options use normal names
 
 [clang]
 #flags with all additional symbols
 flags =-v,-v,-v,-v
 #options, without additional symbols
 configcommand = bash ./autogen.sh
 makecommand = make -j8
 cleancommand = make clean
 
 [cppcheck]
 flags = -v 3, -j 8>
