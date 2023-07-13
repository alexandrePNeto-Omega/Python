# -*- coding: utf-8 -*-
print("\n------------ TABELA TRANCADA ------------\n")

while True:

    tabela = input("Nome da tabela: ").replace(' ', '')

    if tabela == 'stop':
        break

    print("\nselect pg_terminate_backend(pid) from pg_locks where relation=(select oid from pg_class where relname=\'"+tabela+"\') and mode like '%ExclusiveLock';")
    print("\n+-------------+\n")

print("\n---------- PROGRAMA FINALIZADO ----------\n")