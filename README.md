# Augstuma starpības un slīpuma kalkulators

Šī programma ļauj aprēķināt augstuma starpību un slīpumu starp diviem punktiem, kā arī vizualizēt to grafiski.

## Funkcijas

- Augstuma starpības aprēķins starp diviem punktiem
- Slīpuma aprēķins un klasifikācija (viegls, mērens, stāvs)
- Grafisks attēlojums ar kalnu siluetu
- Iespēja pievienot papildu punktus reljefa attēlojumam
- Sagatavoti datu piemēri ātrai demonstrācijai
- Vairākas vizuālās tēmas (Standarta, Tumšā, Zilā, Rozā)
- Pielāgojami grafika un pogu stili
- Animāciju efekti vizualizācijā

## Prasības

- Python 3.6 vai jaunāka versija
- Bibliotēkas:
  - tkinter
  - matplotlib
  - numpy

## Programmas palaišana

Lai palaistu kalkulatoru:

1. Pārliecinieties, ka datorā ir instalēts Python 3.6 vai jaunāka versija
   - Pārbaudiet Python versiju, izpildot komandu: `python --version` vai `python3 --version`
   - Ja Python nav instalēts, lejupielādējiet to no [python.org](https://www.python.org/downloads/)

2. Instalējiet nepieciešamās bibliotēkas:
   ```
   pip install matplotlib numpy
   ```
   Piezīme: Tkinter parasti iekļauts Python instalācijā. Ja tas nav pieejams, instalējiet to ar komandu:
   ```
   pip install tk
   ```

3. Lejupielādējiet ASSK.py failu

4. Atveriet komandrindas logu (CMD vai PowerShell) un pārejiet uz mapi, kur glabājas ASSK.py:
   ```
   cd ceļš\uz\mapi
   ```

5. Palaidiet programmu ar komandu:
   ```
   (windows) python ASSK.py
   ```
   vai
   ```
   (mac/linux) python3 ASSK.py
   ```

6. Programmas interfeiss atvērsies jaunā logā

## Lietošana

1. Palaidiet programmu ar komandu: `python ASSK.py`
2. Ievadiet sākuma punkta augstumu metros
3. Ievadiet beigu punkta augstumu metros
4. Ievadiet attālumu starp punktiem metros
5. Nospiediet "APRĒĶINĀT", lai iegūtu rezultātus