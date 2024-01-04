#!/usr/bin/env python3

from picture import Picture

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        height = self.height()
        width = self.width()
        if (i < 0) or (j < 0) or (i >= height) or (j >= width):
            raise IndexError
        
        R_1, G_1, B_1 = self[(i+1) % (width), j] #lower pixel
        R_2, G_2, B_2 = self[(i-1) % (width), j] #upper pixel
        R_3, G_3, B_3 = self[i, (j+1) % (height)] #right pixel
        R_4, G_4, B_4 = self[i, (j-1)% (height)] #left pixel
        
        #values for y-gradient
        R_y = (R_1 - R_2) ** 2
        G_y = (G_1 - G_2) ** 2
        B_y = (B_1 - B_2) ** 2
        y_gradient = R_y + G_y + B_y
        
        #values for x-gradient
        R_x = (R_3 - R_4) ** 2
        G_x = (G_3 - G_4) ** 2
        B_x = (B_3 - B_4) ** 2
        x_gradient = R_x + G_x + B_x
        
        energy_value = x_gradient + y_gradient
        return energy_value
        raise NotImplementedError

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        # self.height = self.height()
        # self.width = self.width()
        height = self.height()
        width = self.width()
        seam = [0] * height
        min_energy = [[0 for i in range(width)] for j in range(height)]
        seams = [[0 for i in range(width)] for j in range(height)]
        for x in range(width): #bottom row energies
            min_energy[height-1][x] = self.energy(x,height-1)
            seams[height-1][x] = [x]
            
        for j in range(height-2,-1,-1):
            for i in range(width): 
                e1 = self.energy(i,j)
                i_1 = max(0, i-1) #prevents going over to the left
                i_2 = min(i+1, width-1) #prevents going over to the right
                a = min_energy[j+1][i_1]
                b = min_energy[j+1][i]
                c = min_energy[j+1][i_2]
                e2 = min(a,b,c) #finds the minimum among the three pixels below
                if e2 == a: #for backtracking
                    seams[j][i] = [i] + seams[j+1][i_1]
                elif e2 == b:
                    seams[j][i] = [i] + seams[j+1][i]
                elif e2 == c:
                    seams[j][i] = [i] + seams[j+1][i_2]
                print(seams[j][i])
                min_energy[j][i] = e1 + e2
        minimum = min_energy[0].index(min(min_energy[0]))#takes the index of the minimum total energy of top 
        answer = seams[0][minimum]
        # print(answer)
        return answer
        # raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        width = self.width()
        height = self.height()
        if width == 1 or height == 1: #SeamError if height or width is 1
            raise SeamError
        if height != (len(seam)): #SeamError if list is wrong length
            raise SeamError
        for x in range(len(seam)-1): #SeamError if invalid seam
            a = abs(seam[x] - seam[x+1])
            if a > 1: #Two consecutive entries differ more than 1
                raise SeamError
        for j in range(height):
            i = seam[j]
            right = width - i -1
            for k in range(right):
                self[i+k,j] = self[i+k+1,j]
            del self[width-1,j]
        self._width -= 1
        # raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        width = self.width()
        height = self.height()
        if width == 1 or height == 1: #SeamError if height or width is 1
            raise SeamError
        # if self._width != (len(seam)): #SeamError if list is wrong length
            # raise SeamError
        for j in range(width):
            i = seam[j]
            right = height - i -1
            for k in range(right):
                self[j,i+k] = self[j,i+k+1]
            del self[j,height-1]
        self._height -= 1
        # raise NotImplementedError
        
        # seam.reverse()
        height = self.height()
        width = self.width()
        new = [0] * width
        for x in range(len(seam)):
            new[x] = height - seam[x] -1
        self.rotate_90() 
        self.flip_left_right()
        self.flip_top_bottom()
        # for i in range(len(new)):
            # j = new[i]
            # print(self[j,i])
        self.remove_vertical_seam(new)
        self.rotate_90()
        # self.flip_left_right()

class SeamError(Exception):
    pass
