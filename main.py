from pathlib import Path
if not Path('model').exists():
    print('Generating new model')
    import generate_model
else:
    print('Using old model')

import test_model
import sys
test_model.main(sys.argv)
