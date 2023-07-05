print("\n------------ TABELA TRANCADA ------------\n")

tabela = input("Nome da tabela: ")

print("\nselect pg_terminate_backend(pid) from pg_locks where relation=(select oid from pg_class where relname=\'"+tabela+"\') and mode like '%ExclusiveLock';")