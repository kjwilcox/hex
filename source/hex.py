
import menu

try:
    import psyco
    psyco.full()
    print "Psyco is enabled"
except ImportError:
    print "Psyco not enabled"


main = menu.Menu()
main.main_loop()
del main
