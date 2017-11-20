from __future__ import absolute_import
from src.Filtration import Filtration
import sys
from src.ComputeInterval_Disk import IntervalComputation
import memory_profiler


def test_persistencehomology():


    name = "/Users/naheed/NetBeansProjects/jplex_explore/testcase_2"
    #name = "/Users/naheed/NetBeansProjects/jplex_explore/graph1"
    #name = "/Users/naheed/NetBeansProjects/Toy-1.5 63 (6 big cycle)"
    #name = "/Users/naheed/NetBeansProjects/Trivial-1"
    # name = "/Users/naheed/NetBeansProjects/Dexa-Paper Dataset"
    #name = "/Users/naheed/NetBeansProjects/jplex_explore/watts-strogatz/watts-strogatz_11"
    #name = "/Users/naheed/NetBeansProjects/jplex_explore/3437-7"
    #name = "/Users/naheed/NetBeansProjects/Toy-2 262143"
    #name = "/Users/naheed/NetBeansProjects/Toy-4 4095(12 Big Cycle)"
    #name = "/Users/naheed/NetBeansProjects/Toy-3 2047 (11 Vertex Big Cylce)"
    #name = "/Users/naheed/NetBeansProjects/jplex_explore/netscience_10101023"
    #name = "/Users/naheed/NetBeansProjects/Toy-2 262143"
    #fil.add_simplices_from_cliquefiles_ensureinclusion(name)
    name = "/Users/naheed/PycharmProjects/PHComputation/data/test_simplexfromfile.txt"

    fil = Filtration(name.split("/")[-1])
    print fil.maxdeg

    fil.add_simplices_from_file(name)
    print 'size occupied:', sys.getsizeof(fil)
    # fil.add_simplices_from_cliquefiles(name)
    fil._writebackMRUfil()
    # print 'total number of Simplices: ',len(fil)


    ci = IntervalComputation(fil)
    ci.compute_intervals()
    ci.print_BettiNumbers()
    # ci.write_Intervalstofile(name+"/result.betti")
    print sys.getsizeof(ci.T)
    fil.listof_iFiltration.close()

if __name__ == "__main__":
    # test_File_Filtration()
    test_persistencehomology()
    #test_manual_Filtration()
    # test_manual_simplex()
    # test_file_simplex()
    # test_boundary_op()
    # test_nested_boundary()
    # test_nested_boundary_simplicialcomplex()
    # test_kth_boundary_group()
