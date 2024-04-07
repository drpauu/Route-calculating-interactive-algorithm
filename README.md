# Craxify-Machine-Learning
## Preparació
En aquesta secció, s’explica pas a pas com preparar un entorn de desenvolupament local en un sistema basat en Ubuntu, incloent-hi la instal·lació de Python i diverses llibreries útils com Matplotlib, NetworkX, Graphviz i pyvis. Aquestes llibreries són fonamentals per a la visualització de dades, l'anàlisi de xarxes i les tasques relacionades amb la geolocalització en Python.

### Actualitzar el sistema
Abans de començar amb la instal·lació de les llibreries, és recomanable actualitzar el sistema per assegurar-se que es tenen les darreres versions de tots els paquets disponibles. Per fer-ho, s’ha d’executar la següent comanda:

```
sudo apt-get update
```

Aquesta comanda actualitzarà la llista de paquets disponibles i les seves versions al sistema.

### Instal·lar Python 3
Python és un llenguatge de programació de codi obert àmpliament utilitzat per a una gran varietat d'aplicacions. En aquest cas, instal·larem la versió 3 de Python, que és la versió més recent i recomanada en molts casos. Executa la següent comanda per instal·lar Python 3:

```
sudo apt-get install python3 -y
```

### Instal·lar pip (Gestor de paquets de Python)
Pip és una eina que ens permet instal·lar i gestionar paquets de Python addicionals que no estan inclosos en la distribució estàndard. La següent comanda ens permetrà instal·lar pip per a Python 3:

```
sudo apt-get install python3-pip -y
```

### Instal·lar Matplotlib
Matplotlib és una llibreria de Python que ens permet generar gràfics de gran qualitat amb facilitat. És una eina fonamental per a la visualització de dades en Python. Per instal·lar Matplotlib, utilitza la següent comanda:

```
sudo apt-get install python3-matplotlib -y
```

### Instal·lar NetworkX
NetworkX és una llibreria de Python per a l'anàlisi de xarxes i grafs. És una eina potent per a la creació, la manipulació i l'estudi d'estructures de xarxes complexes. Per instal·lar NetworkX, utilitza la següent comanda:

```
sudo apt-get install python3-networkx -y
```

### Instal·lar Graphviz
Graphviz és una eina per a la visualització de grafs i xarxes. És especialment útil quan es vol representar visualment les estructures de xarxes generades amb NetworkX. Per instal·lar Graphviz, utilitza la següent comanda:

```
sudo apt-get install python3-graphviz -y
```

### Instal·lar pyvis
Pyvis és una llibreria de Python per a la visualització interactiva de xarxes i grafs. Proporciona una manera senzilla de crear representacions visuals interactives de les xarxes generades amb NetworkX. Per instal·lar pyvis, utilitza la següent comanda:

```
sudo pip3 install pyvis
```

### Clonar el repositori git
Un cop has preparat el teu entorn de desenvolupament local i instal·lat totes les biblioteques necessàries, el següent pas és clonar el repositori Git que conté el codi font del projecte. Assumint que ja tens Git instal·lat i configurat, pots executar la següent instrucció al teu terminal:

```
git clone https://github.com/CRAAXify/Craxify-Machine-Learning.git
```

## Execució
Per executar el script find_route.py, obre una terminal i navega fins al directori on es troba el fitxer. A continuació, executa la següent comanda:

```
python3 find_route.py
```

Amb això, l'script s'executarà utilitzant Python 3 i podreu començar a utilitzar-lo per trobar rutes segons calgui.
