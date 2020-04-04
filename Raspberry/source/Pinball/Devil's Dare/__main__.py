import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def main(args=None):
    pinball = Game_Operation(use_gui=True)
    pinball.power_on()
	
if __name__ == "__main__":
    main()