from simplex import KSimplex


class Boundary:
    def __init__(self):
        self.boundary = []

    def compute_boundary(self, k_simplex):
        '''
        Computes the boundary of a k_simplex.
        :param k_simplex: KSimplex object
        '''
        # if k_simplex.k == 1:
        #   return (0,)
        indexlist = k_simplex.kvertices
        start = 0
        end = len(indexlist)
        mid = 0
        if end == 1:
            return []
        for mid in range(start, end):
            self.boundary.append(((1) ** mid, KSimplex(indexlist[start:mid] + indexlist[mid + 1:end])))
        return self.boundary

    def get_boundary(self):
        '''
        Returns the boundary of the K-simplex
        :return: list of tuples like ( sign(+ or -) , K-Simplex Object )
        '''
        return self.boundary

    def __str__(self):
        str_repr = ''
        for sign, simplex in self.boundary:
            str_repr += (['+', '-'][sign == -1] + str(simplex.kvertices) + " ")

        return str_repr
