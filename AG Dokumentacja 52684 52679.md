# Algorytm genetyczny
Kacper Grzesik 52684, Dominik Górski 52679
## 1. main.py
Główny plik zawierający algorytm genetyczny.
##### a) Podanie danych wejściowych

| Nazwa zmiennej           | Znaczenie                  |
| ------------------------ | -------------------------- |
| generate_population_size | populacja na generację     |
| generation_limit         | maksymalna ilość generacji |
| mutation_probability     | szansa na mutację          |
| file                     | plik do analizy            |
| file_optimum             | plik z optimum             |
| verbose                  | czy printować output       |
|                          |                            |

![[Pasted image 20251114172219.png]]

##### b) Ustalenie funkcji selekcji oraz krzyżowania w ewolucji
Odbywa się to przez komentowanie niepotrzebnych funkcji. Zostało to rozszerzone w podpunktach związanych z rysowaniem wykresów.

![[Pasted image 20251114172613.png]]


##### c) Uzyskanie wyników (jeśli verbose = True)
![[Pasted image 20251114172730.png]]


# 2. draw_chart.py
Generowanie wykresu na podstawie programu main.py.
Program musiał zostać zmodyfikowany tak, aby śledzić jednostkę o najwyższym fitnessie dla każdej ewolucji.

![[Pasted image 20251114172912.png]]

# 3. experiments.py
Program rysuje wykresy dla różnych parametrów funkcji algorytmu genetycznego za pomocą biblioteki matplotlib.pyplot

##### a) Dane początkowe
![[Pasted image 20251114173141.png]]

##### b) Dane wyjściowe (wykresy)

### Wykresy dla różnych współczynników mutacji i krzyżowania:
![[Pasted image 20251114173244.png]]

### Wykresy porównujące selekcję rankingową, ruletkową oraz turniejową, krzyżowanie jedno i dwupunktowe:
![[Pasted image 20251114173415.png]]