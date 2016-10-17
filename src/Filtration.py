#from src.simplex import SimplicialComplex, KSimplex
from src.simplexdisk import SimplicialComplex,KSimplex # For disk based P intervals
from itertools import combinations
__author__ = 'Naheed'


class iFiltration:
    def __init__(self, index):
        self.index = index  # Filtration index
        self.simplicial_complex = SimplicialComplex()

    def add_simplex_to_filtration(self, simplex):
        '''

        :param filtration_index: The index of the filtration
        :param simplex: An instance of KSimplex
        :return:
        '''
        self.simplicial_complex.add_simplex(simplex)

    def get_all_ksimplices(self, k):
        return self.simplicial_complex.get_allkth_simplices(k)

    def has_simplex(self, Ksim):
        assert isinstance(Ksim, KSimplex)
        k = Ksim.k
        for sim in self.simplicial_complex.get_allkth_simplices(k):
            if sim == Ksim:
                return True
        return False

    def __len__(self):
        return len(self.simplicial_complex)

    def __str__(self):
        return str(self.simplicial_complex)


class Filtration:
    def __init__(self):
        self.listof_iFiltration = {} # use shelve here
        self.simplex_to_filtrationmap = {}
        self.maxdeg = 0

    def add_filtration(self, i):
        self.listof_iFiltration[i] = iFiltration(i)

    def get_ithfiltration(self, i):
        return self.listof_iFiltration.get(i, None)

    def get_ksimplices_from_ithFiltration(self, k, i):
        '''
        :param k: K-simplices
        :param i: i-th filtration
        :return: List of Simplex objects from the simplicial complex at i-th filtration
        '''
        return self.get_ithfiltration(i).get_all_ksimplices(k)

    def has_ksimplex_in_ithfiltration(self, KSim, i):
        assert isinstance(KSim, KSimplex)
        return self.get_ithfiltration(i).has_simplex(KSim)

    def add_simplex_toith_filtration(self, i, simplex):
        '''
        :param i: i'th Filtration
        :param simplex: Simplex to add to i'th Filtration may be a list or a KSimplex instance
        :return: None
        '''
        # IF the ifiltration is None create it
        if self.listof_iFiltration.get(i, None) is None:
            self.add_filtration(i)

        # If its a KSimplex instance
        if isinstance(simplex, KSimplex):
            if simplex.degree is None:
                simplex.degree = i
            self.listof_iFiltration[i].add_simplex_to_filtration(simplex)
            self.simplex_to_filtrationmap[tuple(simplex.kvertices)] = i
        else:
            ksimplex = KSimplex(simplex, i)
            self.listof_iFiltration[i].add_simplex_to_filtration(ksimplex)
            self.simplex_to_filtrationmap[tuple(ksimplex.kvertices)] = i

    def add_simplices_from_file(self, filename):
        with open(filename, 'r') as fp:
            while 1:
                line = fp.readline()
                if not line:
                    break
                simplex, filtr_idx = line.split(',')
                ksimplex_obj = KSimplex(sorted([int(v) for v in
                                                simplex.split()]))  # Building the K-simplex object . Always insert them in sorted order to avoid orientation conflict between higher dimensional simplices.
                self.add_simplex_toith_filtration(int(filtr_idx), ksimplex_obj)

    def add_simplices_from_cliquefiles(self, dir):
        base = 'pclique_'
        from os import path, listdir
        for fil in listdir(dir):
            if fil.startswith(base):
                filtr_idx = int(fil.split("_")[1][0])
                print 'adding filtration: ' + str(filtr_idx)
                with open(dir + '/' + fil, 'r') as fp:
                    print 'filename: ',dir + '/' + fil
                    for simplex in fp:
                        # print simplex
                        if not simplex:
                            break
                        #ksimplex_obj = KSimplex(sorted(int(v) for v in simplex.split()))
                        ksimplex_obj = KSimplex(
                            [int(v) for v in simplex.split()])  # They are already assumed to be sorted.
                        #added_already = False
                        #for i in range(filtr_idx - 1):
                         #   if self.has_ksimplex_in_ithfiltration(ksimplex_obj, i):
                          #      added_already = True

                        #if not added_already:
                        self.add_simplex_toith_filtration(filtr_idx - 1, ksimplex_obj)
                            #print 'added', ksimplex_obj
                print 'done adding'

    def add_simplices_from_cliquefiles_ensureinclusion(self, dir):
        base = 'clique_'
        from os import path, listdir
        for fil in listdir(dir):
            if fil.startswith(base):
                filtr_idx = int(fil.split("_")[1][0])
                print 'adding filtration: ' + str(filtr_idx)
                print 'filename: ',dir + '/' + fil
                with open(dir + '/' + fil, 'r') as fp:
                    for simplex in fp:
                        #print simplex
                        if not simplex:
                            break
                        #ksimplex_obj = KSimplex(sorted(int(v) for v in simplex.split()))
                        ksimplex_obj = KSimplex([int(v) for v in simplex.split()]) # They are already assumed to be sorted.
                        for sz in reversed(range(ksimplex_obj.k+1)):
                            times = None
                            sz_decflag = False
                            if len(ksimplex_obj.kvertices) == 1:
                                sz = 0
                            for comb in combinations(ksimplex_obj.kvertices,sz+1):
                                times = 0
                                if self.simplex_to_filtrationmap.get(comb,None) == None:
                                    self.add_simplex_toith_filtration(filtr_idx - 1, KSimplex(comb))
                                    self.simplex_to_filtrationmap[comb] = filtr_idx
                                    sz_decflag = True

                            if sz_decflag == False:
                                break
    def __str__(self):
        repr = ''
        for key, val in sorted(self.listof_iFiltration.items()):
            repr += "Filtration " + str(key) + '\n' + str(val) + "\n"

        return repr

    def __len__(self):
        return sum([len(a) for a in self.listof_iFiltration.values()])
