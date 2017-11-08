import tempfile
import os
import subprocess as sub
import textwrap
from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput
from datetime import datetime
from awsutil import conf as s3conf
from awsutil import s3sync
S3BOTO = ''
PNG_TIME = ''
TIMEFORMAT = '%Y-%m-%dT%H:%M:%S'


class GraphOutput(GraphvizOutput):
    def done(self):
        source = self.generate()

        self.debug(source)

        fd, temp_name = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as f:
            f.write(source)

        cmd = '"{0}" -T{1} {2}'.format(
            self.tool, self.output_type, temp_name
        )

        self.verbose('Executing: {0}'.format(cmd))
        try:
            s3_sess = s3conf.get_session(S3BOTO)
            s3_client = s3sync.S3sync(s3_sess, 'test-gbm-upload')
            proc = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
            ret, output = proc.communicate()
            s3_client.put(self.output_file, ret)
        finally:
            os.unlink(temp_name)

        self.verbose('Generated {0} with {1} nodes.'.format(
            self.output_file, len(self.processor.func_count),
        ))

def callgraph(depth=3, min_minute=10):
    def call(fun):
        def wrapper(*args, **kwargs):
            rec_time = datetime.now()
            fun_name = fun.__name__
            last_time = PNG_TIME.get(fun_name, None)
            if last_time:
                sec = rec_time - last_time
                if sec.seconds / 60 > min_minute:
                    file_name = fun_name + '_' + rec_time.strftime(TIMEFORMAT)
                    config = Config(max_depth=depth)
                    graphviz = GraphOutput(output_file='%s.png' % file_name)
                    with PyCallGraph(output=graphviz, config=config):
                        PNG_TIME[fun_name] = rec_time
                        return fun(*args, **kwargs)
                else:
                    return fun(*args, **kwargs)
            else:
                PNG_TIME[fun_name] = rec_time
                return fun(*args, **kwargs)
        return wrapper
    return call
