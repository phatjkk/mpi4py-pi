from mpi4py import MPI
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import  math , time
class MyApp(object):
    def __init__(self, slaves):
        self.master = Master(slaves)
        self.work_queue = WorkQueue(self.master)

    def terminate_slaves(self):
        self.master.terminate_slaves()

    def run(self,num_process):
        
        def f(x):
            return math.sqrt(1 - x ** 2)

        a = 0
        b = 1
        n = 100000

        h = (b - a) / n
        sum_total = (f(a) + f(b)) / 2

        # Chia task
        nums_task_per_slave = n // num_process

        for i in range(num_process):
            self.work_queue.add_work(data=(a,b,h, i * nums_task_per_slave ,(i+1) *nums_task_per_slave))

        if n % num_process > 0:
            self.work_queue.add_work(data=(a,b,h, n-(n % num_process),n))

        while not self.work_queue.done():
            self.work_queue.do_work()
            for slave_return_data in self.work_queue.get_completed_work():
                i, sum_slave = slave_return_data
                sum_total += sum_slave
        return sum_total *  h * 4 / 2


class MySlave(Slave):

    def __init__(self):
        super(MySlave, self).__init__()

    def do_work(self, data):
        def f(x):
            return math.sqrt(1 - x ** 2)
        a,b,h,i_start,i_end = data
        s = 0
        for i in range(i_start,i_end):
            s+= 2 * f(a + i * h)
        return i,s


def main():

    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    print('Runing processor %d (total %d)' % (rank, size))

    if rank == 0: # Master
        start = time.time()
        app = MyApp(slaves=range(1, size))
        result = app.run(num_process=size)
        app.terminate_slaves()
        end = time.time()
        total_time =  end - start
        print('Result PI:',result)
        print('Time:',total_time)

    else: # Any slave
        MySlave().run()
        
    if rank != 0:
        print('Slave %d is Done!' % (rank) )
    else:
        print('Master  %d is Done!' % (rank) )


if __name__ == "__main__":
    main()