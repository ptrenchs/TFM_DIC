import numpy as np

class optical_flow:
    def encontrar(cordenadas, valor_ref, matriz):
        i,j = cordenadas
        if matriz[i][j] == valor_ref:
            return [i,j]
        nxn = 1

        while True:
            n = int((nxn - 1) / 2)
            if i < n:
                sup_i = i
                inf_i = n + 1
            elif n <= i and  i < len(matriz) - n:
                sup_i = n
                inf_i = n + 1
            else:
                sup_i = n
                inf_i = len(matriz) - i

            if j < n:
                iz_j = j
                der_j = n + 1
            elif n <= j and  j < len(matriz[i]) - n:
                iz_j = n
                der_j = n + 1
            else:
                iz_j = n
                der_j = len(matriz[i]) - j

            start_i = i - sup_i
            stop_i = i + inf_i

            start_j = j - iz_j
            stop_j = j + der_j

            submatriz = np.abs(matriz[start_i:stop_i, start_j:stop_j] - valor_ref)

            val_min = np.min(submatriz)
            if val_min < 2:
                pos = np.where(submatriz == val_min)
                modulo = []
                for k in range(len(pos[0])):
                    modulo.append(abs(pos[0][k] - sup_i + 1j * (pos[1][k] - iz_j)))
                pos_pos = np.where(np.array(modulo) == np.min(modulo))
                pos_pos = pos_pos[0][0]
                delta_y = pos[0][pos_pos] - sup_i
                delta_x = pos[1][pos_pos] - iz_j
                pi,pj = i + delta_y, j + delta_x
                return [int(pi),int(pj)], delta_x, delta_y
            # if 7 <= nxn:
            #     return [i,j]
            nxn += 2