import tvm
import tvm.testing
from tvm import te
import numpy as np

def compile_execute_raw_operator(schedules, variables, tgt, name):
    fadd = tvm.build(schedules, variables, tgt, name=name)
    dev = tvm.device(tgt.kind.name, 0)
    if "myadd" in name:
        n = 1024
        a = tvm.nd.array(np.random.uniform(size=n).astype(variables[0].dtype), dev)
        b = tvm.nd.array(np.random.uniform(size=n).astype(variables[1].dtype), dev)
        c = tvm.nd.array(np.zeros(n, dtype=variables[2].dtype), dev)
        fadd(a, b, c)
        tvm.testing.assert_allclose(c.asnumpy(), a.asnumpy() + b.asnumpy())
    return fadd