"""
omersahinesk@gmail.com
created: 2020-01-15
revised: 2022-06-05
"""
import numpy as np
import random
import math
import time
from matplotlib import pyplot as plt


def create_matrix(minValue, maxValue, size):
    matris = np.zeros((size, size))
    for i in range(len(matris)):
        for j in range(len(matris)):
            if i != j:
                matris[i][j] = random.randint(minValue, maxValue)
    return np.array(matris, dtype=int)


def calculate_obj_funct(matrix, solution):
    obj_solution = solution.copy()
    z = 0
    size = len(obj_solution)
    obj_solution.append(obj_solution[0])
    for i in range(size):
        z += matrix[obj_solution[i]][obj_solution[i + 1]]
    return z
    # for i in range(solution):
    #     z += matrix[i][solution.index(i)+1]


def move_swap(solution):
    move_solution = solution.copy()
    element = random.sample(move_solution, 2)
    move_solution[move_solution.index(element[1])], move_solution[move_solution.index(element[0])] \
        = element[0], element[1]
    return move_solution


def move_insert(solution):
    move_solution = solution.copy()
    element = random.sample(move_solution, 2)
    ikinci_sira_no = move_solution.index(element[1])
    move_solution.remove(element[0])
    move_solution.insert(ikinci_sira_no, element[0])
    return move_solution


def move_reverse(solution):
    move_solution = solution.copy()
    element = random.sample(range(len(move_solution) - 1), 2)
    element.sort()
    reverseList = move_solution[element[0]:element[1] + 1].copy()
    reverseList.reverse()
    move_solution[element[0]:element[1] + 1] = reverseList
    return move_solution


def simulated_annealing_moves(rastgele_cozum, rastgele_cozum_amac_fnk, mesafeler_matris, sicaklik):
    cozum_sec = random.randint(1, 3)
    if cozum_sec == 1:
        yeni_rastgele_cozum = move_swap(rastgele_cozum)
    if cozum_sec == 2:
        yeni_rastgele_cozum = move_insert(rastgele_cozum)
    else:
        yeni_rastgele_cozum = move_reverse(rastgele_cozum)

    yeni_rastgele_cozum_amac_fnk = calculate_obj_funct(mesafeler_matris, yeni_rastgele_cozum)

    if yeni_rastgele_cozum_amac_fnk < rastgele_cozum_amac_fnk:
        return yeni_rastgele_cozum, yeni_rastgele_cozum_amac_fnk
    else:
        random_value = random.random()
        boltzman_value = math.exp(((yeni_rastgele_cozum_amac_fnk - rastgele_cozum_amac_fnk) / sicaklik))
        if boltzman_value >= random_value:
            return yeni_rastgele_cozum, yeni_rastgele_cozum_amac_fnk
        else:
            return rastgele_cozum, rastgele_cozum_amac_fnk


matrix_min = int(input("Matris'in en küçük değerini seçin:"))
matrix_max = int(input("Matris'in en büyük değerini seçin:"))
matrix_size = int(input("Matris'in boyutunu seçin:"))
heat = int(input("Tavlama Benzetimi için sıcaklık değeri girin:"))
iterCount = int(input("Tavlama Benzetimi için sıcaklık başına iterasyon sayısını girin:"))

starttime = time.time()

mesafeler_matris = create_matrix(matrix_min, matrix_max, matrix_size)
print(mesafeler_matris)

baslangic_cozum = random.sample(range(matrix_size), matrix_size)
print(baslangic_cozum)

amac_fonk = calculate_obj_funct(mesafeler_matris, baslangic_cozum)
print(amac_fonk)

en_iyi_cozum = baslangic_cozum.copy()
en_iyi_amac_fnk = amac_fonk
rastgele_cozum = baslangic_cozum.copy()
rastgele_cozum_amac_fnk = amac_fonk

gelistirmeler = []

iterasyon_sayac = 0
while True:
    # Sıcaklık azaltması
    if iterasyon_sayac % iterCount == 0:
        heat = heat * 0.99
    iterasyon_sayac += 1

    # Sıcaklık kontrolü
    if heat <= 1:
        print("Algoritma sona erdi.")
        break

    rastgele_cozum, rastgele_cozum_amac_fnk = simulated_annealing_moves(rastgele_cozum, rastgele_cozum_amac_fnk,
                                                                        mesafeler_matris, heat)

    if rastgele_cozum_amac_fnk < en_iyi_amac_fnk:
        en_iyi_amac_fnk = rastgele_cozum_amac_fnk
        en_iyi_cozum = rastgele_cozum.copy()
        gelistirmeler.append(en_iyi_amac_fnk)
        print("yeni en iyi cozum bulundu -->", "En iyi Cozum", en_iyi_amac_fnk, "  -->", en_iyi_cozum)

# open()
# matplotlib (gelistirmeler.)

print("Calisma Zamani = ", time.time() - starttime)
print("Algoritma sonucları yazdırılıyor:")
print("...")
time.sleep(3)
print("En iyi Cozum", en_iyi_amac_fnk, "  -->", en_iyi_cozum)

plt.plot(gelistirmeler)
plt.show()
