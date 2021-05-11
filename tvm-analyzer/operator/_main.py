import tvm
import tvm.testing
from tvm import te
import numpy as np
from describe_computation import create_simple_sum
from compile_operator import compile_execute_raw_operator
from execute_operator import evaluate_addition
from update_schedule import update_by_parallel, update_by_vectorization_on_cpu

def create_compile_execute_operator(create_fun, tgt, optimize_type="naive", name="myadd", update_schedule_fun=None, factor= 4):
    # create schedulue an operator on the target:
    schedule, variables = create_fun()
    if update_schedule_fun != None:
        schedule = update_schedule_fun(schedule, variables, name, factor)
    # compile the operator
    operator = compile_execute_raw_operator(schedule, variables, tgt, name=name)
    # execute (compare, evaluate) operator by evaluate execution time:
    evaluate_addition(operator, tgt, optimize_type, name, variables)
    return operator

create_compile_execute_operator(create_simple_sum, tvm.target.Target(target="llvm", host="llvm"),name="myadd")

create_compile_execute_operator(create_simple_sum, tvm.target.Target(target="llvm", host="llvm"), optimize_type="parallel", name="myadd_parallel", update_schedule_fun = update_by_parallel)

create_compile_execute_operator(create_simple_sum, tvm.target.Target(target="llvm", host="llvm"), optimize_type="vectorization", name="myadd_vectorization", update_schedule_fun = update_by_vectorization_on_cpu, factor = 20)
