__author__ = 'Naheed'
from simplexdisk import KSimplex
from boundaryoperator import Boundary
import memory_profiler

__author__ = 'Naheed'

INF = float('inf')


class IntervalComputation:

    def __init__(self, filtr):
        self.filtration_ar = [] # I will dump them as pickle objects and later use unpickle it in COmpute_interval
        self.simplex_to_indexmap = {} # use shelve here
        self.betti_intervals = None
        #self.representative_cycles = []

        maxk = -1
        for fil in filtr.listof_iFiltration.values():
            if fil.simplicial_complex.maxK > maxk:
                maxk = fil.simplicial_complex.maxK

        self.maxdim = maxk
        cnt = 0
        print 'ok'
        for i in range(len(filtr.listof_iFiltration)):
            for k in range(maxk + 1):
                for ksimplex in filtr.get_ksimplices_from_ithFiltration(k, i):
                    vertexlist = tuple(ksimplex.kvertices)
                    if vertexlist not in self.simplex_to_indexmap:
                        self.simplex_to_indexmap[vertexlist] = cnt
                        cnt += 1
                        self.filtration_ar.append(ksimplex)
        print 'hmm'
        # print [str(x) for x in self.filtration_ar]

        self.T = [None] * len(self.filtration_ar)
        self.marked = [False] * len(self.filtration_ar)
        self.j_ar = [None] * len(self.filtration_ar)

        #print self.simplex_to_indexmap


    def compute_intervals(self, K=None):
        """
        :param K: K as in Betti_K
        :return: Betti_0,Betti_1,...,upto Betti_K intervals
        """
        print "Computing Intervals.."
        if K:
            self.betti_intervals = [[] for i in range(K + 1)]
            #self.representative_cycles = [[] for i in range(K + 1)]
        else:
            self.betti_intervals = [[] for i in range(self.maxdim + 1)]
            #self.representative_cycles = [[] for i in range(self.maxdim + 1)]

        for j, sigmaj in enumerate(self.filtration_ar):
            if K:
                if sigmaj.k > K + 1:  # We only want  dimension upto K, i.e birth-death of 0,1,...,upto K simplices.
                    break  # K-simplices occur as boundary of K+1 simplices. therefore we need sigmaj.k <= K+1

            d,basis_z = self.remove_pivot_rows(sigmaj)
            #print d
            if len(d) == 0:
                self.marked[j] = True
            else:
                i, i_ind = self.get_maxindexd(d)
                k = self.filtration_ar[i].k  # dimension of sigmai (according to paper)
                self.j_ar[i] = j
                # print '+'.join([str(sigma) for sigma in d])
                self.T[i] = d
                if (self.filtration_ar[i].degree < sigmaj.degree):
                    self.betti_intervals[k].append((self.filtration_ar[i].degree, sigmaj.degree))
                    #self.representative_cycles[k].append(basis_z)

        for j, sigmaj in enumerate(self.filtration_ar):
            if K:
                if sigmaj.k > K:  # We only want  dimension upto K, i.e birth-death of 0,1,...,upto K simplices.
                    break  # K-simplices occur as boundary of K+1 simplices. therefore we need sigmaj.k <= K+1
            if self.marked[j] and self.j_ar[j] is None:
                k = sigmaj.k
                self.betti_intervals[k].append((sigmaj.degree, INF))
                #self.representative_cycles[k].append(sigmaj.kvertices)

    def remove_pivot_rows(self, simplex):
        assert isinstance(simplex, KSimplex)
        k = simplex.k
        bd = Boundary()
        d = set([]) # the column which will be reduced
        z = []  # the basis formed by repeated addition

        for sign, sigma in bd.compute_boundary(simplex):
            if self.marked[self.simplex_to_indexmap[tuple(sigma.kvertices)]]:
                d.add(tuple(sigma.kvertices))

        z.append(simplex)
        while 1:
            if len(d) == 0:
                break

            max_indexd, maxi_d = self.get_maxindexd(d)
            if self.j_ar[max_indexd] is None:
                break
            z.append(self.filtration_ar[self.j_ar[max_indexd]])
            # Gaussian elimination here
            d.symmetric_difference_update(self.T[max_indexd])

        return d,z

    def get_maxindexd(self, set_ofsimplex_d):

        max_indexd = -1
        maxi = -1
        for i, sigma_bd in enumerate(set_ofsimplex_d):
            #print sigma_bd
            cur_maxd = self.simplex_to_indexmap[sigma_bd]
            if cur_maxd > max_indexd:
                max_indexd = cur_maxd
                maxi = i
        return max_indexd, maxi

    def print_BettiNumbers(self):
        repr = ''
        for dim, li in enumerate(self.betti_intervals):
            repr += ('dim: ' + str(dim) + '\n')
            for tup in li:
                if tup[0] == tup[1]:
                    continue
                repr += str(tup)
            repr += '\n'
        print repr

    def write_Intervalstofile(self,filename):
        with open(filename,'w') as f:
            for dim, li in enumerate(self.betti_intervals):
                if dim == 1:
                    f.writelines(str(dim)+"\n")
                    for tup in li:
                        if tup[0] == tup[1]:
                            continue
                        f.writelines(str(tup)+"\n")



    # def get_representativs(self):
    #     """
    #     :return: Returns Representative Holes (BUGGY CODE)
    #     """
    #
    #     repr = ''
    #     for idx, whatever in enumerate(self.representative_cycles):
    #         if whatever:
    #             repr += "id: " + str(idx) + '{'
    #             for w in whatever:
    #                 repr += '+'.join([str(i) for i in w])
    #                 repr += " "
    #             repr += "}\n"
    #             # repr+="\n"
    #     print repr
