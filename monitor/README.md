-- aquest modul s'encarrega de realitzar visualitzacions carregant les dades del servidor mongodb remot


-- exemple de servidor mongodb disponible

https://mongolab.com/databases/benchbox

## To connect using the shell:
	mongo ds055822.mongolab.com:55822/benchbox -u <dbuser> -p <dbpassword>
## To connect using a driver via the standard URI (what's this?):
    mongodb://<dbuser>:<dbpassword>@ds055822.mongolab.com:55822/benchbox


-- el mongo server podria trobarse aqui, pero nomes seria accessible en proves locals, encanvi si estiguesi en
mongolabs seria accessible desde qualsevol lloc
-- TODO exportar los logs en formato csv



# TODO:

share this folder with sandBox
add a python script in this folder which monitors the cpu, ram, disk, network usage in a logs file. "append overwrite"