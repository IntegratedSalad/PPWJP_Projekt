from app import App
from simulation import Simulation

td = '''
  ___
{~._.~}
 ( Y )
()~*~()
(_)-(_)
'''

def main():
    _app = App(Simulation())
    _app.run()
    print("Bye!")
    print(td)

if __name__ == '__main__':
    main()
