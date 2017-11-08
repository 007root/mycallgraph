from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput
from datetime import datetime
def callgrafa(depth=3):
    rec_time = datetime.now().strftime("%Y-%m-%dT%H-%M")
    def call(fun):
        def wrapper(*args, **kwargs):
            fun_name = fun.__name__
            file_name = fun_name + '_' + rec_time
            config = Config(max_depth=depth)
            print PNG_TIME
            graphviz = GraphvizOutput(output_file=r'./%s.png' % file_name)
            with PyCallGraph(output=graphviz, config=config):
                return fun(*args, **kwargs)
        return wrapper
    return call
